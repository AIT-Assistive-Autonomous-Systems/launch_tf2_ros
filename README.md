ROS2 [launch](https://index.ros.org/p/launch) extensions to react to transform availability.

This is particularly useful for launching rviz together with nodes publishing dynamic `/tf` after long startup times.

# example

This launch snippet runs `rviz2` as soon as a transform between map and base_link is available.

```python
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import event_named
from launch.event_handler import EventHandler
from launch_ros.actions import Node
from launch_tf2_ros.actions import TransformListener
from launch_tf2_ros.events import TimeOut, OnTransformAvailable

def generate_launch_description():
    return LaunchDescription([
        ...
        TransformListener(target_frame='base_link',
                          source_frame='map',
                          timeout=10.0),
        RegisterEventHandler(
            EventHandler(matcher=event_named(OnTransformAvailable.name),
                         entities=[Node(package='rviz2', executable='rviz2')])),
        RegisterEventHandler(
            EventHandler(matcher=event_named(TimeOut.name),
                         entities=[Shutdown(reason='transforms timeout')])),
    ])
```
