import os

from flask import Flask, render_template, send_from_directory, abort, request
from werkzeug.utils import secure_filename

from os import sep
from os.path import isdir, dirname, basename, relpath, join, exists

from config import (
    download_folder,
    server_port,
    upload_folder,
    allowed_extension,
    maximum_file_size
)

from filesystem import Scaner


app = Flask(__name__)

# https://flask.palletsprojects.com/en/1.1.x/config/#SEND_FILE_MAX_AGE_DEFAULT
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_CONTENT_LENGTH'] = maximum_file_size
app.config['DOWNLOAD_FOLDER'] = download_folder
app.config['UPLOAD_FOLDER'] = upload_folder


@app.route('/', methods=['GET'])
def index():
    return list_dir(download_folder)


@app.route('/<path:path>', methods=['GET'])
def download_file(path):

    fetch_latest = '@latest' in path
    real_path = join(download_folder, path.replace('@latest', ''))

    if not exists(real_path):
        return 'Not Found', 404

    if ".." in real_path:
        return 'Not Found', 404

    if isdir(real_path):

        if fetch_latest:
            latest_entry = Scaner(real_path).latest_entry

            if not latest_entry:
                return 'No model found', 404

            return securly_serve_file(latest_entry.path)

        else:
            return list_dir(real_path)
    else:
        return securly_serve_file(real_path)


# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
@app.route('/models/<filename>', methods=['POST'])
def upload_file(filename):
    if request.method == 'POST':

        print(request.__dict__)

        # check if the request has data (the file).
        if request.files['model']:
            file = request.files['model']
        else:
            # Return 400 BAD REQUEST.
            abort('No model file in request', 400)

        # If the request contains empty file name.
        if filename == '':
            # Return 400 BAD REQUEST
            abort('File name empty', 400)

        if "/" in filename:
            # Return 400 BAD REQUEST.
            abort(400, "No sub-directories allowed")

        # If file extension not allowed.
        if file and allowed_file(filename):
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Return 201 CREATED.
            return "", 201
        else:

            print(request.form)
            # Return 400 BAD REQUEST.
            abort(400, "Extension not allowed.")
    else:
        abort(400, "Only POST requests allowed.")


def list_dir(path):
    rel_path = relpath(path, download_folder)
    parent_path = dirname(rel_path)
    entries = Scaner(path).entries

    return render_template(
        'index.html',
        sep=sep,
        parent_path=parent_path,
        path=rel_path,
        entries=entries
    )


# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
def securly_serve_file(path):
    ''' Serves the requested file securly. '''

    return send_from_directory(
        dirname(path),
        basename(path),
        as_attachment=True,
        download_name=basename(path),
        max_age=0
    )


# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
def allowed_file(filename):
    ''' Returns True if the filename has an allowed extension. '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extension


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
