cmake_minimum_required(VERSION 3.5)
project(bin2pcd)
 
find_package(PCL 1.2 REQUIRED)
 
# 加入Boost setting
find_package(Boost COMPONENTS program_options REQUIRED )
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})
 
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
 
add_executable(bin2pcd bin2pcd.cpp)
 
target_link_libraries (bin2pcd ${PCL_LIBRARIES} ${Boost_LIBRARIES}) #此处也有修改
 
install(TARGETS bin2pcd RUNTIME DESTINATION bin)

