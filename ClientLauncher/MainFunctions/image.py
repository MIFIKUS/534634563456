from PIL import Image as pil
import PIL.ImageGrab

import cv2
import numpy as np

import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class Image:
    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):
        if need_for_taking_screenshot:
            if area_of_screenshot:
                PIL.ImageGrab.grab(bbox=area_of_screenshot).save(main_image_name)
            else:
                PIL.ImageGrab.grab().save(main_image_name)

        img_rgb = cv2.imread(main_image_name, 0)
        template = cv2.imread(template_image_name, 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if func is None:
            for pt in zip(*loc[::-1]):
                print("Найдено совпадение")
                return True
            return False

        for pt in zip(*loc[::-1]):
            return list(pt)
        return False

    def delete_all_colors_except_one(self, file: str, colorMin_list: list, colorMax_list: list):
        """Функция для удаления всех цветов с картинки кроме одного"""
        im = cv2.imread(file)

        colorMin = np.array(colorMin_list, np.uint8)
        colorMax = np.array(colorMax_list, np.uint8)

        RGB  = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(RGB, colorMin, colorMax)

        inverse_cachement_mask = cv2.bitwise_not(mask)
        im[inverse_cachement_mask > 0] = [0, 0, 0]

        cv2.imwrite(file, mask)

    def take_screenshot(self, image_name, area_of_screenshot=None):
        print(f'area_of_screenshot {area_of_screenshot}')
        print(f'image_name {image_name}')
        if area_of_screenshot:
            PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
        else:
            PIL.ImageGrab.grab().save(image_name)

    def image_to_string(self, image_name, is_digits):
        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 6 -c tessedit_char_whitelist=0123456789.%(/)$')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='eng', config='--psm 3')
        return text

    def image_to_string_comma(self, image_name):
        text = pytesseract.image_to_string(image_name, config='--psm 6 -c tessedit_char_whitelist=0123456789,')
        return text

    def get_main_color(self, file):
        img = pil.open(file)
        colors = img.getcolors(512)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if (25, 30, 37) in c or (30, 35, 42) in c:
                    continue
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
            if type(most_present) is int:
                return (1, 1, 1)
            return most_present
        except TypeError:
            raise Exception("Too many colors in the image")