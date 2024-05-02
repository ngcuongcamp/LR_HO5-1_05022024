from libs.libs import QThread, pyqtSignal, cv2, np
from src.utilities import config, logger, time


#! Camera Class


class CameraThread(QThread):
    frame_received = pyqtSignal(np.ndarray)
    update_error_signal = pyqtSignal()

    def __init__(self, camera_id, ref=None):

        super(CameraThread, self).__init__()
        self.camera_id = camera_id
        self.is_running = True
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        self.main_ref = ref
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1281)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1025)

    def run(self):
        while self.is_running:
            try:
                self.ret, self.frame = self.cap.read()
                # frame is working...
                if self.ret:
                    self.frame_received.emit(self.frame)
                else:
                    self.update_error_signal.emit()
                    self.cap.release()
                    logger.error("Camera Error")
                    self.is_running = False

            except Exception as E:
                print("Have an error while trying to connect camera: ", E)
                self.update_error_signal.emit()
                self.cap.release()
                logger.error("Camera Error")
                self.is_running = False

    def stop(self):
        self.is_running = False
        self.requestInterruption()
        self.cap.release()
        self.quit()
