import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import bpy

out_dir = os.path.dirname(__file__)
blend_path = os.path.join(out_dir, "shizuppi_animated.blend")
bpy.ops.wm.open_mainfile(filepath=blend_path)

print("=== before ===")
total = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
print("total polys:", total)

# --- 1. decimate meshes (keep vertex groups for skinning intact) ---
DECIMATE_RATIOS = {
    "胴体": 0.10,   # body: 83616 -> ~8362
    "帽子": 0.35,   # hat: 4096 -> ~1434
    "足": 0.35,     # legs: 4352 -> ~1523
    "揺れもの": 0.5,  # dangly bit: 1124 -> ~562
    # eyes/nose left as-is, already small (512 each)
}

for obj in bpy.data.objects:
    if obj.type != "MESH" or obj.name not in DECIMATE_RATIOS:
        continue
    ratio = DECIMATE_RATIOS[obj.name]
    mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod.ratio = ratio
    mod.vertex_group = ""  # apply uniformly
    # move Decimate before the Armature modifier so armature deforms the
    # already-decimated mesh (skin weights survive collapse-decimate)
    while obj.modifiers.find(mod.name) > 0 and obj.modifiers[obj.modifiers.find(mod.name) - 1].type == 'ARMATURE':
        bpy.context.view_layer.objects.active = obj
        with bpy.context.temp_override(object=obj):
            bpy.ops.object.modifier_move_up(modifier=mod.name)
    bpy.context.view_layer.objects.active = obj
    with bpy.context.temp_override(object=obj):
        bpy.ops.object.modifier_apply(modifier=mod.name)

print("=== after decimate ===")
total = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
print("total polys:", total)

# (body texture + nose color are already fixed in the source .blend by
# build_final_rig.py -- no per-export material patching needed here anymore)

# --- 2. dedupe + resize textures ---
by_path = {}
for img in list(bpy.data.images):
    key = img.filepath or img.name
    by_path.setdefault(key, []).append(img)

remap = {}
for key, imgs in by_path.items():
    if len(imgs) <= 1:
        continue
    canonical = imgs[0]
    for dup in imgs[1:]:
        remap[dup] = canonical

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.image in remap:
            node.image = remap[node.image]

for dup in remap:
    if dup.users == 0:
        bpy.data.images.remove(dup)

MAX_TEX = 512
for img in bpy.data.images:
    if img.size[0] > MAX_TEX or img.size[1] > MAX_TEX:
        img.scale(MAX_TEX, MAX_TEX)

print("=== images after dedupe/resize ===")
for img in bpy.data.images:
    print(img.name, img.size[:])

# --- 3. drop camera/light/empties that add nothing to a mobile render ---
for obj in list(bpy.data.objects):
    if obj.type in ("CAMERA", "LIGHT"):
        bpy.data.objects.remove(obj, do_unlink=True)

# --- 4. export ---
glb_path = os.path.join(out_dir, "shizuppi.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_texture_dir='',
    export_apply=False,
)

size_mb = os.path.getsize(glb_path) / (1024 * 1024)
print(f"EXPORTED {glb_path} : {size_mb:.2f} MB")
