import cv2
import numpy as np
import math
import torch
from PIL import Image, ImageDraw, ImageFont
import folder_paths

class AddTextByMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
               'mask': ("MASK",),
               "font_path": (folder_paths.get_filename_list("font"), ),
               "text": ("STRING", {"multiline": False}),
            },
        }

    CATEGORY = "Text"
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "add_text_by_image"
    DESCRIPTION = ""

    def add_text_by_image(self, mask, font_path, text):
        if len(mask.shape)>2:
            mask = mask[0]
        mask = (mask.numpy()*255).astype('uint8')

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            tmp = np.zeros_like(mask)

            rows = min(max(round(h/w),1),3)
            row_num = math.ceil(len(text)/rows)
            font_size = math.floor(w/row_num)
            dx = round(w-font_size*row_num,1)
            dy = round((h-font_size*rows)/2/rows,1)

            print(rows,row_num,font_size)

            font = ImageFont.truetype(folder_paths.get_full_path("font", font_path), font_size)

            image2 = Image.fromarray(tmp)
            draw = ImageDraw.Draw(image2)
            for row in range(rows):
                draw.text((x+dx,y+(font_size+dy*2)*row+dy-font_size/5), text[row_num*row:row_num*(row+1)], font=font, fill='white')
            
        return torch.from_numpy((np.array(image2).astype('float32')/255)), 

