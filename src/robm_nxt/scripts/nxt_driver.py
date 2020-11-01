#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Range, JointState
from robm_nxt.msg import MotorCommand

from math import pi

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import time
import threading

import nxt.bluesock
import nxt.usbsock

# The brick
b = None

# watchdog counter and lock
watchdog_count = 0
watchdog_lock = threading.Lock()

def motor_thread():
	global b
	# ROS topic publisher
	pub = rospy.Publisher('nxt/encoders', JointState, queue_size=10)
	# Motor drivers
	motor_B = Motor(b, PORT_B)
	motor_C = Motor(b, PORT_C)
	# The message to publish
	js_msg = JointState()
	js_msg.name = ['motor_B', 'motor_C']
	# Rate limiter for main loop
	rate = rospy.Rate(10)
	# Process loop
	while not rospy.is_shutdown():
		# Read motor information
		try:
			count_B = motor_B.get_tacho().tacho_count
			count_C = motor_C.get_tacho().tacho_count
		except:
			rospy.logfatal("Connection with NXT robot interrupted!")
			rospy.signal_shutdown("Connexion error")
		# Fill and send ROS message
		js_msg.header.stamp = rospy.Time.now()
		js_msg.position = [pi/180.0*count_B, pi/180.0*count_C]
		pub.publish(js_msg)
		# Wait before next loop
		rate.sleep()
		
def distance_thread():
	global b
	# ROS topic publisher for sonar distance readings
	pub = rospy.Publisher('nxt/sonar', Range, queue_size=10)
	# Sonar driver
	ultrasonic = Ultrasonic(b, PORT_4)
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
		try:
			d = ultrasonic.get_sample()
		except:
			rospy.logfatal("Connection with NXT robot interrupted!")
			rospy.signal_shutdown("Connexion error")
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
	global b
	
	motor_B = Motor(b, PORT_B)
	motor_C = Motor(b, PORT_C)
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
	global b
	global watchdog_count
	global watchdog_lock
	global speed_cmd
	
	# Clear watchdog
	with watchdog_lock:
		watchdog_count = 0
		speed_cmd = msg
	## Set motor speed
	#motor_B = Motor(b, PORT_B)
	#motor_C = Motor(b, PORT_C)
	#motor_B.run(100.0 * msg.speed_B, regulated=True)
	#motor_C.run(100.0 * msg.speed_C, regulated=True)


def nxt_ros():
	global b
	# Initialize ROS node
	rospy.init_node('nxt_driver')
	
	# Find a brick
	rospy.loginfo("nxt_driver v0.3 started")
	
	conf = nxt.locator.read_config()
	name = conf.get('Brick', 'name')
	host = conf.get('Brick', 'host')
	if name == None or host == None:
		rospy.logwarn("The ~/.nxt-config file does not contain all NXT brick info! Please run nxt_register.py to fix this.")
	
	# Try USB first
	try:
		rospy.loginfo("Searching for NXT brick on USB...")
		b = nxt.locator.find_one_brick(name=name, host=host, strict=True, method=nxt.locator.Method(usb=True, bluetooth=False, fantomusb=False))
		rospy.loginfo("Brick found on USB!")
	except:
		b = None
	
	# Then try Bluetooth (direct connection)
	if not b:
		try:
			rospy.loginfo("Searching for NXT brick on Bluetooth...")
			s = nxt.bluesock.BlueSock(host)
			b = s.connect()
			rospy.loginfo("Brick found on Bluetooth!")
		except:
			b = None
	
	if not b:
		rospy.logfatal("Unable to connect to NXT brick... ending")
		return
	
	#b = nxt.locator.find_one_brick(host='00:16:53:0D:7D:4C')
	#b = nxt.bluesock.BlueSock('00:16:53:0D:7D:4C').connect()
	info = b.get_device_info()
	rospy.loginfo("Connected to brick '%s' (%s)", info[0], info[1])

	
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
		rospy.logfatal("Connection with NXT robot interrupted!")
		sys.exit(1)
		
