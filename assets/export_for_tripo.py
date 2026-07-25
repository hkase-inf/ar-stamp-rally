import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

DOTAI_PATH = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\dotai.png"

# The FBX importer turned out to be non-deterministic across runs (material
# node graphs differed run to run). Use the already-validated saved file
# instead of re-importing the FBX fresh.
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(__file__), "shizuppi_animated.blend"))
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# --- fix the body material: use the real, now-supplied texture, tinted blue
# (the mesh's UV layout puts mostly the texture's *white* highlight regions
# on the outward-facing surface, so a plain texture swap still reads as
# white; blend in a strong blue tint so the body clearly reads as blue) ---
BODY_BLUE = (110 / 255, 231 / 255, 255 / 255, 1.0)  # sampled from dotai.png's own background
BODY_TINT_FACTOR = 0.65

body_mat = bpy.data.materials.get("Material")
if body_mat and body_mat.use_nodes:
    nt = body_mat.node_tree
    dotai_img = bpy.data.images.load(DOTAI_PATH, check_existing=True)
    bsdf_node = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")

    # this material never actually had an Image Texture node wired up (the
    # FBX reimport that previously showed one was non-deterministic) --
    # create one from scratch rather than assuming it exists
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = dotai_img
    tex_node.location = (bsdf_node.location.x - 500, bsdf_node.location.y)

    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MIX'
    mix.location = (tex_node.location.x + 160, tex_node.location.y - 120)
    color_inputs = [s for s in mix.inputs if s.type == 'RGBA']
    color_outputs = [s for s in mix.outputs if s.type == 'RGBA']
    factor_input = next(s for s in mix.inputs if s.name == "Factor" and s.type == 'VALUE')
    factor_input.default_value = BODY_TINT_FACTOR
    color_inputs[0].default_value = (0, 0, 0, 1)  # A, overwritten by link below
    color_inputs[1].default_value = BODY_BLUE       # B

    nt.links.new(tex_node.outputs["Color"], color_inputs[0])
    nt.links.new(color_outputs[0], bsdf_node.inputs["Base Color"])

# --- fix the nose material: flat, slightly-darker blue than the body ---
nose_mat = bpy.data.materials.get("マテリアル.005")
if nose_mat and nose_mat.use_nodes:
    for node in list(nose_mat.node_tree.nodes):
        if node.type == "BSDF_PRINCIPLED":
            node.inputs["Base Color"].default_value = (37 / 255, 123 / 255, 140 / 255, 1.0)
        if node.type == "TEX_IMAGE":
            nose_mat.node_tree.nodes.remove(node)

# --- reset to the neutral bind pose (the saved file's frame 1 already has
# the wave-ready arm raised, which we don't want baked into a static mesh) ---
arm_obj = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]
arm_obj.animation_data_clear()
for pb in arm_obj.pose.bones:
    pb.location = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.rotation_euler = (0, 0, 0)
    pb.rotation_axis_angle = (0, 0, 1, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()

# --- render a quick sanity check before export ---
objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
radius = max((maxs - mins).x, (maxs - mins).y, (maxs - mins).z) / 2
bc.setup_camera_and_light(center, radius, angle_deg=90)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_for_tripo.png"))

total = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
print("total polys (full res, uncompressed for Tripo):", total)

# --- export: full resolution, no Draco (third-party tool compatibility),
# no baked animation -- just a clean static mesh for retopology/cleanup ---
for obj in list(bpy.data.objects):
    if obj.type in ("CAMERA", "LIGHT"):
        bpy.data.objects.remove(obj, do_unlink=True)

out_path = os.path.join(os.path.dirname(__file__), "shizuppi_for_tripo.glb")
bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format='GLB',
    use_selection=False,
    export_animations=False,
    export_draco_mesh_compression_enable=False,
    export_apply=False,
)

size_mb = os.path.getsize(out_path) / (1024 * 1024)
print(f"EXPORTED {out_path} : {size_mb:.2f} MB")
