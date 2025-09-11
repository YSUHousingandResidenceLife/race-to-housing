# tile_image.py
from PIL import Image
import math, os, sys, json

# Usage: python tile_image.py <image.png> <out_dir>
src = sys.argv[1]
out_dir = sys.argv[2]

img = Image.open(src).convert("RGB")
W, H = img.size
T = 256

# Compute max zoom so that at maxZoom the image fits in tiles of 256px
max_zoom = int(math.ceil(math.log2(max(W, H) / T))) if max(W, H) > T else 0

os.makedirs(out_dir, exist_ok=True)

def tile_at_level(level_img, z):
    w, h = level_img.size
    xtiles = math.ceil(w / T)
    ytiles = math.ceil(h / T)
    z_dir = os.path.join(out_dir, str(z))
    os.makedirs(z_dir, exist_ok=True)
    for x in range(xtiles):
        for y in range(ytiles):
            box = (x*T, y*T, min((x+1)*T, w), min((y+1)*T, h))
            tile = level_img.crop(box)
            tile_path = os.path.join(z_dir, f"{x}/{y}.png")
            os.makedirs(os.path.dirname(tile_path), exist_ok=True)
            tile.save(tile_path, format="PNG", compress_level=1)

# Build pyramid: z=0 smallest, z=max_zoom full size
for z in range(0, max_zoom+1):
    scale = 2**(max_zoom - z)
    level = img.resize((max(1, W//scale), max(1, H//scale)), Image.LANCZOS)
    tile_at_level(level, z)

with open(os.path.join(out_dir, "meta.json"), "w") as f:
    json.dump({"width": W, "height": H, "tileSize": T, "maxZoom": max_zoom}, f)

print(f"Done. width={W}, height={H}, maxZoom={max_zoom}, tiles in {out_dir}/<z>/<x>/<y>.png")
