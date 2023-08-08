import numpy as np
import bpy

RES = 9
RAD = 1


def get_3d_index(dim1, dim2, dim3, index):
    i = index // (dim2 * dim3)
    index -= i * (dim2 * dim3)
    j = index // dim3
    k = index % dim3
    return (i, j, k)

def get_1d_index(i, j, k, dimensions=(RES, RES, RES)):
    x, y, z = dimensions
    return i * y * z + j * z + k

projection = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
]


scene = bpy.data.scenes['Scene']
scene.frame_start = 0
scene.frame_end = 64

ste1 = 2*np.pi / (RES-1)
ste2 = np.pi / (RES-1)
theta = np.arange(0, 2*np.pi + ste1, ste1, dtype=np.float16)
alpha = np.arange(0, np.pi + ste2, ste2, dtype=np.float16)
beta = alpha.copy()
    
# 3d structure that contains every vertex coordinates of the sphere
vec = lambda t, a, b: [RAD * np.cos(t) * np.sin(a) * np.sin(b), RAD * np.sin(t) * np.sin(a) * np.sin(b), RAD * np.cos(a) * np.sin(b), RAD * np.cos(b)]
vertex = [vec(t, a, b) for b in beta for a in alpha for t in theta]


def hyper_sphere():
    mesh = bpy.data.meshes.new("4d cube")
    vertices = [np.matmul(projection, v) for v in vertex]
    edges = []
    # faces as tuples of vertices to be connected in a clockwise order
    faces = []
    for i in range(RES-1):
        for j in range(RES-1):
            for k in range(RES-1):
                faces.append([  get_1d_index(i, j, k),
                                get_1d_index(i+1, j, k),
                                get_1d_index(i+1, j+1, k),
                                get_1d_index(i+1, j+1, k+1),
                                get_1d_index(i+1, j, k+1),
                                get_1d_index(i, j, k+1),
                                get_1d_index(i, j+1, k+1),
                                get_1d_index(i, j+1, k)])
                                
    mesh.from_pydata(vertices, edges, faces)
    return bpy.data.objects.new("Custom Object", mesh)


obj = hyper_sphere()
bpy.context.scene.collection.objects.link(obj)
verts = obj.data.vertices

steps_angle = np.arange(0, np.pi, np.pi / (scene.frame_end - scene.frame_start))



for index, v in enumerate(verts):

    angle = 0
    for frame in range(scene.frame_start, scene.frame_end):


        rZW = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, np.cos(angle), -np.sin(angle)],
                [0, 0, np.sin(angle),  np.cos(angle)]]
        
        rXY = [
                [np.cos(angle), -np.sin(angle), 0, 0],
                [np.sin(angle),  np.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
        
        rYW = [
                [1, 0, 0, 0],
                [0, np.cos(angle), 0, -np.sin(angle)],
                [0, 0, 1, 0],
                [0, np.sin(angle), 0, np.cos(angle)]]
        
        rotation = np.matmul(rZW, np.matmul(rXY, rYW))
        ram = np.matmul(rotation, vertex[index])
        
        w = 1 / (3/2 - ram[-1])
        projection = [
                        [w, 0, 0, 0],
                        [0, w, 0, 0],
                        [0, 0, w, 0]
        ]
        
        
        v.co = np.matmul(projection, ram)
        
        angle = steps_angle[frame]
        
        v.keyframe_insert("co", frame = scene.frame_start + frame)
        
        
