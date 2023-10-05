import bpy
import numpy as np

RES = 20

fi_width = np.pi / RES
theta_width = 2 * np.pi / RES
alpha_width = 4 * np.pi / RES

def delete_collections():
    for c in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(c)
    for c in bpy.data.collections:
        bpy.data.collections.remove(c)
        
        
def delete_materials():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

fiber_point = lambda t, f, a: np.array([np.cos(0.5*(a+f))*np.sin(0.5*t), np.sin(0.5*(a+f))*np.sin(0.5*t), 
                                        np.cos(0.5*(a-f))*np.cos(0.5*t), np.sin(0.5*(a-f))*np.cos(0.5*t)], dtype=np.float16)
stero_proj = lambda x, y, z, w: [x, y, z] if w == 1 else np.array([x, y, z], dtype=np.float16) / (1 - w)

def draw_one_fiber2(theta, fi):
  alpha = np.arange(0, 4 * np.pi + alpha_width, alpha_width, dtype=np.float16)
  vex1 = []
  for steps, alp in enumerate(alpha):
    thing = fiber_point(theta, fi, alp) 
    vex1.append(stero_proj(thing[0], thing[1], thing[2], 0.6*thing[3]))
  return np.array(vex1)



def fibers(t, f):
    mesh = bpy.data.meshes.new("Fiber")
    vertices = draw_one_fiber2(t, f).tolist()
    edges = [[i, i+1] for i in range(len(vertices)-1)]
 
    mesh.from_pydata(vertices, edges, [])
    return bpy.data.objects.new("Fiber", mesh)
        


def boundle(name: str):
    fi = np.arange(0, np.pi, fi_width, dtype=np.float16)
    theta = np.arange(0, 2 * np.pi, theta_width, dtype=np.float16)
    
    collection = bpy.data.collections.new(name=name)

    for t in theta:
        for f in fi:
            collection.objects.link(fibers(t, f))
            
    for obj in bpy.data.collections[name].all_objects:
        modifier = obj.modifiers.new(name="Skin", type='SKIN')
        for sv in obj.data.skin_vertices[0].data:
            sv.radius = (1/1000, 1/1000)
        
            

    


def over_fi(name : str, scl : int, mat):
    scene = bpy.data.scenes['Scene']
    scene.frame_start = 0
    scene.frame_end = 100
    
    step = np.pi/(scene.frame_end - scene.frame_start)
    fi = np.arange(0, np.pi, step, dtype=np.float16)
    
    
    theta = np.arange(0, 2 * np.pi, theta_width, dtype=np.float16)
    
    collection = bpy.data.collections.new(name=name)
    for angel in theta:
        collection.objects.link(fibers(angel, fi[0]))
        
    
    for obj in bpy.data.collections[name].all_objects:
        modifier = obj.modifiers.new(name=name, type='SKIN')
        
        for sv in obj.data.skin_vertices[0].data:
            sv.radius = (1/40, 1/40)
        
        obj.data.materials.append(mat)

    
    for frame in range(scene.frame_start, scene.frame_end):
        
        for index, obj in enumerate(bpy.data.collections[name].all_objects):
            if obj.type == 'MESH':
                
                new_co = draw_one_fiber2(theta[index], fi[frame])
                
                for i, v in enumerate(obj.data.vertices):
                    v.co = scl * new_co[i]
                    v.keyframe_insert("co", frame = scene.frame_start + frame)
                    


def over_theta(name : str, scl : int):
    scene = bpy.data.scenes['Scene']
    scene.frame_start = 0
    scene.frame_end = 100
    
    step = 2*np.pi/(scene.frame_end - scene.frame_start)
    
    
    theta = np.arange(0, 2*np.pi, step, dtype=np.float16)
    
    fi = np.arange(0, np.pi, fi_width, dtype=np.float16)
    
    collection = bpy.data.collections.new(name=name)
    for angle in fi:
        collection.objects.link(fibers(theta[0], angle))
    
    for obj in bpy.data.collections[name].all_objects:
        modifier = obj.modifiers.new(name="Skin", type='SKIN')
        
        for sv in obj.data.skin_vertices[0].data:
            sv.radius = (1/40, 1/40)
            
        obj.data.materials.append(mat)
        
    
    for frame in range(scene.frame_start, scene.frame_end):
        
        for index, obj in enumerate(bpy.data.collections[name].all_objects):
            if obj.type == 'MESH':
                mesh_verts = obj.data.vertices
                
                new_co = draw_one_fiber2(theta[frame], fi[index])
                
                for i, v in enumerate(mesh_verts):
                    v.co = scl * new_co[i]
                    v.keyframe_insert("co", frame = scene.frame_start + frame)
                    


def my_ma(name : str):
    mat = bpy.data.materials.new(name=f'{name}_Material')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    psdf = nodes.get("Principled BSDF")
    if psdf is None:
        psdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        psdf.location = 0,0
    psdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    psdf.inputs["Transmission"].default_value = 1.0
    psdf.inputs["Roughness"].default_value = 0.4
    return mat
    




delete_collections()
delete_materials()

over_fi('one', 1, my_ma('one'))
#over_theta('two', 1)


bpy.ops.object.collection_instance_add(collection='one', location=(0, 0, 0))

bpy.ops.object.collection_instance_add(collection='one', location=(0, 0, 0))
bpy.ops.transform.mirror(orient_matrix=((0, 0, 1), (0, 1, 0), (1, 0, 0)), constraint_axis=(True, True, True))


#bpy.ops.object.collection_instance_add(collection='two', location=(0, 0, 0))


#bpy.ops.object.collection_instance_add(collection='two', location=(0, 0, 0))
#bpy.ops.transform.mirror(orient_matrix=((-1, 0, 0), (0, -1, 0), (0, 0, -1)), constraint_axis=(True, True, False))


