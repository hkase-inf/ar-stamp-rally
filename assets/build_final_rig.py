import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

HERE = os.path.dirname(__file__)
DOTAI_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\dotai.png"
MASTER_BLEND = os.path.join(HERE, "shizuppi_animated.blend")

bpy.ops.wm.open_mainfile(filepath=MASTER_BLEND)

arm_obj = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]

# reset to true rest pose BEFORE any bone-parenting: the file may still be
# sitting at a previous run's Wave-pose frame 1 (arm already raised), which
# would bake that offset into keep_transform's parent_inverse for small
# objects like the eyes/nose (likely why they ended up invisible/misplaced)
arm_obj.animation_data_clear()
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode="POSE")
for pb in arm_obj.pose.bones:
    pb.location = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.rotation_euler = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()


def bone_parent(obj_name, bone_name):
    # always re-run (even if already bone-parented) so the parent_inverse is
    # recomputed from the current (now guaranteed rest-pose) state
    obj = bpy.data.objects[obj_name]
    arm_obj.data.bones.active = arm_obj.data.bones[bone_name]
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type="BONE", keep_transform=True)


# --- 1. fix rigid prop attachment: these were object-parented to the body
# (rigid, ignore all pose deformation -- e.g. stayed behind during Spin)
# instead of bone-parented to the bone they should follow ---
bone_parent("帽子", "Head")
bone_parent("右目", "Head")
bone_parent("左目", "Head")
bone_parent("鼻", "Head")
bone_parent("揺れもの", "Head")
bone_parent("足", "Hip")

# --- 2. fix the body material: real texture, tinted blue so it clearly
# reads as blue (UV layout otherwise favors the texture's white highlights) ---
BODY_BLUE = (110 / 255, 231 / 255, 255 / 255, 1.0)
BODY_TINT_FACTOR = 0.65

body_mat = bpy.data.materials.get("Material")
nt = body_mat.node_tree
for node in [n for n in nt.nodes if n.type in ("TEX_IMAGE", "MIX")]:
    nt.nodes.remove(node)
bsdf_node = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
dotai_img = bpy.data.images.load(DOTAI_PATH, check_existing=True)
tex_node = nt.nodes.new("ShaderNodeTexImage")
tex_node.image = dotai_img
tex_node.location = (bsdf_node.location.x - 500, bsdf_node.location.y)

mix = nt.nodes.new("ShaderNodeMix")
mix.data_type = "RGBA"
mix.blend_type = "MIX"
mix.location = (bsdf_node.location.x - 250, bsdf_node.location.y - 120)
color_inputs = [s for s in mix.inputs if s.type == "RGBA"]
color_outputs = [s for s in mix.outputs if s.type == "RGBA"]
factor_input = next(s for s in mix.inputs if s.name == "Factor" and s.type == "VALUE")
factor_input.default_value = BODY_TINT_FACTOR
color_inputs[1].default_value = BODY_BLUE
nt.links.new(tex_node.outputs["Color"], color_inputs[0])
nt.links.new(color_outputs[0], bsdf_node.inputs["Base Color"])

# --- 3. fix the nose: flat, slightly-darker blue than the body ---
nose_mat = bpy.data.materials.get("マテリアル.005")
for node in list(nose_mat.node_tree.nodes):
    if node.type == "BSDF_PRINCIPLED":
        node.inputs["Base Color"].default_value = (37 / 255, 123 / 255, 140 / 255, 1.0)
    if node.type == "TEX_IMAGE":
        nose_mat.node_tree.nodes.remove(node)

# --- 4. (re)author all three motions. IMPORTANT: verified by direct matrix
# computation that the Hip bone's "up" axis is local Y, not Z (Z actually
# points along world -Y) -- using Z here is what made Jump move sideways. ---
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode="POSE")
pb = arm_obj.pose.bones
for name in ["Upper Arm_R", "Lower Arm_R", "Upper Arm_L", "Lower Arm_L", "Hip", "Spine", "Chest"]:
    pb[name].rotation_mode = "XYZ"

FPS = 24
bpy.context.scene.render.fps = FPS


def new_action(name):
    existing = bpy.data.actions.get(name)
    if existing:
        bpy.data.actions.remove(existing)
    action = bpy.data.actions.new(name)
    action.use_fake_user = True  # keep it in the file even when not the active action
    arm_obj.animation_data.action = action
    return action


def keyframe_euler(bone_name, f, x=0, y=0, z=0):
    b = pb[bone_name]
    b.rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
    b.keyframe_insert("rotation_euler", frame=f)


def keyframe_loc(bone_name, f, x=0, y=0, z=0):
    b = pb[bone_name]
    b.location = (x, y, z)
    b.keyframe_insert("location", frame=f)


def linearize(action):
    for layer in action.layers:
        for strip in layer.strips:
            for channelbag in strip.channelbags:
                for fcurve in channelbag.fcurves:
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = "LINEAR"


arm_obj.animation_data_create()

# --- Rest: static neutral pose, both arms down. This is the default state
# when the bonus stage loads / when the motion toggle is switched off. Two
# identical frames so it's a valid (non-zero-length) clip but reads as
# perfectly still. ---
REST_FRAMES = 2
rest_action = new_action("Rest")
for f in range(1, REST_FRAMES + 1):
    keyframe_euler("Upper Arm_R", f, x=-70)
    keyframe_euler("Lower Arm_R", f, x=15)
    keyframe_euler("Upper Arm_L", f, x=-70)
    keyframe_euler("Lower Arm_L", f, x=15)
    keyframe_loc("Hip", f, y=0)
    keyframe_euler("Spine", f, y=0)
    keyframe_euler("Chest", f, y=0)
linearize(rest_action)

# --- Wave: friendly wave + gentle idle bounce ---
WAVE_FRAMES = 60
WAVE_CYCLES = 3
wave_action = new_action("Wave")
for f in range(1, WAVE_FRAMES + 1):
    t = (f - 1) / WAVE_FRAMES
    swing = 25 + 15 * math.sin(2 * math.pi * WAVE_CYCLES * t)
    keyframe_euler("Upper Arm_R", f, x=75)
    keyframe_euler("Lower Arm_R", f, x=-30, y=90, z=swing)
    keyframe_euler("Upper Arm_L", f, x=-70)
    keyframe_euler("Lower Arm_L", f, x=15)
    bounce = 0.12 * (0.5 - 0.5 * math.cos(2 * math.pi * 2 * t))
    keyframe_loc("Hip", f, y=bounce)
    sway = 6 * math.sin(2 * math.pi * 1 * t)
    keyframe_euler("Spine", f, y=sway * 0.5)
    keyframe_euler("Chest", f, y=-sway * 0.3)
linearize(wave_action)

# --- Jump: crouch-launch-land loop, both arms thrown up ---
JUMP_FRAMES = 40
jump_action = new_action("Jump")
for f in range(1, JUMP_FRAMES + 1):
    t = (f - 1) / JUMP_FRAMES
    launch = math.sin(2 * math.pi * t)
    bounce = max(0.0, launch) ** 0.6 * 1.35
    squash = -0.12 if launch < -0.6 else 0.0  # tiny crouch dip before/after
    keyframe_loc("Hip", f, y=bounce + squash)
    keyframe_euler("Upper Arm_R", f, x=80)
    keyframe_euler("Lower Arm_R", f, x=-15)
    keyframe_euler("Upper Arm_L", f, x=80)
    keyframe_euler("Lower Arm_L", f, x=-15)
linearize(jump_action)

# --- Walk: bouncy walk-in-place loop, front-facing throughout (the "足"
# mesh is one rigid piece, not per-leg skinned, so there's no real leg
# articulation to animate -- this fakes a walking feel with a footstep-like
# double-bounce, a side-to-side waddle, and opposite-phase arm swing) ---
WALK_FRAMES = 32
WALK_STEPS = 2  # steps per loop
walk_action = new_action("Walk")
for f in range(1, WALK_FRAMES + 1):
    t = (f - 1) / WALK_FRAMES
    step_phase = 2 * math.pi * WALK_STEPS * t
    bounce = 0.11 * abs(math.sin(step_phase))
    waddle = 7 * math.sin(step_phase)
    arm_swing = 20 * math.sin(step_phase)
    keyframe_loc("Hip", f, y=bounce)
    keyframe_euler("Hip", f, z=waddle)
    keyframe_euler("Upper Arm_R", f, x=-70, z=arm_swing)
    keyframe_euler("Lower Arm_R", f, x=15)
    keyframe_euler("Upper Arm_L", f, x=-70, z=-arm_swing)
    keyframe_euler("Lower Arm_L", f, x=15)
linearize(walk_action)

# restore Wave as the assigned/default action and neutral display frame
arm_obj.animation_data.action = wave_action
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = WAVE_FRAMES
bpy.context.scene.frame_set(1)

# drop any orphaned action from earlier iterations (e.g. the old "Spin",
# now replaced by "Walk") so it doesn't linger in the file / get exported
KEEP_ACTIONS = {"Rest", "Wave", "Jump", "Walk"}
for action in list(bpy.data.actions):
    if action.name not in KEEP_ACTIONS:
        bpy.data.actions.remove(action)

print("actions:", [a.name for a in bpy.data.actions])

bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.wm.save_as_mainfile(filepath=MASTER_BLEND)
print("saved", MASTER_BLEND)
