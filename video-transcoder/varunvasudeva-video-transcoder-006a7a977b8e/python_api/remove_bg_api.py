from rembg import remove
import pixellib
from pixellib.tune_bg import alter_bg
import cv2
import os

input_path = 'input_image/roop1.jpg'

output_path = 'output.png'

with open(input_path,'rb') as i:
    with open(output_path,'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)

change_bg = alter_bg()
change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
change_bg.blur_bg('output.png', extreme = True, output_image_name="output/extreme_blur_img.jpg")
change_bg.color_bg("output.png", colors = (255, 255, 255), output_image_name="roop/white_colored_bg.jpg")

# Assign a distinct color to the background of an image green background
change_bg.color_bg('output.png', colors = (0,128,0), output_image_name="roop/colored_bg.jpg")



