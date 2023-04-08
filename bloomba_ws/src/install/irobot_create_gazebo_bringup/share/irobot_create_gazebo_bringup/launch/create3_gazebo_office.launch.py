#!/usr/bin/env python3
# Copyright 2021 iRobot Corporation. All Rights Reserved.
# @author Luis Enrique Chico Capistrano (lchico@irobot.com)

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, PathJoinSubstitution, LaunchConfiguration


ARGUMENTS = [
    DeclareLaunchArgument('use_rviz', default_value='true',
                          choices=['true', 'false'],
                          description='Start rviz.'),
]

# Set the robot and dock pose close to the wall by default
for pose_element, default_value in zip(['x', 'y', 'yaw'], ['0.0', '0.0', '0.0']):
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value=default_value,
                     description=f'{pose_element} component of the robot pose.'))


def generate_launch_description():
    # Directories
    office_dir = get_package_share_directory('lake_harbour_office_gazebo')
    irobot_create_gazebo_bringup_dir = get_package_share_directory('irobot_create_gazebo_bringup')

    # Paths
    create3_launch_file = PathJoinSubstitution(
        [irobot_create_gazebo_bringup_dir, 'launch', 'create3_gazebo.launch.py'])
    world_path = PathJoinSubstitution([office_dir, 'worlds', 'office.world'])
    model_path = PathJoinSubstitution([office_dir, 'models:'])

    # Launch configurations
    use_rviz = LaunchConfiguration('use_rviz')

    # Includes
    world_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([create3_launch_file]),
        launch_arguments={'world_path': world_path, 'use_rviz': use_rviz}.items())

    # Add AWS models to gazebo path
    # This environment variable needs to be set, otherwise code fails
    set_gazebo_model_path_env = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[EnvironmentVariable('GAZEBO_MODEL_PATH', default_value=''), model_path])


    # Define LaunchDescription variable
    ld = LaunchDescription(ARGUMENTS)
    # Add actions to LaunchDescription
    ld.add_action(set_gazebo_model_path_env)
    ld.add_action(world_spawn)

    return ld
