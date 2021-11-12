# Examen Parcial de ROS en Python

⚠️  Los paquetes proporcionados por el profesor se encuentran en el aula virual, por motivos de derechos no se han publicado aquí.⚠️
## Instrucciones para ejecutar

1- Compilar todos los paquetes
2- Ejecutar *roscore* en un terminal.
3- Ejecutar el *turtlesim* en otro terminal:
    - `rosrun turtlesim turtlesim_node`
4- Lanzar los paquetes del profesor (en cualquier orden) en otros dos terminales:
    - `rosrun accion_mueve_a_posicion accion_examen_final.py`
    - `rosrun servicio_vuelta_a_casa servicio_vuelta.py`
5- Ejecutar el paquete **examen_pub_destino** en otro terminal:
    - `rosrun examen_pub_destino examen_pub_dest.py`
6- Ejecutar el paquete **examen_turtle_destino** en otro terminal:
    - `rosrun examen_turtle_destino examen_turtle_dest.py`
7- Desde otro terminal ejecutar una primera llamada al *topic* **/destino** para teleportar a la tortuga a la posicion inicial y luego volver a ejecutar lo mismo pero con otras posiciones *x* e *y*:
```
rostopic pub /destino examen_pub_destino/nueva_pos "id: 0 posicion:
  x: 0.0
  y: 0.0
  z: 0.0"
```

