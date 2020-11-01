;; Auto-generated. Do not edit!


(when (boundp 'robm_nxt::MotorCommand)
  (if (not (find-package "ROBM_NXT"))
    (make-package "ROBM_NXT"))
  (shadow 'MotorCommand (find-package "ROBM_NXT")))
(unless (find-package "ROBM_NXT::MOTORCOMMAND")
  (make-package "ROBM_NXT::MOTORCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude MotorCommand.msg.html


(defclass robm_nxt::MotorCommand
  :super ros::object
  :slots (_speed_B _speed_C ))

(defmethod robm_nxt::MotorCommand
  (:init
   (&key
    ((:speed_B __speed_B) 0.0)
    ((:speed_C __speed_C) 0.0)
    )
   (send-super :init)
   (setq _speed_B (float __speed_B))
   (setq _speed_C (float __speed_C))
   self)
  (:speed_B
   (&optional __speed_B)
   (if __speed_B (setq _speed_B __speed_B)) _speed_B)
  (:speed_C
   (&optional __speed_C)
   (if __speed_C (setq _speed_C __speed_C)) _speed_C)
  (:serialization-length
   ()
   (+
    ;; float32 _speed_B
    4
    ;; float32 _speed_C
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _speed_B
       (sys::poke _speed_B (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _speed_C
       (sys::poke _speed_C (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _speed_B
     (setq _speed_B (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _speed_C
     (setq _speed_C (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get robm_nxt::MotorCommand :md5sum-) "9ba6bdab22f53c19b2150f8a9af566e0")
(setf (get robm_nxt::MotorCommand :datatype-) "robm_nxt/MotorCommand")
(setf (get robm_nxt::MotorCommand :definition-)
      "float32 speed_B 
float32 speed_C

")



(provide :robm_nxt/MotorCommand "9ba6bdab22f53c19b2150f8a9af566e0")


