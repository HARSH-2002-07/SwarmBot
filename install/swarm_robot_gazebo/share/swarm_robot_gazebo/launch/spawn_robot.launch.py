import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Package Directories
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_description = get_package_share_directory('swarm_robot_description')
    
    # Calculate the path to the 'share' directory (where the robot description lives)
    # We go up two levels from the package directory: 
    # .../install/swarm_robot_description/share/swarm_robot_description -> .../install/swarm_robot_description/share
    install_dir = os.path.join(get_package_share_directory('swarm_robot_description'), '..')

    # 2. Path to URDF
    urdf_file = os.path.join(pkg_description, 'urdf', 'turtlebot3_waffle_pi.urdf')

    # 3. SET IGNITION RESOURCE PATH (The Fix!)
    # This tells Ignition where to look for "model://" and "package://" URIs
    set_ign_resource_path = AppendEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=install_dir
    )

    # 4. Launch Gazebo Ignition (Empty World)
    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 5. Spawn the Robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_bot',
            '-file', urdf_file,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )

    return LaunchDescription([
        set_ign_resource_path,
        start_gazebo,
        spawn_entity
    ])