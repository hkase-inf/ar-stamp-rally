import bpy
import mathutils

FBX_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\shizuppi.fbx"
BLEND_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\shizuppi2.blend"


def fresh_import():
    """Deprecated FBX-based import path (kept for reference); loses the body's
    node-based material setup on roundtrip. Use fresh_open() instead."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.render.engine = 'CYCLES'
    import cycles.properties
    if not hasattr(cycles.properties.CyclesLightSettings, "cast_shadow"):
        cycles.properties.CyclesLightSettings.cast_shadow = bpy.props.BoolProperty(
            name="Cast Shadow", default=True)
    bpy.ops.import_scene.fbx(filepath=FBX_PATH)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'


def fresh_open():
    """Open the authoritative source file directly (correct materials, no FBX lossiness)."""
    bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'


def world_bbox(objs):
    mins = mathutils.Vector((1e9, 1e9, 1e9))
    maxs = mathutils.Vector((-1e9, -1e9, -1e9))
    for obj in objs:
        if obj.type != 'MESH':
            continue
        for corner in obj.bound_box:
            world_co = obj.matrix_world @ mathutils.Vector(corner)
            mins.x, mins.y, mins.z = min(mins.x, world_co.x), min(mins.y, world_co.y), min(mins.z, world_co.z)
            maxs.x, maxs.y, maxs.z = max(maxs.x, world_co.x), max(maxs.y, world_co.y), max(maxs.z, world_co.z)
    return mins, maxs


def setup_camera_and_light(target_center, radius, angle_deg=0, height_offset=0.0):
    import math
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    ang = math.radians(angle_deg)
    dist = radius * 4.2
    cam.location = (
        target_center.x + dist * math.sin(ang),
        target_center.y - dist * math.cos(ang),
        target_center.z + radius * 0.15 + height_offset,
    )
    direction = target_center - mathutils.Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type='SUN', location=(target_center.x + radius, target_center.y - radius, target_center.z + radius * 2))
    sun = bpy.context.object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(55), 0, math.radians(35))

    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.9, 0.9, 0.92, 1)
        bg.inputs[1].default_value = 1.0

    return cam


def render_to(path, res=700):
    scene = bpy.context.scene
    scene.render.resolution_x = res
    scene.render.resolution_y = res
    scene.render.filepath = path
    scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
