import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import os
import numpy as np
import zxingcpp


path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)

path = r"./image_NG/2024-04-01/CAMERA1"
arr = []


def read_code_wechat(frames):
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            return data[0]
    return read_code_pyzbar(frames)


def read_code_pyzbar(frames):
    for frame in frames:
        cv2.imshow("frame", frame)
        decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
    return read_code_zxingcpp(frames)


def read_code_zxingcpp(frames):
    for frame in frames:
        cv2.imshow("frame", frame)
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
    return None


def read_code_loop(frames):
    for frame in frames:
        cv2.imshow("frame", frame)
        for threshold in range(50, 110, 3):
            _, thresh = cv2.threshold(frame, threshold, 110, cv2.THRESH_BINARY)

            data_decoded = zxingcpp.read_barcodes(thresh)
            if data_decoded:
                print(f" Thresh value: {threshold} ")
                arr.append(threshold)
                return data_decoded[0].text
            cv2.imshow("image", thresh)
            cv2.waitKey(1)
    return None


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        91,
        3,
    )

    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, thresh, opened, erosion, dilation]


for index in os.scandir(path=path):
    frame = cv2.imread(index.path)

    frames = process_frame(frame)
    data_decoded = None

    max_loop = 5

    while max_loop >= 0:
        max_loop = max_loop - 1
        data_decoded = read_code_wechat(frames)
        if data_decoded is not None:
            break
        # else:
        #     data_decoded = read_code_loop(frames)
        #     if data_decoded is not None:
        #         break

    cv2.waitKey(1)

    if data_decoded is not None:
        print(data_decoded, index.path)
    else:
        cv2.waitKey(0)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXX", index.path)

# print(f"{min(arr)} - {max(arr)}")
cv2.destroyAllWindows()
