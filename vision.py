from google.cloud import vision
from PIL import Image
import io
client = vision.ImageAnnotatorClient()

path='5chang166.png'
with io.open(path, 'rb') as image_file:
    content = image_file.read()

mage = vision.types.Image(content=content)

response = client.text_detection(image=mage)
texts = response.text_annotations

clothesline=""
for text in texts:
    clothesline+=text.description

print(clothesline)