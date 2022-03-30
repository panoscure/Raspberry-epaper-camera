from ftplib import FTP
from pathlib import Path
#import ftplib

def ftp_init():
    path = '/web/silver/camera_pictures/'
    address = "ftpip/name"
    port = 50
    user_name = "ftp_username"
    password = "ftp_password"
    return path, address, port, user_name, password

def send_file(local_path,file_name):
    path, address, port, user_name, password = ftp_init()
    print(path)
    #file_path = Path(file_name)
    #print(file_path)
    path = path+file_name
    print(path)

    ftp = FTP();
    #ftp = FTP(address)
    ftp.connect(address, port)
    ftp.login(user_name, password)
    with open(local_path, "rb") as file:
        ftp.storbinary('STOR %s' % path, file)


#    with FTP(address, user_name, password) as ftp, open(file_path, 'rb') as file:
#        ftp.storbinary(f'STOR {file_path.name}', file)

