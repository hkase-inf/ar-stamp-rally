import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import bpy
import blender_common as bc

bc.fresh_import()

objs = list(bpy.data.objects)
mins, maxs = bc.world_bbox(objs)
center = (mins + maxs) / 2
size = maxs - mins
radius = max(size.x, size.y, size.z) / 2

bc.setup_camera_and_light(center, radius, angle_deg=90)
bc.render_to(os.path.join(os.path.dirname(__file__), "preview_rest.png"))

print("center", center, "radius", radius)
print("bbox min", mins, "max", maxs)
