import open3d as o3d
import numpy as np
def read_pcd(file_path):
	pcd = o3d.io.read_point_cloud(file_path)
	print(np.asarray(pcd.points))
	colors = np.asarray(pcd.colors) * 255
	points = np.asarray(pcd.points)
	print(points.shape, colors.shape)
	return np.concatenate([points, colors], axis=-1)
	
	
a=read_pcd('a1.pcd')

print(a)

a1=read_pcd('a.pcd')

print(a1)

