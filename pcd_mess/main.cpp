#include <iostream>
#include <cstring>
#include <pcl/io/pcd_io.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>


bool LoadPCD(std::string filename,  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud)
{

    if (pcl::io::loadPCDFile<pcl::PointXYZ>(filename, *cloud) == -1)
    {
      std::cout<< "can't read file " << filename << std::endl;
      return (-1);
    }
}



int main(int argc, char **argv) {
    std::cout << "Hello, world!" << std::endl;
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_source(new pcl::PointCloud<pcl::PointXYZ>);

    //std::string filename = "/home/oem/lg/project/centerpoint_pro/python_center_point/pcd_data/show/temp1/a.pcd";
    std::string filename = "../a.pcd";
//        std::string filename = "../table_scene_lms400.pcd";

    LoadPCD(filename, cloud_source);
    std::cout << "PointCloud_source  has: " << cloud_source->points.size () << " data points." << std::endl;

    pcl::PCDWriter writer;
    std::stringstream ss;
    //ss << "/home/oem/lg/project/centerpoint_pro/python_center_point/pcd_data/show/temp1/a1.pcd";
    ss << "../a1.pcd";
    writer.write<pcl::PointXYZ> (ss.str (), *cloud_source, false); //*
    return 0;
}
