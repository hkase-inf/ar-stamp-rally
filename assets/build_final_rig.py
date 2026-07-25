import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

HERE = os.path.dirname(__file__)
DOTAI_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\dotai.png"
MASTER_BLEND = os.path.join(HERE, "shizuppi_animated.blend")

bpy.ops.wm.open_mainfile(filepath=MASTER_BLEND)

arm_obj = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]


def bone_parent(obj_name, bone_name):
    obj = bpy.data.objects[obj_name]
    if obj.parent_type == "BONE" and obj.parent_bone == bone_name:
        return
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

# --- Wave: friendly wave + gentle idle bounce ---
WAVE_FRAMES = 60
WAVE_CYCLES = 3
wave_action = new_action("Wave")
for f in range(1, WAVE_FRAMES + 1):
    t = (f - 1) / WAVE_FRAMES
    swing = 25 + 15 * math.sin(2 * math.pi * WAVE_CYCLES * t)
    keyframe_euler("Upper Arm_R", f, x=75)
    keyframe_euler("Lower Arm_R", f, x=-30, z=swing)
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

# --- Spin: full 360 degree turn around the vertical axis, arms held out ---
SPIN_FRAMES = 60
spin_action = new_action("Spin")
for f in range(1, SPIN_FRAMES + 1):
    t = (f - 1) / SPIN_FRAMES
    keyframe_euler("Hip", f, y=360 * t)
    bounce = 0.08 * (0.5 - 0.5 * math.cos(2 * math.pi * 2 * t))
    keyframe_loc("Hip", f, y=bounce)
    keyframe_euler("Upper Arm_R", f, x=22)
    keyframe_euler("Lower Arm_R", f, x=-8)
    keyframe_euler("Upper Arm_L", f, x=22)
    keyframe_euler("Lower Arm_L", f, x=-8)
linearize(spin_action)

# restore Wave as the assigned/default action and neutral display frame
arm_obj.animation_data.action = wave_action
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = WAVE_FRAMES
bpy.context.scene.frame_set(1)

print("actions:", [a.name for a in bpy.data.actions])

bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.wm.save_as_mainfile(filepath=MASTER_BLEND)
print("saved", MASTER_BLEND)
