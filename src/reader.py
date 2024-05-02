from libs.libs import cv2, ZBarSymbol, decode, zxingcpp
from src.utilities import logger

path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)


def read_code_wechat(frames):
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            return data[0]
    return None


def read_code_pyzbar(frames):
    for frame in frames:
        decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
    return read_code_wechat(frames)


def read_code_zxingcpp(frames):
    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
    return read_code_pyzbar(frames)


def only_read_zxingcpp(frames):
    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
    return None


def process_frame1(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, opened, erosion, dilation]


def process_frame2(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, opened, erosion, dilation]


def loop_thresh_frame(self, frames, min_thresh, max_thresh, space_thresh):
    data = None
    for frame in frames:
        # print("for loop running")
        for thresh_value in range(min_thresh, max_thresh, space_thresh):

            _, thresh_frame = cv2.threshold(
                frame, thresh_value, max_thresh, cv2.THRESH_BINARY
            )
            data = only_read_zxingcpp([thresh_frame])

            if data is not None:
                print("thresh value: ", thresh_value)
                logger.info(f"--> THRESH VALUE: {thresh_value}")
                return data

        if data is not None:
            break
    return None
