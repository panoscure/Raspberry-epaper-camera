# epaper-camera

This is a project to take photo from raspberry pi camera, display it on e-Paper and upload it to an FTP.
Hardware to have:
1. Raspberry pi(zero w)
2. Raspberry Camera
3. 2.7 inch e-Paper HAT

Features:
1. Press key1 to take photo
2. Press key2 to view list of photos taken/ With every next click list with pictures is rotating one at the time. 
3. Press key3 to display or delete Photo, when you are on the images list, with first click you display the image and with second click you delet it. to return back click key2
4. View Raspberry details(Bonus feature). Raspberry IP/Nework Name/CPU usage/Memory usage/Hard disk usage/Raspberry pi model


Configuration:
Edit file "ftp_upload.py" and fill the following variables
1. path: path to your FTP
2. address: FTP ip or name
3. port: FTP port
4. user_name: Your FTP user name
5. password: Your FTP password

Edit file "camera.py" and update the following variable
1. images_path: the local path where you keep your images
