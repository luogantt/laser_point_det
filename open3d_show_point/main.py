import open3d as o3d
import numpy as np

def read_pcd(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    # print(np.asarray(pcd.points))
    colors = np.asarray(pcd.colors) * 255
    points = np.asarray(pcd.points)
    # print(points.shape, colors.shape)
# 	return np.concatenate([points, colors], axis=-1)
    return points
    
	
	
a=read_pcd('b1.pcd')


#这里B已经是一个n*3的numpy.ndarray(也就是常见的数组类型)
pcd=o3d.geometry.PointCloud()#实例化一个pointcloud类
pcd.points=o3d.utility.Vector3dVector(a)#给该类传入坐标数据，此时pcd.points已经是一个点云了
o3d.visualization.draw_geometries([pcd])#显示一下


print(a)

