import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_description = get_package_share_directory('swarm_robot_description')
    
    pkg_share_path = get_package_share_directory('swarm_robot_description')
    install_dir = os.path.join(pkg_share_path, '..')
    urdf_file = os.path.join(pkg_description, 'urdf', 'turtlebot3_waffle_pi.urdf')

    # 1. PROCESS XACRO (Crucial Fix!)
    # This command converts the ${namespace} variable into an empty string
    robot_desc = Command(['xacro ', urdf_file, ' namespace:=', ''])

    set_ign_resource_path = AppendEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=install_dir
    )

    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 2. SPAWN ROBOT
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_bot',
            '-string', robot_desc, 
            '-x', '0.0', '-y', '0.0', '-z', '0.1'
        ],
        output='screen'
    )

    # 3. ROBOT STATE PUBLISHER
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 4. TF BRIDGE (The "Queue Full" Fix)
    # Gazebo adds "my_bot/..." to the frame name. This node connects it back to ROS.
    # We link 'base_scan' (ROS) to 'my_bot/base_scan/lidar' (Gazebo)
    tf_bridge = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments = ['0', '0', '0', '0', '0', '0', 'base_scan', 'my_bot/base_scan/lidar']
    )

    return LaunchDescription([
        set_ign_resource_path,
        start_gazebo,
        spawn_entity,
        robot_state_publisher,
        tf_bridge
    ])