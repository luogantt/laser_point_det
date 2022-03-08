import numpy as np
import mayavi.mlab
 
# lidar_path换成自己的.bin文件路径
pointcloud = np.fromfile(str("n015-2018-07-18-11-07-57+0800__LIDAR_TOP__1531883537397861.pcd.bin"), dtype=np.float32, count=-1).reshape([-1, 5])
 
x = pointcloud[:, 0]  # x position of point
y = pointcloud[:, 1]  # y position of point
z = pointcloud[:, 2]  # z position of point

r = pointcloud[:, 3]  # reflectance value of point
# d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

# degr = np.degrees(np.arctan(z / d))

# vals = 'height'
# if vals == "height":
#     col = z
# else:
#     col = d

# fig = mayavi.mlab.figure(bgcolor=(0, 0, 0), size=(640, 500))
# mayavi.mlab.points3d(x, y, z,
#                      col,  # Values used for Color
#                      mode="point",
#                      colormap='spectral',  # 'bone', 'copper', 'gnuplot'
#                      # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
#                      figure=fig,
#                      )

# mayavi.mlab.show()


import time

###########################################################################

import numba

import numpy as np





@numba.jit(nopython=True)

def _points_to_voxel_reverse_kernel(

    points,

    voxel_size,

    coors_range,

    num_points_per_voxel,

    coor_to_voxelidx,

    voxels,

    coors,

    max_points=35,

    max_voxels=20000,

):

    # put all computations to one loop.

    # we shouldn't create large array in main jit code, otherwise

    # reduce performance
    # 点的数量，比如这里的bin文件有3w个点
    N = points.shape[0]
    # ndim = points.shape[1] - 1
    #数据的维度，三维的x,y,z
    ndim = 3
    #维度减去1
    ndim_minus_1 = ndim - 1
    grid_size = (coors_range[3:] - coors_range[:3]) / voxel_size
    # np.round(grid_size)
    # grid_size = np.round(grid_size).astype(np.int64)(np.int32)

    #grid_size=array([512, 512,   1]
    grid_size = np.round(grid_size, 0, grid_size).astype(np.int32)
    coor = np.zeros(shape=(3,), dtype=np.int32)
    voxel_num = 0
    failed = False

    for i in range(N):
    # for i in range(1):
        failed = False
        for j in range(ndim):
            #np.floor 向下取整 np.floor([1.9])=array([1.])
            #voxel_size= [0.2 ,0.2, 8. ]
            c = np.floor((points[i, j] - coors_range[j]) / voxel_size[j])
            # print(c)
            if c < 0 or c >= grid_size[j]:
                failed = True
                break
            coor[ndim_minus_1 - j] = c
        if failed:

            continue
        #oor_to_voxelidx.shape=(1, 512, 512)
        voxelidx = coor_to_voxelidx[coor[0], coor[1], coor[2]]
        if voxelidx == -1:
            voxelidx = voxel_num
            if voxel_num >= max_voxels:
                continue
            voxel_num += 1
            
            #这里的 voxelidx就是 voxel_num
            coor_to_voxelidx[coor[0], coor[1], coor[2]] = voxelidx
            coors[voxelidx] = coor

        #num_points_per_voxel.shape[0]=20000=max_voxels
        num = num_points_per_voxel[voxelidx]
        if num < max_points:
            voxels[voxelidx, num] = points[i]
            num_points_per_voxel[voxelidx] += 1
    return voxel_num








def points_to_voxel(

    points, voxel_size, coors_range, max_points=35, reverse_index=True, max_voxels=20000

):

    """convert kitti points(N, >=3) to voxels. This version calculate

    everything in one loop. now it takes only 4.2ms(complete point cloud)

    with jit and 3.2ghz cpu.(don't calculate other features)

    Note: this function in ubuntu seems faster than windows 10.



    Args:

        points: [N, ndim] float tensor. points[:, :3] contain xyz points and

            points[:, 3:] contain other information such as reflectivity.

        voxel_size: [3] list/tuple or array, float. xyz, indicate voxel size

        coors_range: [6] list/tuple or array, float. indicate voxel range.

            format: xyzxyz, minmax

        max_points: int. indicate maximum points contained in a voxel.

        reverse_index: boolean. indicate whether return reversed coordinates.

            if points has xyz format and reverse_index is True, output

            coordinates will be zyx format, but points in features always

            xyz format.

        max_voxels: int. indicate maximum voxels this function create.

            for second, 20000 is a good choice. you should shuffle points

            before call this function because max_voxels may drop some points.



    Returns:

        voxels: [M, max_points, ndim] float tensor. only contain points.

        coordinates: [M, 3] int32 tensor.

        num_points_per_voxel: [M] int32 tensor.
        
    max_points=35 
    reverse_index=True
    max_voxels=20000

    """
    #将voxel_size 转化成 numpy
    if not isinstance(voxel_size, np.ndarray):

        voxel_size = np.array(voxel_size, dtype=points.dtype)
    #将coors_range+ 转化成 numpy
    if not isinstance(coors_range, np.ndarray):

        coors_range = np.array(coors_range, dtype=points.dtype)

    voxelmap_shape = (coors_range[3:] - coors_range[:3]) / voxel_size

    voxelmap_shape = tuple(np.round(voxelmap_shape).astype(np.int32).tolist())
    
    # voxelmap_shape=(512, 512, 1) 
    if reverse_index:

        voxelmap_shape = voxelmap_shape[::-1]

    # don't create large array in jit(nopython=True) code.

    num_points_per_voxel = np.zeros(shape=(max_voxels,), dtype=np.int32)

    coor_to_voxelidx = -np.ones(shape=voxelmap_shape, dtype=np.int32)

    #voxels.shape=(20000, 35, 5)
    voxels = np.zeros(

        shape=(max_voxels, max_points, points.shape[-1]), dtype=points.dtype

    )
    
    #coors.shape=(20000, 3)
    coors = np.zeros(shape=(max_voxels, 3), dtype=np.int32)

    if reverse_index:

        print('我是reverse_index..')

        voxel_num = _points_to_voxel_reverse_kernel(

            points,

            voxel_size,

            coors_range,

            num_points_per_voxel,

            coor_to_voxelidx,

            voxels,

            coors,

            max_points,

            max_voxels,

        )



    else: 
        pass



    coors = coors[:voxel_num]

    voxels = voxels[:voxel_num]

    num_points_per_voxel = num_points_per_voxel[:voxel_num]



    print("这里是将cloud转成VOXEL..")

    print("/home/oem/lg/project/centerpoint_pro/python_center_point/CenterPoint1/det3d/ops/point_cloud/point_cloud_ops.py")

    return voxels, coors, num_points_per_voxel

voxel_size= [0.2 ,0.2, 8. ]
coors_range= [-51.2 ,-51.2,  -5. ,  51.2 , 51.2  , 3. ]

points=pointcloud
voxels, coors, num_points_per_voxel=points_to_voxel(points, voxel_size,coors_range)


print('voxels=',voxels)

import numpy
numpy.savetxt("voxel1.csv", voxels[0], delimiter=',')

print(voxels)















