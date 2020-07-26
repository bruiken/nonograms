from PIL import Image
import os

current_dir = os.getcwd().replace('\\', '/')
image = Image.open(current_dir + "/generator/images/image_1_1.png")

def get_width(image):
    return image._size[0]

def get_height(image):
    return image._size[1]

attributes = image.__dict__.items()
print(attributes)

for x in range(get_width(image)):
    col_vals = {}
    for y in range(get_height(image)):
        a = image.getpixel((x,y))
        avg_val = (a[0] + a[1] + a[2]) / 3 / 255
        if avg_val >= 0.5:
            col_vals[y] = 1
        else:
            col_vals[y] = 0

    print(col_vals)