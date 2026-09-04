import base64, io
from PIL import Image
import mss

class ScreenCapture:
    def __init__(self, scale=1.0): self.scale=scale
    def grab(self):
        with mss.mss() as sct:
            mon=sct.monitors[1]
            raw=sct.grab(mon)
            img=Image.frombytes("RGB", raw.size, raw.rgb)
        if self.scale != 1.0:
            img=img.resize((int(img.width*self.scale), int(img.height*self.scale)))
        buf=io.BytesIO(); img.save(buf, format="PNG", optimize=True)
        return img, base64.b64encode(buf.getvalue()).decode()
