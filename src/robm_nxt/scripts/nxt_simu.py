#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import rospy
from sensor_msgs.msg import Range, JointState
from robm_nxt.msg import MotorCommand
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA

import numpy as np
from numpy import cos, sin, pi, sqrt, array

import time
import threading

from geometry_msgs.msg import Quaternion, Vector3, Point
from tf.transformations import quaternion_from_euler

# Create a Quaternion message representiong yaw rotation
def quaternion_msg_from_yaw(yaw):
	q = quaternion_from_euler(0.0, 0.0, yaw)
	return Quaternion(*q)

######################################################################
## Robot and environment simulation

class RobotSim:
    env_segments = []
    
    def process(self):
        for k in range(10):
            self.tick()
    
    def __init__(self):        
        self.t = 0.0

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.v = 1.0 #*0
        self.w = 0.4 #*2

        self._last_control = -1e10
        self._control_avoid = False
        
        self._last_x = self.x;
        self._last_y = self.y;
        self._last_theta = self.theta;
        self._last_t = self.t;
    
    def measured_displacement(self):
        dx = self.x - self._last_x;
        dy = self.y - self._last_y;
        dtheta = self.theta - self._last_theta;
        dt = self.t - self._last_t;
        
        dx_bf = cos(-self._last_theta)*dx - sin(-self._last_theta)*dy
        dy_bf = sin(-self._last_theta)*dx + cos(-self._last_theta)*dy
        
        self._last_x = self.x;
        self._last_y = self.y;
        self._last_theta = self.theta;
        self._last_t = self.t;
        
        return dx_bf, dy_bf, dtheta, dt
    
    def command(self, v, w):
        self.v = v
        self.w = w
    
    def evolve(self, dt = 0.02):
        # Block movement if there is a wall in the direction
        theta_move = self.theta if self.v >= 0 else self.theta + pi
        d = distance_cone_environnement(self.x, self.y, theta_move, self.env_segments, 10.0 * pi / 180.)
        if d > 0.15:
            self.x += dt * self.v * cos(self.theta)
            self.y += dt * self.v * sin(self.theta)
        self.theta += dt * self.w
        self.t += dt
    
    def observe(self):
        return distance_cone_environnement(self.x, self.y, self.theta, self.env_segments, 10.0 * pi / 180.) \
            + np.random.uniform(-0.005, 0.005) + np.random.normal(0, 0.02)
    
    def state(self):
        return [self.x, self.y, self.theta]


#@jit(nopython=True)
def segment_directional_distance(o, v, a, b):
    v1 = o - a
    v2 = b - a
    v3 = np.array([-v[1], v[0]], dtype=np.float64)
    v2_v3 = v2.dot(v3)
    if v2_v3 == 0: return np.inf
    t2 = (v1.dot(v3)) / (v2_v3)
    if not 0 <= t2 <= 1: return np.inf
    v2_X_v1 = v2[0]*v1[1] - v2[1]*v1[0]
    t1 = v2_X_v1 / v2_v3
    if t1 < 0: return np.inf
    return t1

#@jit(nopython=True)
def segment_directional_distance_no_cull(o, v, a, b):
    v1 = o - a
    v2 = b - a
    v3 = np.array([-v[1], v[0]], dtype=np.float64)
    v2_v3 = v2.dot(v3)
    if v2_v3 == 0: return (np.inf,np.inf)
    t2 = (v1.dot(v3)) / (v2_v3)
    v2_X_v1 = v2[0]*v1[1] - v2[1]*v1[0]
    t1 = v2_X_v1 / v2_v3
    return (t1, t2)

#@jit(nopython=True)
def segment_pie_distance(o, v1, v2, a, b):
    """ Return the shortest directionnal distance from o to line segment [ab] 
    within the cone defined by unit direction vectors v1 and v2
    """
    d1, s1 = segment_directional_distance_no_cull(o, v1, a, b)
    d2, s2 = segment_directional_distance_no_cull(o, v2, a, b)
    
    # Reject if both pie limit vectors point away from the supporting line (ab)
    if d1 < 0 and d2 < 0:
        return (np.inf,np.inf)
    
    if d1 < 0:
        # swap v1 and v2, to reduce to the d2<0 case
        v1,v2 = v2,v1
        (d1,s1),(d2,s2) = (d2,s2),(d1,s1)
    
    if d2 < 0:
        # If (d1,d2) angle spans in a->b direction
        if s2 < s1:
            if s1 > 1: # Reject if the cone only spans on the b-side invalid half-line
                return (np.inf,np.inf)
            else: # Cap to the b bound
                s2 = 1
                d2 = np.linalg.norm(b-o)
        else:
            if s1 < 0: # Reject if the cone only spans on the a-side invalid half-line
                return (np.inf,np.inf)
            else: # Cap to the a bound
                s2 = 0
                d2 = np.linalg.norm(a-o)
    
    # reorder v1 and v2
    if s1>s2:
        v1,v2 = v2,v1
        (d1,s1),(d2,s2) = (d2,s2),(d1,s1)
    
    # Reject if both vectors intersect on the same invalid half-line
    if s2 < 0 or s1 > 1:
        return (np.inf,np.inf)
    
    # Cap to the line-segment bounds
    if s1 < 0:
        s1 = 0
        d1 = np.linalg.norm(a-o)
    if s2 > 1:
        s2 = 1
        d2 = np.linalg.norm(b-o)
        
    # Compute orthogonal projection and distance
    ab = b-a
    n = np.array([-ab[1], ab[0]]) / np.linalg.norm(ab)
    dn, sn = segment_directional_distance_no_cull(o, n, a, b)
    
    # Return the orthogonal distance if the orthogonal projection is within the s1,s2 bounds
    if s1 < sn < s2:
        return ( np.abs(dn), sn )
    
    # Otherwise, min distance is on the bounds
    return (d1,s1) if d1<d2 else (d2,s2)


#@jit
def env_directional_distance(o, v, env_segments):
    d = np.inf
    for seg in env_segments:
        a = np.array([seg[0][0], seg[1][0]], dtype=np.float64)
        b = np.array([seg[0][1], seg[1][1]], dtype=np.float64)
        ds = segment_directional_distance(o,v, a,b )
        if d>ds: d=ds
    return d


#@jit
def env_pie_distance(o, v1, v2, env_segments):
    d = np.inf
    for seg in env_segments:
        a = np.array([seg[0][0], seg[1][0]], dtype=np.float64)
        b = np.array([seg[0][1], seg[1][1]], dtype=np.float64)
        ds = segment_pie_distance(o,v1,v2, a,b )[0]
        if d>ds: d=ds
    return d


#@jit
def distance_cone_environnement(x, y, theta, env_segments, aperture=10.0 * pi / 180.):
    v1 = array([ cos(theta + aperture), sin(theta + aperture) ], dtype=np.float64)
    v2 = array([ cos(theta - aperture), sin(theta - aperture) ], dtype=np.float64)
    o = array([x, y], dtype=np.float64)
    return env_pie_distance(o, v1, v2, env_segments)


#@jit
def distance_rayon_environnement(x, y, theta, env_segments):
    v = array([ cos(theta), sin(theta) ], dtype=np.float64)
    o = array([x, y], dtype=np.float64)
    return env_directional_distance(o, v, env_segments)


######################################################################
## NXT stub classes

class Tacho:
    def __init__(self):
        self.tacho_count = 0.0

class Motor:
    def __init__(self):
        self._tacho = Tacho()
        self._speed = 0.0
        self._K = 16.8 / 100.0 * 180.0 / pi

    def get_tacho(self):
        return self._tacho
    
    def get_speed(self):
        return self._speed * pi / 180.0

    def run(self, speed, regulated):
        self._speed = speed * self._K * (1.0 + np.random.normal(0, 0.003))
    
    def update(self, Te):
        self._tacho.tacho_count += Te * self._speed

    def idle(self):
        self.run(0.0, False)

class Ultrasonic:
    def __init__(self, simu):
        self._simu = simu

    def get_sample(self):
        return int(100 * simu.observe())

######################################################################
## NXT ROS driver

# watchdog counter and lock
watchdog_count = 0
watchdog_lock = threading.Lock()

motor_B = Motor()
motor_C = Motor()

# Environnement simulé
env_points = [[-1,1], [-1,-1.5], [1,-1.5], [2,2]] # pas de symétrie
#env_points = [[-1,1], [-1,-1], [1,-1], [2,2]] # juste un axe de symétrie (pas de rotation)
#env_points = [[-1,2], [-1,-1], [1,-1], [1,2]] # symétrie rotation 180° (rectangle)
#env_points = [[-1,1.5], [-1,-1], [1.5,-1], [1.5,1.5]] # symétrie rotation 90° (carré)
#env_points = [[-0.9,1.5], [-1.1,-1], [1.5,-1], [1.5,1.5]] # symétrie rotation 90° (carré)

env_vertices = [[0,1], [1,2], [2,3], [3,0]]

env_segments = [ [ [env_points[e][0] for e in v] , [env_points[e][1] for e in v] ] for v in env_vertices ]
RobotSim.env_segments = env_segments

simu = RobotSim()

def motor_thread():
    global motor_B, motor_C
    global simu
    # ROS topic publisher
    pub = rospy.Publisher('nxt/encoders', JointState, queue_size=10)
    pub_viz = rospy.Publisher('visualization_marker', Marker, queue_size=10)
    # The message to publish
    js_msg = JointState()
    js_msg.name = ['motor_B', 'motor_C']
    # Rate limiter for main loop
    rate = rospy.Rate(10)
    # Process loop
    while not rospy.is_shutdown():
        # Update motor counts
        motor_B.update(1.0 / 10.0)
        motor_C.update(1.0 / 10.0)
        # Apply motor speeds to simu
        r = 0.0166
        L = 0.15
        v1 = motor_B.get_speed() * r
        v2 = motor_C.get_speed() * r
        v = (v1 + v2) / 2
        w = (v1 - v2) / L
        simu.command(v, w)
        for k in range(10):
            simu.evolve(dt=0.02)
        # Read motor information
        try:
            count_B = motor_B.get_tacho().tacho_count
            count_C = motor_C.get_tacho().tacho_count
        except:
            rospy.logfatal("Connection with NXT robot interrupted!")
            rospy.signal_shutdown("Connexion error")
        # Fill and send ROS motor position message
        js_msg.header.stamp = rospy.Time.now()
        js_msg.position = [pi/180.0*count_B, pi/180.0*count_C]
        pub.publish(js_msg)
        # Fill and send visualization message
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "nxt_simu"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        [x, y, theta] = simu.state()
        marker.pose.position = Point(x, y, 0.0)
        marker.pose.orientation = quaternion_msg_from_yaw(theta)
        marker.scale = Vector3(0.2, 0.1, 0.1)
        marker.color = ColorRGBA(0.0, 1.0, 0.0, 1.0)
        pub_viz.publish(marker)
        marker.id = 1
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        [x, y, theta] = simu.state()
        marker.pose.position = Point(x, y, 0.12)
        marker.pose.orientation = quaternion_msg_from_yaw(theta)
        marker.scale = Vector3(0.10, 0.03, 0.03)
        marker.color = ColorRGBA(0.0, 0.0, 1.0, 1.0)
        pub_viz.publish(marker)
        marker.id = 2
        marker.type = Marker.LINE_LIST
        marker.pose.position = Point(0.0, 0.0, 0.0)
        marker.pose.orientation = quaternion_msg_from_yaw(0.0)
        marker.scale = Vector3(0.03, 0.03, 0.03)
        marker.color = ColorRGBA(1.0, 0.0, 0.0, 1.0)
        for v in env_vertices:
            for e in v:
                marker.points.append(Point(env_points[e][0], env_points[e][1], 0))
        pub_viz.publish(marker)

        # Wait before next loop
        rate.sleep()

def distance_thread():
    global simu
    # ROS topic publisher for sonar distance readings
    pub = rospy.Publisher('nxt/sonar', Range, queue_size=10)
    # Sonar driver
    ultrasonic = Ultrasonic(simu)
    # Setup the ROS range message with sensor properties
    range_msg = Range()
    range_msg.radiation_type = Range.ULTRASOUND
    range_msg.field_of_view = 10.0 * pi / 180.0
    range_msg.min_range = 0.01
    range_msg.max_range = 2.55
    # Rate limiter for process loop
    rate = rospy.Rate(4)
    # Main process loop
    while not rospy.is_shutdown():
        # Perform and read US range measurement
        #try:
        d = ultrasonic.get_sample()
        #except:
        #    rospy.logfatal("Connection with NXT robot interrupted!")
        #    rospy.signal_shutdown("Connexion error")
        # Fill and publish the ROS range message
        range_msg.header.stamp = rospy.Time.now()
        range_msg.range = 0.01 * d
        pub.publish(range_msg)
        # Wait until next loop
        rate.sleep()
        

speed_cmd = MotorCommand()


def update_motors_speed():
    global watchdog_count
    global watchdog_lock
    global motor_B, motor_C

    # Rate limiter for process loop
    rate = rospy.Rate(10)
    # Main process loop
    while not rospy.is_shutdown():
        timeout = False
        needsupdate = False

        with watchdog_lock:
            if watchdog_count == 0:
                needsupdate = True
                speed_B = speed_cmd.speed_B
                speed_C = speed_cmd.speed_C
            if watchdog_count >= 0:
                watchdog_count += 1
            if watchdog_count > 20:
                timeout = True
                watchdog_count = -1

        try:
            if needsupdate:
                motor_B.run(100.0 * speed_B, regulated=True)
                motor_C.run(100.0 * speed_C, regulated=True)
            if timeout:
                rospy.logwarn("Motors stopped, no command received in the last 2 secs")
                motor_B.idle()
                motor_C.idle()
        except:
            rospy.logfatal("Connection with NXT robot interrupted!")
            rospy.signal_shutdown("Connexion error")
            
        rate.sleep()
    
    # Stop motors before terminating
    try:
        rospy.loginfo("Stopping motors before quiting")
        motor_B.idle()
        motor_C.idle()
    except:
        rospy.logerr("Unable to set motors to idle state")


def motor_callback(msg):
    global watchdog_count
    global watchdog_lock
    global speed_cmd
    
    # Clear watchdog
    with watchdog_lock:
        watchdog_count = 0
        speed_cmd = msg

def nxt_ros():
    # Initialize ROS node
    rospy.init_node('nxt_simu')
    
    # Find a brick
    rospy.loginfo("nxt simulator v0.1 started")
    
    # Setup the sensor-reading thread pool
    threads = []
    threads.append( threading.Thread(target=motor_thread) )
    threads.append( threading.Thread(target=distance_thread) )
    threads.append( threading.Thread(target=update_motors_speed) )

    # Start sensor-reading threads
    for t in threads:
        t.start()
    # Subscribe to motor command
    motor_sub = rospy.Subscriber("nxt/command", MotorCommand, motor_callback)
    # Process incoming ROS messages until termination
    rospy.spin()
    # Here, the node is stopping, wait for all threads to finish
    for t in threads:
        t.join()
    
if __name__ == '__main__':
    try:
        nxt_ros()
    except rospy.ROSInterruptException:
        pass
    except:
        rospy.logfatal("Connection with NXT simu interrupted!")
        sys.exit(1)
        
