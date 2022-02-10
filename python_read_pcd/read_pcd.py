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

print(a)



#第二种
def read_pcd(pcd_path):
    lines = []
    num_points = None

    with open(pcd_path, 'r') as f:
        for line in f:
            lines.append(line.strip())
            if line.startswith('POINTS'):
                num_points = int(line.split()[-1])
    assert num_points is not None

    points = []
    for line in lines[-num_points:]:
        x, y, z, i = list(map(float, line.split()))
        #这里没有把i放进去，也是为了后面 x, y, z 做矩阵变换的时候方面
        #但这个理解我选择保留， 因为可能把i放进去也不影响代码的简易程度
        points.append((np.array([x, y, z, i])))

    return points


	
a0=read_pcd('b1.pcd')
a=np.array(a0)
print(a)
#第三种
def load_pcd_to_ndarray(pcd_path):
    with open(pcd_path) as f:
        while True:
            ln = f.readline().strip()
            if ln.startswith('DATA'):
                break

        points = np.loadtxt(f)
        points = points[:, 0:4]
        return points 
a0=read_pcd('b1.pcd')
a=np.array(a0)
print(a)
#第四种（需要源码安装pypcd）链接在底部
# import argparse
# from pypcd import pypcd
# import numpy as np
# parser = argparse.ArgumentParser()
# parser.add_argument('--pcd_path', default='', type=str)
# args = parser.parse_args()

# def read_pcd(pcd_path):
#     pcd = pypcd.PointCloud.from_path(pcd_path)
#     pcd_np_points = np.zeros((pcd.points, 5), dtype=np.float32)
#     print(pcd.pc_data['x'])
#     pcd_np_points[:, 0] = np.transpose(pcd.pc_data['x'])
#     pcd_np_points[:, 1] = np.transpose(pcd.pc_data['y'])
#     pcd_np_points[:, 2] = np.transpose(pcd.pc_data['z'])
#     pcd_np_points[:, 3] = np.transpose(pcd.pc_data['intensity'])
#     pcd_np_points[:, 4] = np.transpose(pcd.pc_data['is_ground'])
    
#     del_index = np.where(np.isnan(pcd_np_points))[0]
#     pcd_np_points = np.delete(pcd_np_points, del_index, axis=0)
#     return pcd_np_points

# read_pcd(args.pcd_path)


# #第一种
# # pip3 install python-pcl
# import pcl 
# #pcd_ndarray = pcl.load(args.pcd_path).to_array()[:, :3] #不要intensity
# pcd_ndarray = pcl.load_XYZI(args.pcd_path).to_array()[:, :4]
# point_num = pcd_ndarray.shape[0] 
# # shape属性可以获取矩阵的形状（例如二维数组的行列），获取的结果是一个元组
