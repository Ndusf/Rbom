#!/usr/bin/env python

import rospy

# Importer la classe du message MotorCommand
from robm_nxt.msg import MotorCommand

# Initialize ROS node (named 'avance')
rospy.init_node('avance', anonymous=True)

# Instanciate ROS topic publisher motor commands (on 'nxt/command' topic). Use latch=True
pub = rospy.Publisher('nxt/command', MotorCommand, queue_size=10, latch=True)

# Create MotorCommand message and publish
msg_avance = MotorCommand()
msg_avance.speed_B = +1.0
msg_avance.speed_C = +1.0

pub.publish(msg_avance)


# Wait 1 sec
rospy.sleep(1.0)


# Publish zero-speed command message
msg_avance = MotorCommand()
msg_avance.speed_B = +0
msg_avance.speed_C = +0

pub.publish(msg_avance)


