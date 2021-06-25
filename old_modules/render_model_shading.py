from math import radians, sin, cos, pi
import mathutils, bpy, argparse, random, time, os,logging
import tqdm


def generate_rand(a=0, b=1, only_positive=False):
	x = (random.random()-0.5) * 2*b
	if abs(x) < a or (only_positive and x<0):
		return generate_rand(a, b, only_positive)
	else:
		return x

def point_at(obj, target, roll=0):
	"""
	Rotate obj to look at target

	:arg obj: the object to be rotated. Usually the camera
	:arg target: the location (3-tuple or Vector) to be looked at
	:arg roll: The angle of rotation about the axis from obj to target in radians.

	Based on: https://blender.stackexchange.com/a/5220/12947 (ideasman42)
	"""
	if not isinstance(target, mathutils.Vector):
		target = mathutils.Vector(target)
	loc = obj.location
	# direction points from the object to the target
	direction = target - loc

	quat = direction.to_track_quat('-Z', 'Y')

	# /usr/share/blender/scripts/addons/add_advanced_objects_menu/arrange_on_curve.py
	quat = quat.to_matrix().to_4x4()
	rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

	# remember the current location, since assigning to obj.matrix_world changes it
	loc = loc.to_tuple()
	obj.matrix_world = quat * rollMatrix
	obj.location = loc

# init & params
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
random.seed(time.time())

light_num_low, light_num_high = 6, 12
light_loc_low, light_loc_high = 3, 6

#context = bpy.context


# model_path = '/media/jcn/新加卷/JCN/CLOTHES/Human_model/衬衫+裙子/model_3'
# model = "model_3.obj"
# render_path = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/%08d.png"
# quat_file = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/result.txt"


root='/media/jcn/新加卷/JCN/CLOTHES/Human_model'
cloth_dirs=os.listdir(root)#
model_path_1=[]#chenshan+model_1
for dir in cloth_dirs:
	model_dirs=os.listdir(os.path.join(root,dir))#model_1,model_2
	for model in model_dirs:
		if model.endswith('zip'):
			pass
		else:
			temp=dir+'+'+model
			model_path_1.append(temp)

pbar=tqdm.tqdm(total=len(model_path_1))

model_path_1.sort()

count=0
for model in model_path_1:

	pbar.update(1)
	count+=1
	if count<10:
		continue
	path_0=model.split('+')[0]
	path_1=model.split('+')[1]
	present_path=os.path.join(os.path.join(os.path.join(root,path_0),path_1),path_1+'.obj')

	path=present_path #'/media/jcn/新加卷/JCN/CLOTHES/Human_model/衬衫+裙子/model_3/Model_3.obj'
	render_path ='/media/jcn/新加卷/JCN/CLOTHES/Results_1'
	render_path=os.path.join(render_path,str(count))#/media/jcn/新加卷/JCN/CLOTHES/Results/2
	if not os.path.exists(render_path):
		os.mkdir(render_path)
	quat_file=render_path+'/result.txt'
	model_name=path_1
	model_path=os.path.join(os.path.join(root,path_0),path_1)

	if count==10:
		bpy.data.objects['Cube'].select = True
		bpy.ops.object.delete()

	'''
	for obj in bpy.data.objects:
		if obj.name in ['Cube','Light','Camera']:
			pass
		else:
			bpy.data.objects[obj.name].select = True
			bpy.ops.object.delete()
	'''

	# rendering process
	# create a scene
	scene = bpy.context.scene

	# scene = bpy.data.scenes.new("Scene")
	if count==2:
		print('2')
		for obj in bpy.context.scene.objects:
			print(obj.name)

	context=bpy.context
	# create a camera
	camera_data = bpy.data.cameras.new("Camera")
	camera = bpy.data.objects.new("Camera", camera_data)

	distance, alpha, beta, gamma = 4.5, 1.0, 89.0, 0.0
	alpha, beta, gamma = radians(alpha), radians(beta), radians(gamma)
	camera.location = mathutils.Vector((distance*cos(beta)*cos(alpha), distance*cos(beta)*sin(alpha), distance*sin(beta)))

	point_at(camera, mathutils.Vector((0, -0.4, 0)), roll=gamma)
	print('camera by looked_at', camera.location, camera.rotation_euler, camera.rotation_euler.to_quaternion())

	scene.objects.link(camera)

	# Create lights (lights with random num in random directions)
	# light number:6~12, point light
	light_num = random.randint(a=light_num_low, b=light_num_high)
	print('create %d light(s) at:', light_num)
	for idx in range(light_num):
		light_data = bpy.data.lamps.new('light'+str(idx), type='POINT')
		light = bpy.data.objects.new('light'+str(idx), light_data)
		light_loc = (generate_rand(light_loc_low, light_loc_high), generate_rand(light_loc_low, light_loc_high), generate_rand(light_loc_low, light_loc_high, True))
		light.location = mathutils.Vector(light_loc)
		scene.objects.link(light)

	if count==1:
		light_data = bpy.data.lamps.new('light', type='POINT')
		light = bpy.data.objects.new('light', light_data)
		light.location = mathutils.Vector((0, 0, 8))
		scene.objects.link(light)

	scene.update()
	scene.render.resolution_x = 2048
	scene.render.resolution_y = 2048
	scene.render.resolution_percentage = 100
	scene.render.alpha_mode = 'TRANSPARENT'

	scene.camera = camera

	# make a new scene with cam and lights linked
	context.screen.scene = scene
	bpy.ops.scene.new(type='LINK_OBJECTS')
	context.scene.name = model_path
	cams = [c for c in context.scene.objects if c.type == 'CAMERA']
	print(cams)

	bpy.context.scene.use_nodes = True
	tree = bpy.context.scene.node_tree
	links = tree.links
	bpy.context.scene.render.image_settings.color_depth = '8'
	bpy.context.scene.render.image_settings.color_mode = 'RGB'

	# Clear default nodes
	for n in tree.nodes:
		tree.nodes.remove(n)

	# 必须设置，否则无法输出法向
	bpy.context.scene.render.layers['RenderLayer'].use_pass_normal = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_color = True
	# bpy.context.scene.render.layers["RenderLayer"].use_pass_diffuse = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_combined = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_z = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_ambient_occlusion = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_diffuse_direct = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_diffuse_indirect = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_diffuse_color = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_glossy_direct = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_glossy_indirect = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_glossy_color = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_transmission_direct = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_transmission_indirect = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_transmission_color = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_subsurface_direct = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_subsurface_indirect = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_subsurface_color = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_emit = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_environment = True
	bpy.context.scene.render.layers["RenderLayer"].use_pass_normal = True
	bpy.context.scene.render.image_settings.file_format = 'PNG'

	# Create input render layer node.
	render_layers = tree.nodes.new('CompositorNodeRLayers')

	print(render_layers.outputs.keys())

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

	# Remap as other types can not represent the full range of depth.
	depth_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	depth_file_output.label = 'Depth Output'
	map = tree.nodes.new(type="CompositorNodeMapValue")
	# Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
	map.offset = [-0.7]
	map.size = [0.1]
	map.use_min = True
	map.min = [0]
	links.new(render_layers.outputs['Depth'], map.inputs[0])
	links.new(map.outputs[0], depth_file_output.inputs[0])

	# image_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	# image_file_output.label = 'Image'
	# links.new(render_layers.outputs['Image'], image_file_output.inputs[0])
	#print('image_idx: %08d, camera: (%.3f,%.3f,%.3f)' % (image_idx, a * 180. /pi, b * 180. / pi, g * 180. / pi))

	albedo_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	albedo_file_output.label = 'Albedo Output'
	links.new(render_layers.outputs['Color'], albedo_file_output.inputs[0])

	shading_add = tree.nodes.new(type="CompositorNodeMixRGB")
	shading_add.blend_type = 'ADD'

	direct_file_output=tree.nodes.new(type="CompositorNodeOutputFile")
	direct_file_output.label='Direct Output'
	links.new(render_layers.outputs['DiffDir'], shading_add.inputs[1])

	# in_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	# in_file_output.label = 'In'
	# links.new(render_layers.outputs['DiffDir'], in_file_output.inputs[0])

	indirect_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	indirect_file_output.label = 'INDirect Output'
	links.new(render_layers.outputs['DiffInd'], shading_add.inputs[2])

	shading_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
	shading_file_output.label = 'Shading Output'
	links.new(shading_add.outputs[0], shading_file_output.inputs[0])


	# import model
	bpy.ops.import_scene.obj(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl") #-Z, Y

	# print('scene objects:')
	for o in bpy.context.scene.objects:
		print(o.name)

	for obj in context.scene.objects:
		if obj.name in ['Camera','Lamp','light',model_name]:
			obj.location = mathutils.Vector((0, 0, -2.0))
			obj.scale = mathutils.Vector((0.002, 0.002, 0.002))


	c = cams[0]

	scene = bpy.context.scene

	#scene = bpy.context.scene
	f_quat = open(quat_file, 'w')
	image_idx = 0
	for g in [0]:
		g = radians(float(g))
		for b in [20, -20]:
			b =  radians(float(b))
			for a in range(1, 360, 60):
				a = radians(float(a))
				c.location = mathutils.Vector((distance*cos(b)*cos(a), distance*cos(b)*sin(a), distance*sin(b)))
				point_at(c, mathutils.Vector((0, -0.4, 0)), roll = g)
				quat = c.rotation_euler.to_quaternion()

				for output_node in [normal_file_output, depth_file_output,albedo_file_output,shading_file_output]:
					output_node.base_path = ''

				scene.render.filepath = render_path+'/image_%03d' % image_idx
				# image_file_output.file_slots[0].path = '/media/jcn/新加卷/JCN/CLOTHES/Results/2/image%d' % image_idx
				normal_file_output.file_slots[0].path = render_path+'/normal_%03d' % image_idx
				depth_file_output.file_slots[0].path = render_path+'/depth_%03d' % image_idx
				albedo_file_output.file_slots[0].path = render_path+'/albedo_%03d' % image_idx
				shading_file_output.file_slots[0].path = render_path+'/shading_%03d' % image_idx
				# in_file_output.file_slots[0].path = render_path+'/in_%03d' % image_idx

				bpy.ops.render.render(use_viewport=True,write_still=True)

				#context.scene.render.filepath = render_path % image_idx
				f_quat.write('%08d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (image_idx, quat[0], quat[1], quat[2], quat[3], a * 180 /pi, b * 180 / pi, g * 180 / pi))
				image_idx = image_idx + 1

	f_quat.close()
	for obj in bpy.context.scene.objects:
		print(obj.name)
	print(path)

	bpy.data.objects[model_name].select = True
	bpy.ops.object.delete()
	for obj in bpy.context.scene.objects:
		if obj.name in ['Lamp', 'Camera','light']:
			obj.select=False
		else:
			obj.select=True
	bpy.ops.object.delete()
	break


