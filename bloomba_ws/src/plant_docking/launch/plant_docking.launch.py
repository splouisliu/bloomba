
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    """

    This function launches 4 nodes at the same time.
    - turtlesim: this is the simulation environment of the two turtles
    - plant_docking -> turtle_tf2_broadcaster -> broadcaster1:
    - plant_docking -> turtle_tf2_broadcaster -> broadcaster2:
    - plant_docking -> turtle_tf2_listener:

    It also does DeclareLaunchArgument (whatever that means)
    """
    return LaunchDescription([
        
        Node(
            package='plant_docking',
            executable='plant_tf2_broadcaster',
            name='broadcaster1',
            parameters=[
                {'plantname': 'plant_num1'}
            ]
        ),
        DeclareLaunchArgument(
            'target_frame', default_value='camera',
            description='Target frame name.'
        ),
        # Node(
        #     package='plant_docking',
        #     executable='turtle_tf2_broadcaster',
        #     name='broadcaster2',
        #     parameters=[
        #         {'turtlename': 'turtle2'}
        #     ]
        # ),
        Node(
            package='plant_docking',
            executable='plant_tf2_listener',
            name='listener',
            parameters=[
                {'target_frame': LaunchConfiguration('target_frame')}
            ]
        ),
    ])