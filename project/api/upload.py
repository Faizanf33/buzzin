import os
import random
import string
import base64
import logging
from functools import wraps
from flask import jsonify, request
from project.api.utils import secure_file, upload_file

"""
    Decorator to upload files to the server and return the file path

    :param f: function to be decorated
    :return: decorated function
"""

logger = logging.getLogger(__name__)


def upload(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            "status": False,
            "message": "Please provide a valid file."
        }

        if "file" not in request.files:
            return jsonify(response_object), 400

        file = request.files["file"]

        if file and file.filename == "":
            return jsonify(response_object), 400

        if allowed_file(file.filename):
            secured_file = secure_file(file)
            filename = secured_file["filename"]

            # get current path
            current_path = os.path.dirname(os.path.abspath(__name__))
            file_path = os.path.join(current_path, filename)
            logger.info("File path: {}".format(file_path))

            # read binary file and encode it to base64
            with open(file_path, mode="rb") as img:
                imgstr = base64.b64encode(img.read())

            # upload file
            response = upload_file(imgstr, filename)
            object_url = response.url

            logger.info("File uploaded successfully: {}".format(object_url))

            # delete file locally
            os.remove(filename)

            return f(object_url, *args, **kwargs)

            # filename = secure_filename(file.filename)

            # # create the upload folder if it does not exist
            # upload_folder = os.getenv("UPLOAD_FOLDER")
            # os.makedirs(upload_folder, exist_ok=True)

            # # append the random string to the end of the filename
            # filename = f"{filename.rsplit('.', 1)[0]}_{random_string()}.{filename.rsplit('.', 1)[-1]}"

            # # save the file to the server
            # file.save(os.path.join(upload_folder, filename))

            # # return the relative path to the file
            # return f(
            #     os.path.join(
            #         os.getcwd(),
            #         upload_folder,
            #         filename
            #     ), *args, **kwargs
            # )

    return decorated_function


def allowed_file(filename: str) -> bool:
    ALLOWED_EXTENSIONS = set([
        "pdf", "png", "jpg", "jpeg", "heic", "heif", "tiff", "tif", "gif", "svg"
    ])
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def random_string(length: int = 10) -> str:
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
