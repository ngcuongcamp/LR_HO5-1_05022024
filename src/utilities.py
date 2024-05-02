from libs.libs import (
    datetime,
    configparser,
    os,
    shutil,
    json,
    time,
    logging,
    init,
    AnsiToWin32,
    Fore,
    sys,
)

#! utility function

config = configparser.ConfigParser()
config.read("./config.ini")

# custom cmd color
init(autoreset=True)
stream = AnsiToWin32(sys.stderr).stream


def cmd_printer(type: str, msg: str):
    if type == "WARNING":
        print(Fore.YELLOW + msg, file=stream)
    elif type == "ERROR":
        print(Fore.RED + msg, file=stream)
    elif type == "SUCCESS":
        print(Fore.GREEN + msg, file=stream)
    elif type == "INFO":
        # print(Fore.WHITE + msg, file=stream)
        print(msg)


def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def format_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H-%M-%S")
    return formatted_time


def create_daily_folders():
    path = config["PATH"]["IMAGE_NG_FOLDER"]
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(path, current_date)
    for camera_folder in ["CAMERA1", "CAMERA2"]:
        os.makedirs(os.path.join(folder_path, camera_folder), exist_ok=True)


def handle_remove_old_folders():
    folder_to_keep = int(config["SETTING"]["FOLDER_TO_KEEP"])
    path = config["PATH"]["IMAGE_NG_FOLDER"]
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    subfolders.sort()
    if len(subfolders) > folder_to_keep:
        folders_to_delete = subfolders[: len(subfolders) - folder_to_keep]
        for folder_to_delete in folders_to_delete:
            try:
                shutil.rmtree(folder_to_delete)
                print(f"Removed old folder: {folder_to_delete}")
            except Exception as e:
                cmd_printer("ERROR", f"Remove error '{folder_to_delete}': {e}")


def setup_logger():
    path_dir_log = "./logs/"
    time_day = time.strftime("%Y_%m_%d")
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(f"{path_dir_log}{time_day}.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger


def read_config(self):
    # serial port config
    self.COM_PLC = config["PLC"]["COM"]
    self.BAUDRATE_PLC = config["PLC"]["BAUDRATE"]

    # option settings
    self.ID_C1 = int(config["CAMERA"]["IDC1"])
    self.ID_C2 = int(config["CAMERA"]["IDC2"])
    self.SCAN_LIMIT = int(config["SETTING"]["SCAN_LIMIT"])
    self.NUM_CAMERA = int(config["SETTING"]["NUM_CAMERA"])
    self.IS_SAVE_NG_IMAGE = int(config["SETTING"]["IS_SAVE_NG_IMAGE"])
    self.IS_OPEN_CAM_PROPS = int(config["SETTING"]["IS_OPEN_CAM_PROPS"])

    self.IS_USE_DYNAMIC_FRAME = int(config["SETTING"]["IS_USE_DYNAMIC_FRAME"])
    self.IS_USE_MINIMIZE = int(config["SETTING"]["IS_USE_MINIMIZE"])
    self.IS_USE_SNAPSHOT_OLD_SN = int(config["SETTING"]["IS_USE_SNAPSHOT_OLD_SN"])
    self.TIME_TO_HIDE_WINDOW = float(config["SETTING"]["TIME_TO_HIDE_WINDOW"])
    self.TIME_TO_REOPEN = float(config["SETTING"]["TIME_TO_REOPEN"])
    self.IS_USE_REPAINT = int(config["SETTING"]["IS_USE_REPAINT"])
    self.IS_USE_AUTOCLICK = int(config["SETTING"]["IS_USE_AUTOCLICK"])

    self.PROP_EXPOSURE_1 = int(config["SETTING"]["PROP_EXPOSURE_1"])
    self.PROP_EXPOSURE_2 = int(config["SETTING"]["PROP_EXPOSURE_2"])

    # Process image config
    # self.BLOCK_SIZE_1 = int(config["THRESH"]["BLOCK_SIZE_1"])
    # self.BLOCK_SIZE_2 = int(config["THRESH"]["BLOCK_SIZE_2"])
    # self.C1 = int(config["THRESH"]["C1"])
    # self.C2 = int(config["THRESH"]["C2"])

    self.MIN_THRESH_1 = int(config["THRESH"]["MIN_THRESH_1"])
    self.MAX_THRESH_1 = int(config["THRESH"]["MAX_THRESH_1"])
    self.SPACE_THRESH_1 = int(config["THRESH"]["SPACE_THRESH_1"])

    self.MIN_THRESH_2 = int(config["THRESH"]["MIN_THRESH_2"])
    self.MAX_THRESH_2 = int(config["THRESH"]["MAX_THRESH_2"])
    self.SPACE_THRESH_2 = int(config["THRESH"]["SPACE_THRESH_2"])

    # MES config
    self.TIME_SLEEP = float(config["MES"]["TIME_SLEEP"])
    self.WAIT_TIME = float(config["MES"]["WAIT_TIME"])
    self.MES_APP_NAME = config["MES"]["MES_APP_NAME"]
    self.MES_BACKEND = config["MES"]["BACKEND"]
    # self.POSITION_SN = json.loads(config["MES"]["POSITION_SN"])

    self.PERCENT_MATCHING_1 = float(config["MES"]["PERCENT_MATCHING_1"])
    self.PERCENT_MATCHING_2 = float(config["MES"]["PERCENT_MATCHING_2"])
    self.PERCENT_MATCHING_3 = float(config["MES"]["PERCENT_MATCHING_3"])
    self.PERCENT_MATCHING_4 = float(config["MES"]["PERCENT_MATCHING_4"])

    self.ACCEPT_REPETITIVE = int(config["SETTING"]["ACCEPT_REPETITIVE"])
    self.ACCEPT_REOPEN_APP = int(config["SETTING"]["ACCEPT_REOPEN_APP"])
    self.APP_PATH = config["PATH"]["APP_PATH"]

    # SIGNALS TO PLC
    self.PASS_SIGNAL = config["SIGNALS"]["PASS_SIGNAL"].encode("utf-8")
    self.FAIL_SIGNAL = config["SIGNALS"]["FAIL_SIGNAL"].encode("utf-8")


handle_remove_old_folders()
create_daily_folders()
logger = setup_logger()
