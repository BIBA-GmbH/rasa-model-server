from os import environ

# --- Connection-related variables.
server_port = environ.get('PORT', 8080)

# --- Download-related variables.
download_folder = environ.get('DOWNLOAD_FOLDER', 'models')

# --- Upload-related variables.
# Default upload folder is the model's folder.
upload_folder = environ.get('UPLOAD_FOLDER', download_folder)

allowed_extension = environ.get(
    'ALLOWED_EXTENSIONS',
    {
        'gz',
    }
)

# Maximum allowed file size in MB
maximum_file_size = 150 * 1000 * 1000
