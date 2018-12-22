import getpass,tempfile,os

THREAD_COUNT=4
TEMP_FILE_LOCATION=os.path.join(tempfile.gettempdir(),"pyr0-Downloader")

if os.name=="nt":
    DOWNLOAD_LOCATION=os.path.join(r"C:\Users",getpass.getuser(),"Downloads",r"pyr0-Downloader")
else:
    DOWNLOAD_LOCATION=os.path.join(os.path.expanduser("~"),"Downloads","pyr0-Downloader")