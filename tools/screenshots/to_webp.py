"""Turn the captured PNGs into the WebP files the guide uses."""
import glob, os
from PIL import Image
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "delivery-tracker", "img")
for p in glob.glob(os.path.join(IMG, "*.png")):
    Image.open(p).convert("RGB").save(p[:-4] + ".webp", "WEBP", quality=82, method=6)
    os.remove(p)
    print("webp:", os.path.basename(p)[:-4])
