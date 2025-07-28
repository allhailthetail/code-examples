#!/usr/bin/env python3
import argparse
import pdb
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

temp_image_loc = '/tmp/enhanced_img_tmp.jpg'
confidence_interval = 50


def parseargs():
    # init parser and def dict to hold values
    parser = argparse.ArgumentParser()
    args_dict = {}

    # define 'file' as an argument
    parser.add_argument("file")
    args = parser.parse_args()

    return args

def enhance_image(file):
    # Load the image
    image_path = str(file)
    image = Image.open(image_path)

    # Convert to greyscale
    image = image.convert("L")

    # Resize the image (e.g., reduce to half the size)
    image = image.resize((image.width // 2, image.height // 2))

    # Crop the image to improve model focus
    bounding_box = (94, 703, 1230, 947)
    image = image.crop(bounding_box)

    # Invert the colors
    inverted_image = ImageOps.invert(image)

    # Blurring removes a lot of noise
    blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(3)) # v1 value

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(blurred_image)
    enhanced_image = enhancer.enhance(9)  # v1 value

    # Save or show the processed image
    enhanced_image.save(temp_image_loc)  # Save the image

    # DEBUGGNG PURPOSES
    #enhanced_image.show()
    #pdb.set_trace()

def read_image(args):
    # Load the image
    image = Image.open(temp_image_loc)

    # Set the configuration to recognize only digits
    # psm6 assumes a uniform block of text. restrict characters to numeric
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

    # dict output seems necessary to obtain both the text and the confidence interval
    data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

    # Nums are only stored in the last entry.
    text_res = data['text'][-1]
    conf_res = data['conf'][-1]

    # If values fully match:
    #    i.e. are ~6 digits long and are within tolerance.
    if len(text_res) == 6 and int(conf_res) > confidence_interval:
        # Print file name:
        #print("\n", args.file)
        # print recognized text with confidence
        print(f"{args.file}: {text_res[0]}{text_res[1]}{text_res[2]}{text_res[3]}{text_res[4]}[{text_res[5]}] confidence: {conf_res}%")

def main():
    args = parseargs()
    #print(args.file)

    # Pass file to image enhancer
    enhance_image(args.file)

    #read_image()
    read_image(args)


if __name__ == '__main__':
    main()
