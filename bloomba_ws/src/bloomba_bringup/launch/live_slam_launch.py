import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

"""
Launches the following:
 - Sensors
 - Scan filters
 - Nav2 components:
    - Localization
    - Navigation
"""


def generate_launch_description():
    # Get the launch directory
    slam_dir = get_package_share_directory('bloomba_slam')
    slam_launch_dir = os.path.join(slam_dir, 'launch')

    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params_file = LaunchConfiguration('slam_params_file')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(slam_dir, 'config', 'mapper_params_online_async.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    # Specify the actions
    bringup_cmd_group = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('bloomba_bringup'), 'launch'),
                '/sensors_launch.py'])
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('bloomba_bringup'), 'launch'),
                '/laser_filters_launch.py'])
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(slam_launch_dir, 'online_async_launch.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time,
                              'slam_params_file': slam_params_file}.items()),
    ])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_params_file_cmd)

    # Add the actions to launch all of the navigation nodes
    ld.add_action(bringup_cmd_group)

    return ld
