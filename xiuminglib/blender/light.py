"""Add functions in this module usually provide no setter for the lamp's 3D
rotation, because one usually implicitly sets the rotation by pointing the
light to an object (and specifying an up vector), by using
:func:`point_light_to`.
"""

from os.path import basename
import numpy as np

from ..imprt import preset_import
bpy = preset_import('bpy')
Vector = preset_import('Vector')

from ..log import get_logger
logger = get_logger()


def point_light_to(light, target):
    """Points the directional light to a target.

    Args:
        light (bpy_types.Object): Light object.
        target (tuple(float)): Target location to which light rays point.
    """
    target = Vector(target)

    # Point it to target
    direction = target - light.location
    # Find quaternion that rotates lamp facing direction '-Z',
    # so that it aligns with 'direction'
    # This rotation is not unique because the rotated lamp can still rotate
    # about direction vector
    # Specifying 'Y' gives the rotation quaternion with lamp's 'Y' pointing up
    rot_quat = direction.to_track_quat('-Z', 'Y')
    light.rotation_euler = rot_quat.to_euler()

    logger.info("Lamp '%s' points to %s now", light.name, target)


def add_light_sun(xyz=(0, 0, 0), rot_vec_rad=(0, 0, 0), name=None,
                  energy=1, size=0.1):
    """Adds a sun lamp that emits parallel light rays.

    Args:
        xyz (tuple(float), optional): Location only used to compute light ray
            direction.
        rot_vec_rad (tuple(float), optional): Rotations in radians around x,
            y and z.
        name (str, optional): Light name.
        energy (float, optional): Light intensity.
        size (float, optional): Light size for ray shadow tracing. Use larger
            for softer shadows.

    Returns:
        bpy_types.Object: Light added.
    """
    bpy.ops.object.lamp_add(
        type='SUN', location=xyz, rotation=rot_vec_rad)
    sun = bpy.context.active_object

    if name is not None:
        sun.name = name

    sun.data.shadow_soft_size = size # larger means softer shadows

    # Strength
    engine = bpy.context.scene.render.engine
    if engine == 'CYCLES':
        sun.data.node_tree.nodes['Emission'].inputs[
            'Strength'].default_value = energy
    else:
        raise NotImplementedError(engine)

    logger.info("Sun lamp (parallel light) added")

    return sun


def add_light_area(xyz=(0, 0, 0), rot_vec_rad=(0, 0, 0), name=None,
                   energy=100, size=0.1):
    """Adds an area light that emits light rays the lambertian way.

    Args:
        xyz (tuple(float), optional): Location.
        rot_vec_rad (tuple(float), optional): Rotations in radians around x,
            y and z.
        name (str, optional): Light name.
        energy (float, optional): Light intensity.
        size (float, optional): Light size for ray shadow tracing.
            Use larger values for softer shadows.

    Returns:
        bpy_types.Object: Light added.
    """
    if (np.abs(rot_vec_rad) > 2 * np.pi).any():
        logger.warning(
            ("Some input value falls outside [-2pi, 2pi]. "
             "Sure inputs are in radians?"))

    bpy.ops.object.lamp_add(type='AREA', location=xyz, rotation=rot_vec_rad)
    area = bpy.context.active_object

    if name is not None:
        area.name = name

    area.data.size = size # larger means softer shadows

    # Strength
    engine = bpy.context.scene.render.engine
    if engine == 'CYCLES':
        area.data.node_tree.nodes['Emission'].inputs[
            'Strength'].default_value = energy
    else:
        raise NotImplementedError(engine)

    logger.info("Area light added")

    return area


def add_light_point(
        xyz=(0, 0, 0), name=None, size=0, color=(1, 1, 1), energy=100):
    """Adds an omnidirectional point lamp.

    Args:
        xyz (tuple(float), optional): Location.
        name (str, optional): Light name.
        size (float, optional): Light size; the larger the softer shadows are.
        color (tuple(float), optional): Color of the light.
        energy (float, optional): Light intensity.

    Returns:
        bpy_types.Object: Light added.
    """
    bpy.ops.object.lamp_add(type='POINT', location=xyz)
    point = bpy.context.active_object

    if name is not None:
        point.name = name

    if len(color) == 3:
        color += (1.,)

    point.data.shadow_soft_size = size

    # Strength
    engine = bpy.context.scene.render.engine
    if engine == 'CYCLES':
        point.data.node_tree.nodes['Emission'].inputs[
            'Strength'].default_value = energy
        point.data.node_tree.nodes['Emission'].inputs[
            'Color'].default_value = color
    else:
        raise NotImplementedError(engine)

    logger.info("Omnidirectional point light added")

    return point


def add_light_spot(xyz=(0, 0, 0), name=None, energy=100, shadow_soft_size=0.1,
                   spot_size=0.785, spot_blend=0.15):
    """Adds a spotlight lamp.

    Args:
        xyz (tuple(float), optional): Location.
        name (str, optional): Light name.
        energy (float, optional): Light intensity.
        shadow_soft_size (float, optional): Light size for raytracing the
            shadow.
        spot_size (float, optional): Angle, in radians, of the spotlight beam.
        spot_blend (float, optional): Softness of the spotlight edge.

    Returns:
        bpy_types.Object: Light added.
    """
    bpy.ops.object.lamp_add(type='SPOT', location=xyz)
    spot = bpy.context.active_object

    if name is not None:
        spot.name = name

    # Strength
    engine = bpy.context.scene.render.engine
    if engine == 'CYCLES':
        spot.data.node_tree.nodes['Emission'].inputs[
            'Strength'].default_value = energy
    else:
        raise NotImplementedError(engine)

    spot.data.shadow_soft_size = shadow_soft_size

    # Spot shape
    spot.data.spot_size = spot_size
    spot.data.spot_blend = spot_blend

    logger.info("Spotlight lamp added")

    return spot


def add_light_env(env=(1, 1, 1, 1), strength=1, rot_vec_rad=(0, 0, 0),
                  scale=(1, 1, 1)):
    r"""Adds environment lighting.

    Args:
        env (tuple(float) or str, optional): Environment map. If tuple,
            it's RGB or RGBA, each element of which :math:`\in [0,1]`.
            Otherwise, it's the path to an image.
        strength (float, optional): Light intensity.
        rot_vec_rad (tuple(float), optional): Rotations in radians around x,
            y and z.
        scale (tuple(float), optional): If all changed simultaneously,
            then no effects.
    """
    engine = bpy.context.scene.render.engine
    assert engine == 'CYCLES', "Rendering engine is not Cycles"

    if isinstance(env, str):
        bpy.data.images.load(env, check_existing=True)
        env = bpy.data.images[basename(env)]
    else:
        if len(env) == 3:
            env += (1,)
        assert len(env) == 4, "If tuple, env must be of length 3 or 4"

    world = bpy.context.scene.world
    world.use_nodes = True
    node_tree = world.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    bg_node = nodes.new('ShaderNodeBackground')
    links.new(bg_node.outputs['Background'],
              nodes['World Output'].inputs['Surface'])

    if isinstance(env, tuple):
        # Color
        bg_node.inputs['Color'].default_value = env
        logger.warning(("Environment is pure color, "
                        "so rotation and scale have no effect"))
    else:
        # Environment map
        texcoord_node = nodes.new('ShaderNodeTexCoord')
        env_node = nodes.new('ShaderNodeTexEnvironment')
        env_node.image = env
        mapping_node = nodes.new('ShaderNodeMapping')
        mapping_node.rotation = rot_vec_rad
        mapping_node.scale = scale
        links.new(texcoord_node.outputs['Generated'],
                  mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], env_node.inputs['Vector'])
        links.new(env_node.outputs['Color'], bg_node.inputs['Color'])

    bg_node.inputs['Strength'].default_value = strength
    logger.info("Environment light added")
