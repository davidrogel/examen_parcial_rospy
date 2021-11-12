#!/usr/bin/env python

import rospy
import actionlib
from examen_pub_destino.msg import nueva_pos
from accion_mueve_a_posicion.msg import (AccionExamenAction, AccionExamenGoal,
        AccionExamenFeedback, AccionExamenResult)
from servicio_vuelta_a_casa.srv import ServicioExamen, ServicioExamenRequest
from turtlesim.srv import TeleportAbsolute, TeleportAbsoluteRequest
from std_msgs.msg import String
from std_srvs.srv import Empty, EmptyRequest

primer_msg = True

def feedback_cb(feed):
    if feed.realimentacion < 2.0:
        cliente_mueve_recto.cancel_goal()
        a_casa = ServicioExamenRequest()
        he_llegado_bien = servicio_vuelve_a_casa(a_casa)
        if he_llegado_bien:
            rospy.wait_for_service('/clear')
            servicio_clear = rospy.ServiceProxy('/clear', Empty)
            servicio_clear(EmptyRequest())

def done_cb(g, a):
    if a.exito:
        msg = String()
        msg.data = "dame_nueva_posicion"
        pub_nueva_pos.publish(msg)

def callback_destino(msg):
    global primer_msg
    global cliente_mueve_recto
    if primer_msg: # el primer destino que llega
        teleport = TeleportAbsoluteRequest()
        teleport.x = msg.posicion.x
        teleport.y = msg.posicion.y
        teleport.theta = msg.posicion.z
        servicio(teleport)
        primer_msg = False
    else: # el resto de los destinos
        # si es un id = 12
        if msg.id > 12:
            if cliente_mueve_recto.get_state() != 1:
                cliente_mueve_recto.cancel_goal()
                a_casa = ServicioExamenRequest()
                he_llegado_bien = servicio_vuelve_a_casa(a_casa)
                if he_llegado_bien:
                    terminar_msg = String()
                    terminar_msg.data = "terminar"
                    pub_nueva_pos.publish(terminar_msg)

        m_goal = AccionExamenGoal()
        m_goal.x = msg.posicion.x
        m_goal.y = msg.posicion.y
        cliente_mueve_recto.send_goal(m_goal, done_cb=done_cb, feedback_cb=feedback_cb)
        cliente_mueve_recto.wait_for_server()


rospy.init_node('examen_turtle_destino_nodo')

# esperamos por el servicio para teleportar y lo creamos
rospy.wait_for_service('/turtle1/teleport_absolute')
servicio = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)

# nos suscribimos al destino
rospy.Subscriber('/destino', nueva_pos, callback_destino)
# generamos el publisher para pedir nuevas posiciones
pub_nueva_pos = rospy.Publisher('/comando', String, queue_size=1)

# generamos el cliente de la accion
cliente_mueve_recto = actionlib.SimpleActionClient('mueve_robot', AccionExamenAction)

# servicio de vuelta a casa
rospy.wait_for_service('/vuelve_a_casa')
servicio_vuelve_a_casa = rospy.ServiceProxy('/vuelve_a_casa', ServicioExamen)

rospy.spin()
