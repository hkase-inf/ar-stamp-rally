import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

glb_path = os.path.join(os.path.dirname(__file__), "shizuppi.glb")
bpy.ops.import_scene.gltf(filepath=glb_path)

total = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
print("verify polys:", total)

action = bpy.data.actions.get("Wave")
print("action found:", action, action.frame_range if action else None)

arm_obj = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]
arm_obj.animation_data_create()
arm_obj.animation_data.action = action
bpy.context.scene.frame_start = int(action.frame_range[0])
bpy.context.scene.frame_end = int(action.frame_range[1])

objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
radius = max((maxs - mins).x, (maxs - mins).y, (maxs - mins).z) / 2
bc.setup_camera_and_light(center, radius, angle_deg=90)

for f in [1, 16, 30]:
    bpy.context.scene.frame_set(f)
    bc.render_to(os.path.join(os.path.dirname(__file__), f"preview_glb_{f:03d}.png"))
