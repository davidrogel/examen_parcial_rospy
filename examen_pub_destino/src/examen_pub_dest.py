#!/usr/bin/env python

import random
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
from examen_pub_destino.msg import nueva_pos

def callback(msg):
    global exit
    if msg.data == 'dame_nueva_posicion':
        pos = nueva_pos()
        pos.id = random.randint(1, 15)
        pos.posicion.x = random.uniform(0.5, 10)
        pos.posicion.y = random.uniform(0.5, 10)
        pos.posicion.z = random.uniform(0, 3.14)
        pub.publish(pos)
    elif msg.data == 'terminar':
        exit = True

rospy.init_node('examen_pub_destino_nodo')

pub = rospy.Publisher('/destino', nueva_pos, queue_size=1)
rospy.Subscriber('/comando', String, callback)

exit = False
rate = rospy.Rate(1)

while not exit:
    rate.sleep()
