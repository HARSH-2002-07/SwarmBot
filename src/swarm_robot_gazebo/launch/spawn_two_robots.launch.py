import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_swarm_gazebo = get_package_share_directory('swarm_robot_gazebo')
    pkg_swarm_description = get_package_share_directory('swarm_robot_description')

    # Fix for missing meshes
    ign_resource_path = AppendEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=os.path.join(pkg_swarm_description, '..')
    )

    world_file = os.path.join(pkg_swarm_gazebo, 'worlds', 'warehouse.sdf')
    urdf_file = os.path.join(pkg_swarm_description, 'urdf', 'turtlebot3_waffle_pi.urdf')
    
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Start Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_file]}.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_desc}],
    )

    # Spawn Robot 1 (Immediate)
    spawn_bot1 = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'bot1',
            '-topic', 'robot_description', 
            '-x', '-3.0', '-y', '0.0', '-z', '0.5',
        ],
        output='screen'
    )

    # Spawn Robot 2 (Delayed by 5 seconds)
    # This prevents the graphics driver from crashing!
    spawn_bot2_event = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-name', 'bot2',
                    '-topic', 'robot_description', 
                    '-x', '3.0', '-y', '0.0', '-z', '0.5',
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        ign_resource_path,
        gazebo,
        robot_state_publisher,
        spawn_bot1,
        spawn_bot2_event # <--- Now using the delayed version
    ])