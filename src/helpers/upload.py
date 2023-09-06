import os
import base64
from src.helpers.help import random_string

async def upload(base64String = None, uploadedDir = None):
    '''
        File will automatically uploaded inside ./cdn/{uploadedDir}
        if uploadedDir is None
        then file will saved in root folder of ./cdn
    '''
    callback = {
        "filename": None,
        "message": "Something went wrong when uploading file",
        "uploaded": False
    }

    if base64String is not None:
        try:
            # Create dir ./cdn
            CDN_FOLDER = "cdn"
            TARGET_DIR = CDN_FOLDER
            if not os.path.exists(CDN_FOLDER):
                os.makedirs(CDN_FOLDER)
            # Create {uploadedDir} if not None
            if uploadedDir is not None:
                TARGET_DIR = f'{CDN_FOLDER}/{uploadedDir}'
                if not os.path.exists(TARGET_DIR):
                    os.makedirs(TARGET_DIR)

            # Do upload file
            base64arr = base64String.split(";base64,")
            if len(base64arr) >= 2:
                extension = base64arr[0].split("/")
                if len(extension) >= 2:
                    filename = await random_string(10) + f'.{extension[1]}'
                    fullpath = f'{TARGET_DIR}/{filename}'

                    with open(fullpath, "wb") as fh:
                        fh.write(base64.decodebytes(base64arr[1].encode("utf-8")))

                    # Update callback
                    callback["filename"] = f'{TARGET_DIR}/{filename}'
                    callback["message"] = "File uploaded"
                    callback["uploaded"] = True
        except Exception as e:
            callback["message"] = str(e)
    else:
        callback["message"] = "Base64 cannot be empty"
    
    # Response
    return callback