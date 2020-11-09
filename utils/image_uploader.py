import os
import time

from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary

from config import CLOUD_KEY, CLOUD_SECRET, CLOUD_NAME


cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key = CLOUD_KEY,
    api_secret = CLOUD_SECRET
    )

def upload_file(filepath):
    """
    Uploads files to Cloudinary
    https://github.com/cloudinary/pycloudinary/blob/master/samples/basic/basic.py
    """
    fname = filepath.split('/')[-1][:-4]

    response = upload(filepath,
                      public_id=fname,
                      use_filename=True)
    for key in sorted(response.keys()):
        print(key, response[key])

    url, options = cloudinary_url(response['public_id'],
                                  format=response['format'])
    print('URL: ', url)


def upload_dir(dir_path):
    """
    Upload all files from dir_path to Cloudinary
    """
    fnames = os.listdir(dir_path)
    for i, fname in enumerate(fnames):
        print(f'Uploading file number: {i}')
        filepath = os.path.join(dir_path, fname)
        upload_file(filepath)
        time.sleep(0.1)





if __name__ == '__main__':
    upload_dir('./media/scaled_images')