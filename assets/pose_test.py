import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

bc.fresh_import()

arm_obj = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')

def rot(bone_name, axis, deg):
    pb = arm_obj.pose.bones[bone_name]
    pb.rotation_mode = 'XYZ'
    v = [0, 0, 0]
    v["XYZ".index(axis)] = math.radians(deg)
    pb.rotation_euler = v

# --- test values, tweak between runs ---
rot("Upper Arm_R", "X", 75)
def rot2(bone_name, ax1, deg1, ax2, deg2):
    pb = arm_obj.pose.bones[bone_name]
    pb.rotation_mode = 'XYZ'
    v = [0, 0, 0]
    v["XYZ".index(ax1)] = math.radians(deg1)
    v["XYZ".index(ax2)] = math.radians(deg2)
    pb.rotation_euler = v
rot2("Lower Arm_R", "X", -30, "Z", 30)
rot("Upper Arm_L", "X", -70)
rot("Lower Arm_L", "X", 15)

bpy.ops.object.mode_set(mode='OBJECT')

objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
radius = max((maxs - mins).x, (maxs - mins).y, (maxs - mins).z) / 2

bc.setup_camera_and_light(center, radius, angle_deg=90)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_pose.png"))
