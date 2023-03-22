# Bloomba: An Autonomous Plant Watering Robot for The Office

<div align="center">
    <a align="center">
        <img alt="photo" src="pics/photo.jpg" width="40%" hspace="15"></img>
        <img alt="cad" src="pics/cad.png" width="33%" height="30%"></img>
    </a>
</div>


## ROS2 Commands
### Basics

Build (on PC):
```
rosdep install --from-path src -yi
colcon build --symlink-install
```

Build (on live robot):
```
rosdep install --from-path src/bloomba_bringup src/bloomba_navigation src/bloomba_slam -yi
colcon build --symlink-install --packages-select bloomba_bringup bloomba_navigation bloomba_slam
```

Source:

`source install/local_setup.bash`


### Bringup commands

Run SLAM bringup (on PC):

`ros2 launch bloomba_bringup sim_slam_launch.py`

Run navigation bringup (on PC):

`ros2 launch bloomba_bringup sim_nav_launch.py`

Run SLAM bringup (on live robot):

`ros2 launch bloomba_bringup live_slam_launch.py`

Run navigation bringup (on live robot):

`ros2 launch bloomba_bringup live_nav_launch.py`


### Standalone Commands

Run sim (on PC):

`ros2 launch irobot_create_gazebo_bringup create3_gazebo_office.launch.py use_rviz:=false spawn_dock:=false`

Run lidar (on live robot):
`ros2 launch bloomba_bringup sensors_launch.py`

Run laser filters:

`ros2 launch bloomba_bringup laser_filters_launch.py`

Run teleop:

`ros2 run teleop_twist_keyboard teleop_twist_keyboard`

Run slam:

`ros2 launch bloomba_slam online_async_launch.launch.py`

Run rviz:

`ros2 launch bloomba_bringup rviz_launch.py`

Run navigation:

`ros2 launch bloomba_navigation bringup_launch.py map:="maps/map_office_sim.yaml"`

Run rosbridge:

`ros2 launch rosbridge_server rosbridge_websocket_launch.xml`

Visualize TF:

`ros2 run tf2_tools view_frames`
