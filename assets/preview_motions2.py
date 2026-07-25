import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(__file__), "shizuppi_animated.blend"))
arm = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]
if bpy.context.mode != "OBJECT":
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="OBJECT")

objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
radius = max((maxs - mins).x, (maxs - mins).y, (maxs - mins).z) / 2
bc.setup_camera_and_light(center, radius, angle_deg=90)

# Jump at peak frame
arm.animation_data.action = bpy.data.actions["Jump"]
bpy.context.scene.frame_set(11)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_jump2.png"))

# Spin at a quarter turn -- check eyes/nose/hat all rotate together
arm.animation_data.action = bpy.data.actions["Spin"]
bpy.context.scene.frame_set(10)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_spin2_quarter.png"))
bpy.context.scene.frame_set(30)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_spin2_half.png"))
