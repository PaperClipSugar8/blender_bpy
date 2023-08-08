import bpy
import numpy as np





cube_4d = [     [1, 1, 1, 1],
                [1, 1, 1, -1],
                [1, 1, -1, 1],
                [1, 1, -1, -1],
                [1, -1, 1, 1],
                [1, -1, 1, -1],
                [1, -1, -1, 1],
                [1, -1, -1, -1],
                [-1, 1, 1, 1],
                [-1, 1, 1, -1],
                [-1, 1, -1, 1],
                [-1, 1, -1, -1],
                [-1, -1, 1, 1],
                [-1, -1, 1, -1],
                [-1, -1, -1, 1],
                [-1, -1, -1, -1]
            ]
            

projection = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0]
]

def hyper_cube():
    mesh = bpy.data.meshes.new("4d cube")
    vertices = [np.matmul(projection, v) for v in cube_4d]
    edges = []
    faces = [[0, 1, 3, 2], [12, 13, 15, 14], [0, 1, 5, 4], [10, 11, 15, 14], [0, 2, 6, 4],
             [9, 11, 15, 13], [0, 1, 9, 8], [6, 7, 15, 14], [0, 2, 10, 8], [5, 7, 15, 13],
             [0, 4, 12, 8], [3, 7, 15, 11], [4, 5, 7, 6], [8, 9, 11, 10], [2, 3, 7, 6],
             [8, 9, 13, 12], [1, 3, 7, 5], [8, 10, 14, 12], [2, 3, 11, 10], [4, 5, 13, 12],
             [1, 3, 11, 9], [4, 6, 14, 12], [1, 5, 13, 9], [2, 6, 14, 10]]
    mesh.from_pydata(vertices, edges, faces)
    return bpy.data.objects.new("Custom Object", mesh)




scene = bpy.data.scenes['Scene']
scene.frame_start = 0
scene.frame_end = 100


obj = hyper_cube()
bpy.context.scene.collection.objects.link(obj)
verts = obj.data.vertices

'''
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0), scale=(1, 1, 1))

cube = bpy.data.objects["Cube"]
verts = cube.data.vertices
'''

for index, v in enumerate(verts):
    
    angle = 0
    for frame in range(scene.frame_start, scene.frame_end):
        
        angle += 0.0005
        rZW = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, np.cos(angle), -np.sin(angle)],
                [0, 0, np.sin(angle),  np.cos(angle)]]
                
        rXW = [
                [np.cos(angle), 0, 0, -np.sin(angle)],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [np.sin(angle), 0, 0, np.cos(angle)]]
                
        rotation = np.matmul(rZW, rXW)
        cube_4d[index] = np.matmul(rotation, cube_4d[index])
        v.co = np.matmul(projection, cube_4d[index])
        
        
        
        
        
        
        
        
        
        
        v.keyframe_insert("co", frame = scene.frame_start + frame)
