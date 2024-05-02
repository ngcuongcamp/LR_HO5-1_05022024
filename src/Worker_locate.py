from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool


class WorkerSignals(QObject):
    finished = pyqtSignal(bool)


class Worker_locate(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(Worker_locate, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        # Thực hiện công việc trong hàm func với các tham số được truyền vào
        result = self.func(*self.args, **self.kwargs)
        # Khi công việc hoàn thành, phát tín hiệu finished với kết quả
        self.signals.finished.emit(result)
