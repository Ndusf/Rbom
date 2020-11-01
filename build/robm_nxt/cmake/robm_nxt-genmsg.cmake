# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "robm_nxt: 1 messages, 0 services")

set(MSG_I_FLAGS "-Irobm_nxt:/home/ny/catkin_ws/src/robm_nxt/msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(robm_nxt_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_custom_target(_robm_nxt_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "robm_nxt" "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(robm_nxt
  "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robm_nxt
)

### Generating Services

### Generating Module File
_generate_module_cpp(robm_nxt
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robm_nxt
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(robm_nxt_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(robm_nxt_generate_messages robm_nxt_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_dependencies(robm_nxt_generate_messages_cpp _robm_nxt_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robm_nxt_gencpp)
add_dependencies(robm_nxt_gencpp robm_nxt_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robm_nxt_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(robm_nxt
  "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robm_nxt
)

### Generating Services

### Generating Module File
_generate_module_eus(robm_nxt
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robm_nxt
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(robm_nxt_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(robm_nxt_generate_messages robm_nxt_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_dependencies(robm_nxt_generate_messages_eus _robm_nxt_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robm_nxt_geneus)
add_dependencies(robm_nxt_geneus robm_nxt_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robm_nxt_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(robm_nxt
  "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robm_nxt
)

### Generating Services

### Generating Module File
_generate_module_lisp(robm_nxt
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robm_nxt
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(robm_nxt_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(robm_nxt_generate_messages robm_nxt_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_dependencies(robm_nxt_generate_messages_lisp _robm_nxt_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robm_nxt_genlisp)
add_dependencies(robm_nxt_genlisp robm_nxt_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robm_nxt_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(robm_nxt
  "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robm_nxt
)

### Generating Services

### Generating Module File
_generate_module_nodejs(robm_nxt
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robm_nxt
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(robm_nxt_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(robm_nxt_generate_messages robm_nxt_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_dependencies(robm_nxt_generate_messages_nodejs _robm_nxt_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robm_nxt_gennodejs)
add_dependencies(robm_nxt_gennodejs robm_nxt_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robm_nxt_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(robm_nxt
  "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robm_nxt
)

### Generating Services

### Generating Module File
_generate_module_py(robm_nxt
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robm_nxt
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(robm_nxt_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(robm_nxt_generate_messages robm_nxt_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ny/catkin_ws/src/robm_nxt/msg/MotorCommand.msg" NAME_WE)
add_dependencies(robm_nxt_generate_messages_py _robm_nxt_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robm_nxt_genpy)
add_dependencies(robm_nxt_genpy robm_nxt_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robm_nxt_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robm_nxt)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robm_nxt
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(robm_nxt_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robm_nxt)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robm_nxt
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(robm_nxt_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robm_nxt)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robm_nxt
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(robm_nxt_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robm_nxt)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robm_nxt
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(robm_nxt_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robm_nxt)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robm_nxt\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robm_nxt
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(robm_nxt_generate_messages_py sensor_msgs_generate_messages_py)
endif()
