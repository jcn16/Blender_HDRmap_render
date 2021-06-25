from math import radians, sin, cos, pi
import mathutils, bpy, argparse, random, time, os,logging


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

context = bpy.context

model_path = '/media/jcn/新加卷/JCN/CLOTHES/Human_model/衬衫+裙子/model_3'
model = "model_3.obj"
render_path = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/%08d.png"
quat_file = "/media/jcn/新加卷/JCN/CLOTHES/Results/2/result.txt"
# model_path = "C:\\Users\\Admin\\Desktop\\CLOTHES\\Human_model\\衬衫+裙子"
# model = "model_1.obj"
# render_path ='C:\\Users\\Admin\\Desktop\\CLOTHES\\Results'
# quat_file = "C:\\Users\\Admin\\Desktop\\CLOTHES\\Results\\result.txt"


# create a scene
scene = bpy.data.scenes.new("Scene")

# create a camera
camera_data = bpy.data.cameras.new("Camera")
camera = bpy.data.objects.new("Camera", camera_data)

distance, alpha, beta, gamma = 4.0, 1.0, 89.0, 0.0
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

light_data = bpy.data.lamps.new('light', type='POINT')
light = bpy.data.objects.new('light', light_data)
light.location = mathutils.Vector((0, 0, 8))
scene.objects.link(light)

# rendering process
scene.update()

scene.render.resolution_x = 2048
scene.render.resolution_y = 2048
scene.render.resolution_percentage = 100

scene.camera = camera
path = os.path.join(model_path, model)

# make a new scene with cam and lights linked
context.screen.scene = scene
bpy.ops.scene.new(type='LINK_OBJECTS')
context.scene.name = model_path
cams = [c for c in context.scene.objects if c.type == 'CAMERA']
print(cams)

# import model
bpy.ops.import_scene.obj(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl") #-Z, Y

print('scene objects:')
for o in context.scene.objects:
	print(o)
for obj in context.scene.objects:
	if obj.name in ['Camera.001'] + ['light'+str(idx) for idx in range(light_num)]:
		continue
	else:
		obj.location = mathutils.Vector((0, 0, -2.0))
		obj.scale = mathutils.Vector((0.002, 0.002, 0.002))


c = cams[0]

bpy.context.scene.render.image_settings.file_format = 'PNG'

f_quat = open(quat_file, 'w')
image_idx = 0
for g in [0]:
	g = radians(float(g))
	for b in [40, -20]:
		b =  radians(float(b))
		for a in range(1, 360, 60):
			a = radians(float(a))
			
			c.location = mathutils.Vector((distance*cos(b)*cos(a), distance*cos(b)*sin(a), distance*sin(b)))
			point_at(c, mathutils.Vector((0, -0.4, 0)), roll = g)
			quat = c.rotation_euler.to_quaternion()
			#print('image_idx: %08d, camera: (%.3f,%.3f,%.3f)' % (image_idx, a * 180. /pi, b * 180. / pi, g * 180. / pi))
			context.scene.render.filepath = render_path % image_idx
			bpy.ops.render.render(use_viewport = True, write_still=True)
			f_quat.write('%08d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (image_idx, quat[0], quat[1], quat[2], quat[3], a * 180 /pi, b * 180 / pi, g * 180 / pi))
			image_idx = image_idx + 1
			
f_quat.close()
