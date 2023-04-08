from rosidl_runtime_py import set_message_fields, message_to_ordereddict
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped, Pose
import rclpy
import json

initial_pose_dict = {
    "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
    },
    "orientation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "w": 1.0,
    },
}

waypoints = [
    {
        "position": {                   # Main room
            "x": -3.58,
            "y": 4.62,
            "z": 0.0,
        },
        "orientation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "w": 1.0,
        },
    },
    {
        "position": {                   # Big room
            "x": 1.91,
            "y": 5.82,
            "z": 0.0,
        },
        "orientation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "w": 1.0,
        },
    },
    {
        "position": {                   # Back room
            "x": -6.04,
            "y": -6.39,
            "z": 0.0,
        },
        "orientation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "w": 1.0,
        },
    },
]


def main():
    rclpy.init()
    navigator = BasicNavigator()

    # Set initial pose of robot
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    set_message_fields(initial_pose.pose, initial_pose_dict)
    navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate, since autostarting nav2
    navigator.waitUntilNav2Active()

    # INSERT UNDOCKING CODE
    pass


    for i, waypoint_pose_dict in enumerate(waypoints):
        # Navigate to a waypoint (goToPose is async)
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        set_message_fields(goal_pose.pose, waypoint_pose_dict)
        navigator.goToPose(goal_pose)

        # Feedback
        j=0
        while not navigator.isTaskComplete():
            j=j+1
            feedback = navigator.getFeedback()

            if feedback and j % 5 ==0:
                print(f'Executing current waypoint: {i+1}/{len(waypoints)}')

        # INSERT DOCKING AND FLOWERING CODE
        pass

    # Exit
    navigator.lifecycleShutdown()

    exit(0)


if __name__ == '__main__':
    main()