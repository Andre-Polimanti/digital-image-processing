from PIL import Image
import numpy as np

im = Image.open("requantization.tif")

images= [] # list of adaptaded images

array = np.array(im)

for bits in range(1,9): # We will get images of 1 bit quantization to 8 bits
    level = 2**bits - 1 # Since the levels of grey go from 0 to (2**bits - 1) we got to adapt to that reality

    arrayAdap = (np.round(array / 255.0 * (level)) * (255.0 / (level))).astype(np.uint8)
    imgAdap = Image.fromarray(arrayAdap)

    images.append(imgAdap)

# Dimensions of the images in RAM
w, h = images[0].size

# Generates a final image that will contain all eight images in RAM
final = Image.new("L", (4 * w, 2 * h))

# Builds the final image
for idx, img in enumerate(images):
    x = (idx % 4) * w
    y = (idx // 4) * h
    final.paste(img, (x, y))

# Shows the final image
final.show()