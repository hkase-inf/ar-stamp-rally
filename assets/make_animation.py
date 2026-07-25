import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

bc.fresh_import()

arm_obj = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')

action = bpy.data.actions.new("Wave")
arm_obj.animation_data_create()
arm_obj.animation_data.action = action

FPS = 24
FRAMES = 60  # 2.5s loop
bpy.context.scene.render.fps = FPS
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = FRAMES

pb = arm_obj.pose.bones
for name in ["Upper Arm_R", "Lower Arm_R", "Upper Arm_L", "Lower Arm_L", "Hip", "Spine", "Chest"]:
    pb[name].rotation_mode = 'XYZ'

def keyframe_euler(bone_name, f, x=0, y=0, z=0):
    b = pb[bone_name]
    b.rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
    b.keyframe_insert("rotation_euler", frame=f)

def keyframe_loc(bone_name, f, x=0, y=0, z=0):
    b = pb[bone_name]
    b.location = (x, y, z)
    b.keyframe_insert("location", frame=f)

WAVE_CYCLES = 3

for f in range(1, FRAMES + 1):
    t = (f - 1) / FRAMES  # 0..1 over the loop

    # waving right arm: constant raise + elbow bend, oscillating side-to-side swing
    swing = 25 + 15 * math.sin(2 * math.pi * WAVE_CYCLES * t)
    keyframe_euler("Upper Arm_R", f, x=75)
    keyframe_euler("Lower Arm_R", f, x=-30, z=swing)

    # resting left arm stays still
    keyframe_euler("Upper Arm_L", f, x=-70)
    keyframe_euler("Lower Arm_L", f, x=15)

    # gentle idle bounce + sway on the body
    bounce = 0.12 * (0.5 - 0.5 * math.cos(2 * math.pi * 2 * t))  # 2 bounces per loop, always >=0
    sway = 6 * math.sin(2 * math.pi * 1 * t)
    keyframe_loc("Hip", f, z=bounce)
    keyframe_euler("Spine", f, y=sway * 0.5)
    keyframe_euler("Chest", f, y=-sway * 0.3)

# constant interpolation-friendly: use linear so the per-frame sampling is exact
for layer in action.layers:
    for strip in layer.strips:
        for channelbag in strip.channelbags:
            for fcurve in channelbag.fcurves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'LINEAR'

bpy.ops.object.mode_set(mode='OBJECT')

# --- render a few frames to sanity check ---
objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
radius = max((maxs - mins).x, (maxs - mins).y, (maxs - mins).z) / 2
bc.setup_camera_and_light(center, radius, angle_deg=90)

scene = bpy.context.scene
out_dir = os.path.dirname(__file__)
for f in [1, 6, 16, 30, 46]:
    scene.frame_set(f)
    bc.render_to(os.path.join(out_dir, f"preview_anim_{f:03d}.png"))

# save a .blend for later export step
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, "shizuppi_animated.blend"))
print("DONE")
