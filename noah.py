# Project Backup Script ver 0.0.1
# Jeff Dickson Oct 1, 2022
# The intent is to create a script that will make copies of projects onto whatever medium you point it at

import os, sys, shutil, noahSources, logging, tdqm, socket, zipfile
from shutil import SameFileError
from datetime import date

arkName = "ARK"

def _logpath(path, names):
    logging.info('Working in %s' % path)
    return []   # nothing will be ignored

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

print("Begining file backup process")

#Clear the path for the new backup
for root, dirs, files in os.walk(noahSources.arkLocation):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

for i in range(0,len(noahSources.directory)):
    print("Working on directory " + str(i))
    shutil.copytree(noahSources.directory[i], noahSources.arkLocation + arkName + " " + str(date.today()) + "/Animal" + str(i), ignore=_logpath)
    # try:
        # shutil.copytree(noahSources.directory[i], noahSources.arkLocation + arkName + str(date.today()))
    # except SameFileError:
        # print("Error copying " + str(noahSources.directory[i]) + "we are attempting to copy the same file")
    # except IsADirectoryError:
        # print("Error copying " + str(noahSources.directory[i]) + "the destination is a directory")
    #If flag is present we can send the data to a computer preferably over a LAN network, at the moment the process IS NOT encrypted. [UNTESTED]
    if noahSources.remoteSend == True:
        #We should zip up the directory first
        zipName = "Animal" + str(i) + ".zip"
        zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED) #Creates a file in the current directory called Animal{i}.zip
        zipdir('./my_folder', zipf)
        zipf.close()
        
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step
        # the ip address or hostname of the server, the receiver
        host = noahSources.remoteArk
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = zipName
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        s.close()
        #Delete zipped file on local machine
    else:
    print("Network send not set, skipping...")

    

print("Process complete")
