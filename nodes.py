import cv2
import numpy as np
import math
import torch
from PIL import Image, ImageDraw, ImageFont
import os
from folder_paths import folder_names_and_paths, models_dir
import folder_paths
folder_names_and_paths["font"] = ([os.path.join(models_dir, "font")], [".ttf"])

class AddTextByMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", ),
                "mask": ("MASK", ),
                "font_file": (folder_paths.get_filename_list("font"), ),
                "hex_color": ("STRING", {"multiline": False, "default": "#000"}),
                "opacity": ("FLOAT", {"default": 1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "text": ("STRING", {"multiline": False, "default": "Hello"}, ),
            },
        }

    CATEGORY = "Text"
    RETURN_TYPES = ("IMAGE", "MASK",)
    RETURN_NAMES = ("image", "mask",)
    FUNCTION = "add_text_by_image"
    DESCRIPTION = ""

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color[1:] if hex_color[0]=='#' else hex_color
        if len(hex_color) == 3:
            hex_color = hex_color[0]*2 + hex_color[1]*2 + hex_color[2]*2
        hex_color = hex_color.ljust(6, '0')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def add_text_by_image(self, image, mask, font_file, hex_color, opacity, text):
        
        if len(mask.shape)>2:
            mask = mask[0]
        mask = (mask.numpy()*255).astype('uint8')

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            tmp = np.zeros_like(mask)

            rows = min(max(round(h/w*2.5),1),3)
            row_num = math.ceil(len(text)/rows)
            font_size = math.floor(w/row_num)
            dx = round(w-font_size*row_num,1)
            dy = round((h-font_size*rows)/2/rows,1)

            font = ImageFont.truetype(folder_paths.get_full_path("font", font_file), font_size)

            image = (image.numpy()*255).astype('uint8')[0]
            image = Image.fromarray(image).convert("RGBA")
            text_overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_overlay)

            image2 = Image.fromarray(tmp)
            draw2 = ImageDraw.Draw(image2)

            rgb = self.hex_to_rgb(hex_color)
            for row in range(rows):
                draw.text((x+dx,y+(font_size+dy*2)*row+dy-font_size/5), text[row_num*row:row_num*(row+1)], font=font, fill=(*rgb, int(opacity*255)))
                draw2.text((x+dx,y+(font_size+dy*2)*row+dy-font_size/5), text[row_num*row:row_num*(row+1)], font=font, fill='white')

            image =  Image.alpha_composite(image, text_overlay)
            
        return torch.from_numpy((np.array([image]).astype('float32')/255)), torch.from_numpy((np.array(image2).astype('float32')/255)), 

