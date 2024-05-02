# from src.capture_and_compare import capture_result_groupbox, compare_sn_template
# import cv2
# import pyscreeze
# import time
#
# # time.sleep(3)
# # 352, 104, 780, 136
#
# left = 352
# top = 104
# right = 780
# bottom = 136
#
# img1 = capture_result_groupbox(left, top, (right - left), (bottom - top))
# cv2.imshow("test", img1)
# cv2.waitKey(0)
#
#
# def compare_sn_template(old_sn):
#     try:
#         location = pyscreeze.locateOnScreen(
#             image=old_sn,
#             minSearchTime=0,
#             confidence=0.94,
#             # region=(left, top, right - left, bottom - top),
#             # region=(left, top, (right - left), (bottom - top)),
#             region=None,
#             grayscale=True,
#         )
#
#         if location is not None:
#             screenshot = capture_result_groupbox(
#                 int(location.left),
#                 int(location.top),
#                 int(location.width),
#                 int(location.height),
#             )
#             cv2.imshow("new sn", screenshot)
#             cv2.waitKey(0)
#             return True
#         else:
#             return False
#     except Exception as E:
#         print(E)
#         return False
#
#
# result_cp = compare_sn_template(img1)
#
# print(result_cp)


from libs.libs import Desktop, keyboard, pyautogui
import time


def test():
    x = 352 + ((780 - 352) / 2)
    y = 59 + ((91 - 59) / 2)
    pyautogui.moveTo(x, y)
    pyautogui.click(x=x, y=y)
    pyautogui.typewrite('11111')
    pyautogui.moveTo(x, y)

time.sleep(3)

test()
