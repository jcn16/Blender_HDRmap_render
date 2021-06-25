import bpy
import os,sys
sys.path.append('//')
import xiuminglib as xm


tx = 0.0
ty = 0.0
tz = -5.0

rx = 180.0
ry = 0.0
rz = 0.0


pi = 3.14159265

# init & params

context = bpy.context

model_path = '/media/jcn/新加卷/JCN/CLOTHES/Human_model/衬衫裙子/model_3'
model = "model_3.obj"
render_path = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/%08d.png"
quat_file = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/result.txt"



# create a scene


camera = bpy.data.objects['Camera']

# Set camera rotation in euler angles
camera.rotation_mode = 'XYZ'
camera.rotation_euler[0] = rx*(pi/180.0)
camera.rotation_euler[1] = ry*(pi/180.0)
camera.rotation_euler[2] = rz*(pi/180.0)

# Set camera translation
camera.location.x = tx
camera.location.y = ty
camera.location.z = tz

bpy.context.scene.use_nodes = True
xm.blender.render.set_cycles(w=1024, h=1024)

tree = bpy.context.scene.node_tree
links = tree.links
bpy.context.scene.render.image_settings.color_depth = '8'
bpy.context.scene.render.image_settings.color_mode = 'RGB'

# 必须设置，否则无法输出法向
bpy.context.scene.render.layers['RenderLayer'].use_pass_normal = True

# Clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

# Create input render layer node.
render_layers = tree.nodes.new('CompositorNodeRLayers')

scale_normal = tree.nodes.new(type="CompositorNodeMixRGB")
scale_normal.blend_type = 'MULTIPLY'
scale_normal.inputs[2].default_value = (0.5, 0.5, 0.5, 1)
links.new(render_layers.outputs['Normal'], scale_normal.inputs[1])
bias_normal = tree.nodes.new(type="CompositorNodeMixRGB")
bias_normal.blend_type = 'ADD'
bias_normal.inputs[2].default_value = (0.5, 0.5, 0.5, 0)
links.new(scale_normal.outputs[0], bias_normal.inputs[1])
normal_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
normal_file_output.label = 'Normal Output'
links.new(bias_normal.outputs[0], normal_file_output.inputs[0])

image_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
image_file_output.label = 'Image'
links.new(render_layers.outputs['Image'], image_file_output.inputs[0])


scene = bpy.context.scene
# 设置输出分辨率，可以自行修改
scene.render.resolution_x = 300
scene.render.resolution_y = 200

scene.render.resolution_percentage = 100
cam = scene.objects['Camera']

# import model
path = os.path.join(model_path, model)
bpy.ops.import_scene.obj(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl") #-Z, Y

# fov
cam.data.angle = 10*(3.1415926/180.0)
bpy.context.scene.render.image_settings.file_format = 'PNG'

for output_node in [normal_file_output, image_file_output]:
    output_node.base_path = ''

# 输出路径
scene.render.filepath = '/media/jcn/新加卷/JCN/CLOTHES/Results'
normal_file_output.file_slots[0].path = scene.render.filepath + 'normal_'
image_file_output.file_slots[0].path = scene.render.filepath + 'image_'

xm.blender.scene.save_blend('./blender_1.blend')

bpy.ops.render.render()
