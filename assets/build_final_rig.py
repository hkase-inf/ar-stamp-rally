import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

HERE = os.path.dirname(__file__)
DOTAI_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\dotai.png"
MASTER_BLEND = os.path.join(HERE, "shizuppi_animated.blend")

bpy.ops.wm.open_mainfile(filepath=MASTER_BLEND)

arm_obj = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]

# --- 1. fix hat attachment: it was object-parented to the body (rigid,
# ignores all pose deformation) instead of bone-parented to the head ---
hat = bpy.data.objects["帽子"]
if hat.parent_type != "BONE":
    arm_obj.data.bones.active = arm_obj.data.bones["Head"]
    bpy.ops.object.select_all(action="DESELECT")
    hat.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type="BONE", keep_transform=True)

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

# --- 4. author two more motions (kept to arm bones + rigid Hip transforms,
# since spine/chest bends visibly tear this garment-shaped mesh) ---
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode="POSE")
pb = arm_obj.pose.bones
for name in ["Upper Arm_R", "Lower Arm_R", "Upper Arm_L", "Lower Arm_L", "Hip"]:
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

# --- Jump: crouch-launch-land loop, both arms thrown up ---
JUMP_FRAMES = 40
jump_action = new_action("Jump")
for f in range(1, JUMP_FRAMES + 1):
    t = (f - 1) / JUMP_FRAMES
    launch = math.sin(2 * math.pi * t)
    bounce = max(0.0, launch) ** 0.6 * 1.35
    squash = -0.12 if launch < -0.6 else 0.0  # tiny crouch dip before/after
    keyframe_loc("Hip", f, z=bounce + squash)
    keyframe_euler("Upper Arm_R", f, x=80)
    keyframe_euler("Lower Arm_R", f, x=-15)
    keyframe_euler("Upper Arm_L", f, x=80)
    keyframe_euler("Lower Arm_L", f, x=-15)
linearize(jump_action)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = JUMP_FRAMES

# --- Spin: full 360 degree turn, arms held out ---
SPIN_FRAMES = 60
spin_action = new_action("Spin")
for f in range(1, SPIN_FRAMES + 1):
    t = (f - 1) / SPIN_FRAMES
    keyframe_euler("Hip", f, z=360 * t)
    bounce = 0.08 * (0.5 - 0.5 * math.cos(2 * math.pi * 2 * t))
    keyframe_loc("Hip", f, z=bounce)
    keyframe_euler("Upper Arm_R", f, x=22)
    keyframe_euler("Lower Arm_R", f, x=-8)
    keyframe_euler("Upper Arm_L", f, x=22)
    keyframe_euler("Lower Arm_L", f, x=-8)
linearize(spin_action)

# restore Wave as the assigned/default action and neutral display frame
wave_action = bpy.data.actions.get("Wave")
arm_obj.animation_data.action = wave_action
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
bpy.context.scene.frame_set(1)

print("actions:", [a.name for a in bpy.data.actions])

bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.wm.save_as_mainfile(filepath=MASTER_BLEND)
print("saved", MASTER_BLEND)
