// Auto-generated. Do not edit!

// (in-package robm_nxt.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class MotorCommand {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.speed_B = null;
      this.speed_C = null;
    }
    else {
      if (initObj.hasOwnProperty('speed_B')) {
        this.speed_B = initObj.speed_B
      }
      else {
        this.speed_B = 0.0;
      }
      if (initObj.hasOwnProperty('speed_C')) {
        this.speed_C = initObj.speed_C
      }
      else {
        this.speed_C = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MotorCommand
    // Serialize message field [speed_B]
    bufferOffset = _serializer.float32(obj.speed_B, buffer, bufferOffset);
    // Serialize message field [speed_C]
    bufferOffset = _serializer.float32(obj.speed_C, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MotorCommand
    let len;
    let data = new MotorCommand(null);
    // Deserialize message field [speed_B]
    data.speed_B = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [speed_C]
    data.speed_C = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'robm_nxt/MotorCommand';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9ba6bdab22f53c19b2150f8a9af566e0';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 speed_B 
    float32 speed_C
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MotorCommand(null);
    if (msg.speed_B !== undefined) {
      resolved.speed_B = msg.speed_B;
    }
    else {
      resolved.speed_B = 0.0
    }

    if (msg.speed_C !== undefined) {
      resolved.speed_C = msg.speed_C;
    }
    else {
      resolved.speed_C = 0.0
    }

    return resolved;
    }
};

module.exports = MotorCommand;
