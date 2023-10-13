from flask import *
import pixellib
from pixellib.tune_bg import alter_bg
import filetype
import cv2
import os

app = Flask(__name__)

@app.route('/api',methods=["GET","POST"])
def img_background_change_api():
    if request.method == "POST":
        image_path= request.form['image_path']
        bg_image_path = request.form['bg_image_path']
        if filetype.is_image(image_path) and filetype.is_image(bg_image_path):
            print(f"{image_path} {bg_image_path} is a valid image...")

            change_bg = alter_bg()
            change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
            change_bg.change_bg_img(f_image_path = image_path,b_image_path = bg_image_path, output_image_name="output_image/background_change_img.jpg")


            change_bg.blur_bg(image_path, extreme = True, output_image_name="output_image/extreme_blur_img.jpg")


            # Assign a distinct color to the background of an image green background
            change_bg.color_bg("output_image/extreme_blur_img.jpg", colors = (0,128,0), output_image_name="output_image/colored_bg.jpg")

            # white background
            change_bg.color_bg("output_image/extreme_blur_img.jpg", colors = (255, 255, 255), output_image_name="output_image/white_colored_bg.jpg")

            # grayscale the background of an image
            change_bg.gray_bg(image_path,output_image_name="output_image/gray_img.jpg")

            # Blur Image Background
            # The image is blurred with a low effect.
            change_bg.blur_bg(image_path, low = True, output_image_name="output_image/blur_img.jpg")

            # moderately blur the background of the image,
            change_bg.blur_bg(image_path, moderate = True, output_image_name="output_image/moderate_blur_img.jpg")

            # We want to deeply blurred the background of the image, and we set extreme to true.
            # change_bg.blur_bg(image_path, extreme = True, output_image_name="output_image/extreme_blur_img.jpg")

            print(image_path)
            print(bg_image_path)
            print("File location using os.getcwd():", os.getcwd())
            message = "Background Image change Successfully..."
        else:
            print(f"{bg_image_path} is not a valid image...")
    
    return jsonify({'message':message})


if __name__=='__main__':
    app.run(debug=True)


# '/home/roop/Roopsingh/moviepy'
