import bpy
import sys

fbx_path = r"C:\Users\kase0\Downloads\20260725GrateFigures\bonus\shizuppi.fbx"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.engine = 'CYCLES'

# Work around a bug in this Blender build's FBX importer: it tries to set
# Light.cycles.cast_shadow, which doesn't exist in this build's Cycles addon schema.
try:
    import cycles.properties
    cycles.properties.CyclesLightSettings.cast_shadow = bpy.props.BoolProperty(name="Cast Shadow", default=True)
    print("patched cast_shadow OK")
except Exception as e:
    print("patch failed", e)

bpy.ops.import_scene.fbx(filepath=fbx_path, use_custom_props=False)

print("=== OBJECTS ===")
for obj in bpy.data.objects:
    print(f"- {obj.name} type={obj.type} loc={tuple(round(v,3) for v in obj.location)} "
          f"dims={tuple(round(v,3) for v in obj.dimensions)}")
    if obj.type == "MESH":
        mesh = obj.data
        print(f"    verts={len(mesh.vertices)} polys={len(mesh.polygons)} "
              f"materials={[m.name if m else None for m in mesh.materials]}")
        if obj.vertex_groups:
            print(f"    vertex_groups={[vg.name for vg in obj.vertex_groups][:10]} (count={len(obj.vertex_groups)})")
    if obj.type == "ARMATURE":
        arm = obj.data
        print(f"    bones={len(arm.bones)} names={[b.name for b in arm.bones][:15]}")

print("=== ACTIONS (animations) ===")
for action in bpy.data.actions:
    print(f"- {action.name} frame_range={action.frame_range[:]} fcurves={len(action.fcurves)}")

print("=== MATERIALS ===")
for mat in bpy.data.materials:
    print(f"- {mat.name}")

print("=== IMAGES/TEXTURES ===")
for img in bpy.data.images:
    print(f"- {img.name} size={img.size[:]} filepath={img.filepath}")

print("=== ARMATURE MODIFIERS ON MESHES ===")
for obj in bpy.data.objects:
    if obj.type == "MESH":
        for mod in obj.modifiers:
            print(f"- {obj.name}: modifier {mod.name} type={mod.type}")
