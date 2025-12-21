import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Get the path to the URDF file
    pkg_share = get_package_share_directory('swarm_robot_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'turtlebot3_waffle_pi.urdf')

    # 2. Read the URDF file (Command lets us process xacro if needed later)
    # We use 'cat' because it's a raw URDF. If it were Xacro, we'd use 'xacro'.
    robot_desc = Command(['cat ', urdf_file])

    # 3. Define the nodes
    
    # Robot State Publisher: Publishes the TFs (transforms) of the robot
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Joint State Publisher GUI: Sliders to move wheels
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # RViz2: The Visualizer
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    # 4. Return the Launch Description
    return LaunchDescription([
        rsp_node,
        jsp_gui_node,
        rviz_node
    ])