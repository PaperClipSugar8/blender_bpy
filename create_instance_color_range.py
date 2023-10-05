import bpy
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors

def delete_collections():
    for c in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(c)
    for c in bpy.data.collections:
        bpy.data.collections.remove(c)
        
def delete_materials():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

# starting name delete
def delete_material_givenName(name : str):
    for material in bpy.data.materials:
        if material.name.startswith(name):
            material.user_clear()
            bpy.data.materials.remove(material)

def delete_collection_givenName(name : str):
    for collection in bpy.data.collections:
        if collection.name.startswith(name):
            bpy.data.collections.remove(collection)


        
def create_cube_collection(col_name : str, color : list[np.float16]):      
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0), scale=(1, 1, 1))
    cube = bpy.context.active_object
    
    mat = bpy.data.materials.new(name=f'{col_name}_Material')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    psdf = nodes.get("Principled BSDF")
    if psdf is None:
        psdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        psdf.location = 0,0
    
    psdf.inputs["Base Color"].default_value = color
    psdf.inputs["Transmission"].default_value = 1.0
    psdf.inputs["Roughness"].default_value = 0.8
    cube.data.materials.append(mat)
    collection = bpy.data.collections.new(name=col_name)
    collection.objects.link(cube)
    bpy.ops.object.delete()
    
def create_rainbow_collection(name : str, num_col : int):
    
    delete_material_givenName(name) # reset all pervious materials with same name
    delete_collection_givenName(name) # reset all pervious collections with same name
    
    lst = np.arange(0.0, 1.0, 1.0 / num_col, dtype=np.float16)
    norm = colors.Normalize(vmin=min(lst), vmax=max(lst))
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.RdYlBu)

    for v in lst:
        create_cube_collection(f"{name}_rainbow_{v}", mapper.to_rgba(v))
    
    

    
NAME = 'bob'
COLOR_RANGE = 10
STEPS = np.arange(0.0, 1.0, 1.0 / COLOR_RANGE, dtype=np.float16)
#create_rainbow_collection(NAME, COLOR_RANGE)


scene = bpy.data.scenes['Scene']
scene.frame_start = 0
scene.frame_end = 64


WIDTH = 10
HEIGHT = 10
LENGTH = 10
RES = 5
XS, YS, ZS = WIDTH / RES, HEIGHT / RES, LENGTH / RES
world_grid = [[[np.floor(np.random.rand()+0.5) for k in range(RES+1)] for j in range(RES+1)] for i in range(RES+1)]


horizontal = np.arange(-WIDTH/2, WIDTH/2 + XS, XS, dtype=np.float16)
vertical = np.arange(-HEIGHT/2, HEIGHT/2 + YS, YS, dtype=np.float16)
orthogonal = np.arange(-LENGTH/2, LENGTH/2 + ZS, ZS, dtype=np.float16)



for i, x in enumerate(horizontal):
  for j, y in enumerate(vertical):
    for k, z in enumerate(orthogonal):
      bpy.ops.object.collection_instance_add(collection='bob_rainbow_0.0', location=(x, y, z))
      bpy.context.object.scale = (XS, YS, ZS) * np.array([world_grid[i][j][k]] * 3)
      
      for frame in range(scene.frame_start, scene.frame_end):
          bpy.context.object.scale = (XS, YS, ZS) * np.array([np.floor(np.random.rand()+0.5)]*3)
          
          bpy.context.object.keyframe_insert(data_path="scale", frame=scene.frame_start + frame)

      

        
        

        


    
#create_cube_collection("bob", (0.0, 1.0, 0.0, 0.5))
#delete_collections()
#bpy.ops.object.collection_instance_add(collection='bob', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#delete_materials()


