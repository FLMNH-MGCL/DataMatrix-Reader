from pyzbar.pyzbar import decode
from PIL import Image

path = "MGCL_1000224_F_D.JPG" # whatever function you use to read an image file into a numpy array

decoded = decode(Image.open(path))
name = str(decoded[0].data)
name = name.replace("'", "")
name = name.replace("b", "")
print(name)