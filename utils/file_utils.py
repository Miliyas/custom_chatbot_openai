import os
import shutil
from glob import glob

def save_uploaded_files(uploaded_files, tmp_directory):
    if os.path.exists(tmp_directory):
        shutil.rmtree(tmp_directory)
    os.makedirs(tmp_directory)

    for file in uploaded_files:
        with open(f"{tmp_directory}/{file.name}", 'wb') as temp:
            temp.write(file.getvalue())
            temp.seek(0)

def get_uploaded_files(tmp_directory):
    return [path.split(os.path.sep)[-1] for path in glob(tmp_directory + '/*')]
