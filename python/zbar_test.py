from pyzbar.pyzbar import decode
from PIL import Image

decoded = decode(Image.open("/Users/aaronleopold/Documents/data_science/DataMatrix-Reader/images/test/barcode.JPG"))
data = str(decoded[0].data).replace("b\'", '').replace(' ', '_').replace('\'', '')
print (data)