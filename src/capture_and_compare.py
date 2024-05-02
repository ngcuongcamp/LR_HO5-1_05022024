import pyscreeze
import numpy as np
import pytesseract
import cv2
import time


# def detect_label(screenshot):
#     pytesseract.pytesseract.tesseract_cmd = (
#         r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#     )
#     # config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</"
#     # config = r"--oem 3 --psm 6"
#     config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789</"
#     try:
#         str_label = pytesseract.image_to_string(screenshot, config=config)
#         txt_result = str_label.strip().split(" ")[-1]
#         return txt_result
#     except Exception as E:
#         print(E)


# def get_text_result():
#     try:
#         image = capture_text_result()
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (3, 3), 0)
#         _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#         cv2.imshow("screenshot", gray)
#         cv2.waitKey(0)
#         pytesseract.pytesseract.tesseract_cmd = r"./libs/Tesseract-OCR/tesseract.exe"
#         # config = r"--oem 3 --psm 6"
#         # txt_result = pytesseract.image_to_string(image, config=config)
#         txt_result = pytesseract.image_to_string(gray)
#         print("txt detected: ", txt_result)
#         return txt_result
#     except Exception as E:
#         print(E)


# def capture_text_result():
#     # L362, T314, R817, B475
#     left = 362
#     top = 314
#     right = 817
#     bottom = 475
#     screenshot = pyscreeze.screenshot(region=(left, top, right - left, bottom - top))
#     screenshot = np.array(screenshot)

#     # screenshot = cv2.imread("./tat.png")
#     return screenshot


# 352, 104, 780, 136

template_1 = cv2.imread("./temp/template_1.png")
template_1 = cv2.cvtColor(template_1, cv2.COLOR_BGR2GRAY)
template_2 = cv2.imread("./temp/template_2.png")
template_2 = cv2.cvtColor(template_2, cv2.COLOR_BGR2GRAY)
template_3 = cv2.imread("./temp/template_3.png")
template_3 = cv2.cvtColor(template_3, cv2.COLOR_BGR2GRAY)


def capture_result_groupbox(left, top, width, height):
    capture_screen = pyscreeze.screenshot(region=(left, top, width, height))
    capture_screen = np.array(capture_screen)
    capture_screen = cv2.cvtColor(capture_screen, cv2.COLOR_BGR2GRAY)
    return capture_screen


def find_position_of_template(self, option):
    #! template_1 la anh pass ma sn
    #! template 2 la anh pass ma khuon (final pass)
    #! template 3 la anh pass (dieu kien dac biet)

    if option == 0:
        template_image = template_1
        confidence = self.PERCENT_MATCHING_1
    elif option == 1:
        template_image = template_2
        confidence = self.PERCENT_MATCHING_2
    elif option == 2:
        template_image = template_3
        confidence = self.PERCENT_MATCHING_3
    try:
        location = pyscreeze.locateOnScreen(
            image=template_image,
            minSearchTime=0.1,
            confidence=confidence,
            # region=(left, top, right - left, bottom - top),
            region=None,
            grayscale=True,
        )

        if location is not None:
            screenshot = capture_result_groupbox(
                int(location.left),
                int(location.top),
                int(location.width),
                int(location.height),
            )
            cv2.imwrite(f"./temp/screenshot_{option}.png", screenshot)
            return True
        else:
            return False
    except Exception as E:
        print(E)
        return False


def compare_sn_template(self, old_sn):
    try:
        location = pyscreeze.locateOnScreen(
            image=old_sn,
            minSearchTime=0.1,
            confidence=self.PERCENT_MATCHING_4,
            # region=(left, top, right - left, bottom - top),
            # region=(352, 104, (780 - 352), (136 - 104)),
            # region=(352, 104, (780 - 352), (136 - 104)),
            region=None,
            grayscale=True,
        )

        if location is not None:
            screenshot = capture_result_groupbox(
                int(location.left),
                int(location.top),
                int(location.width),
                int(location.height),
            )
            cv2.imwrite(f"./temp/new_sn.png", screenshot)
            return True
        else:
            return False
    except Exception as E:
        print(E)
        return False
