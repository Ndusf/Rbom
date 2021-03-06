// Generated by gencpp from file robm_nxt/MotorCommand.msg
// DO NOT EDIT!


#ifndef ROBM_NXT_MESSAGE_MOTORCOMMAND_H
#define ROBM_NXT_MESSAGE_MOTORCOMMAND_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace robm_nxt
{
template <class ContainerAllocator>
struct MotorCommand_
{
  typedef MotorCommand_<ContainerAllocator> Type;

  MotorCommand_()
    : speed_B(0.0)
    , speed_C(0.0)  {
    }
  MotorCommand_(const ContainerAllocator& _alloc)
    : speed_B(0.0)
    , speed_C(0.0)  {
  (void)_alloc;
    }



   typedef float _speed_B_type;
  _speed_B_type speed_B;

   typedef float _speed_C_type;
  _speed_C_type speed_C;





  typedef boost::shared_ptr< ::robm_nxt::MotorCommand_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::robm_nxt::MotorCommand_<ContainerAllocator> const> ConstPtr;

}; // struct MotorCommand_

typedef ::robm_nxt::MotorCommand_<std::allocator<void> > MotorCommand;

typedef boost::shared_ptr< ::robm_nxt::MotorCommand > MotorCommandPtr;
typedef boost::shared_ptr< ::robm_nxt::MotorCommand const> MotorCommandConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::robm_nxt::MotorCommand_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::robm_nxt::MotorCommand_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::robm_nxt::MotorCommand_<ContainerAllocator1> & lhs, const ::robm_nxt::MotorCommand_<ContainerAllocator2> & rhs)
{
  return lhs.speed_B == rhs.speed_B &&
    lhs.speed_C == rhs.speed_C;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::robm_nxt::MotorCommand_<ContainerAllocator1> & lhs, const ::robm_nxt::MotorCommand_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace robm_nxt

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::robm_nxt::MotorCommand_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::robm_nxt::MotorCommand_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robm_nxt::MotorCommand_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robm_nxt::MotorCommand_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robm_nxt::MotorCommand_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robm_nxt::MotorCommand_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::robm_nxt::MotorCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9ba6bdab22f53c19b2150f8a9af566e0";
  }

  static const char* value(const ::robm_nxt::MotorCommand_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9ba6bdab22f53c19ULL;
  static const uint64_t static_value2 = 0xb2150f8a9af566e0ULL;
};

template<class ContainerAllocator>
struct DataType< ::robm_nxt::MotorCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "robm_nxt/MotorCommand";
  }

  static const char* value(const ::robm_nxt::MotorCommand_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::robm_nxt::MotorCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 speed_B \n"
"float32 speed_C\n"
;
  }

  static const char* value(const ::robm_nxt::MotorCommand_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::robm_nxt::MotorCommand_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.speed_B);
      stream.next(m.speed_C);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MotorCommand_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::robm_nxt::MotorCommand_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::robm_nxt::MotorCommand_<ContainerAllocator>& v)
  {
    s << indent << "speed_B: ";
    Printer<float>::stream(s, indent + "  ", v.speed_B);
    s << indent << "speed_C: ";
    Printer<float>::stream(s, indent + "  ", v.speed_C);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROBM_NXT_MESSAGE_MOTORCOMMAND_H
