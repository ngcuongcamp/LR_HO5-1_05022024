from ftplib import FTP
import os


def upload_image_to_ftp(image_path, ftp_server, ftp_user, ftp_password, ftp_directory):
    ftp = None
    try:
        ftp = FTP(ftp_server)
        ftp.login(user=ftp_user, passwd=ftp_password)

        ftp.cwd(ftp_directory)

        with open(image_path, "rb") as file:
            ftp.storbinary("STOR " + os.path.basename(image_path), file)

        print("Uploaded")
    except Exception as e:
        print("Have an error", e)
    finally:
        if ftp:
            ftp.quit()


image_path = "./test.py"
ftp_server = "10.222.48.86"
ftp_user = "ftpfiles"
ftp_password = "PASSword321"
ftp_directory = "/NguyenCuong/A"

upload_image_to_ftp(image_path, ftp_server, ftp_user, ftp_password, ftp_directory)
