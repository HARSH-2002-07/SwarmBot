#!/usr/bin/env python3
import time
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration

def main():
    rclpy.init()
    navigator = BasicNavigator()

    # Wait for Nav2 to be fully ready
    print("Waiting for Navigation to start...")
    navigator.waitUntilNav2Active()

    # --- DEFINE WAREHOUSE WAYPOINTS ---
    goal_poses = []
    
    # Waypoint 1: Top Right Corner (Approx)
    goal_pose1 = PoseStamped()
    goal_pose1.header.frame_id = 'map'
    goal_pose1.header.stamp.sec = 0  # <--- CHANGE TO THIS
    goal_pose1.pose.position.x = 5.0
    goal_pose1.pose.position.y = 5.0
    goal_pose1.pose.orientation.w = 1.0
    goal_poses.append(goal_pose1)

    # Waypoint 2: Bottom Left Corner (Approx)
    goal_pose2 = PoseStamped()
    goal_pose2.header.frame_id = 'map'
    goal_pose2.header.stamp.sec = 0  # <--- CHANGE TO THIS
    goal_pose2.pose.position.x = -5.0
    goal_pose2.pose.position.y = -5.0
    goal_pose2.pose.orientation.w = 1.0
    goal_poses.append(goal_pose2)

    # Waypoint 3: Back to Center (Home)
    goal_pose3 = PoseStamped()
    goal_pose3.header.frame_id = 'map'
    goal_pose3.header.stamp.sec = 0  # <--- CHANGE TO THIS
    goal_pose3.pose.position.x = 0.0
    goal_pose3.pose.position.y = 0.0
    goal_pose3.pose.orientation.w = 1.0
    goal_poses.append(goal_pose3)

    # --- EXECUTE PATROL ---
    print(f"Starting Warehouse Patrol with {len(goal_poses)} stops.")

    for i, goal in enumerate(goal_poses):
        print(f"Driving to Waypoint {i+1}...")
        navigator.goToPose(goal)

        while not navigator.isTaskComplete():
            # Minimal feedback so we don't spam the terminal
            pass

        # Check result
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"Waypoint {i+1} reached!")
        else:
            print(f"Waypoint {i+1} failed with code: {result}")
            # navigator.cancelTask() # Optional: cancel if stuck

    print("Patrol Complete! Returning to base.")
    rclpy.shutdown()

if __name__ == '__main__':
    main()