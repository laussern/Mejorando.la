from django.conf import settings
import Image
import os

def resize(size, imagen):
    path = os.path.join(settings.MEDIA_ROOT, str(imagen))

    image = Image.open(path)

    # sizes
    (width, height) = image.size
    (newWidth, newHeight) = size

    # relacion size actual, size nuevo
    ratioW = float(width) / newWidth
    ratioH = float(height) / newHeight
    ratio = ratioW if ratioW < ratioH else ratioH

    cropH, cropW = int(newHeight * ratio), int(newWidth * ratio)

    offsetX = (width - cropW) / 2
    offsetY = (height - cropH) / 2

    box = (offsetX, offsetY, cropW + offsetX, cropH + offsetY)
    image = image.crop(box)
    image = image.resize((newWidth, newHeight), Image.ANTIALIAS)

    # guardar la imagen
    image.save(path)
