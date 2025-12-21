cmake_minimum_required(VERSION 3.8)
project(swarm_robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# --- START OF INSTALL RULES ---

# 1. Install the URDF directory (Crucial for the robot model)
install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# 2. Install the Meshes directory (Crucial for 3D visuals)
install(
  DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
)

# 3. Install the Launch directory
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# 4. Install the RViz directory
install(
  DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}
)

# --- END OF INSTALL RULES ---

ament_package()