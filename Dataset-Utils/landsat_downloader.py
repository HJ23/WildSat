#
#
#                                WildSat
#            This script will download landsat images from the google-drive.
#            
#
#


import gdown
import os


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LandSat')


BASE_URL = 'https://drive.google.com/uc?id={}'

REGIONS = {
    'Oceania': '1xHYTICHKU0u3-kIrq-pM9k0YaeQt60Bt', 
    'North_America1': '1BXRGldTdGGNeWDOFqNnmiNPuPQjweB2M', 
    'North_America2': '1zW_pEIggJ5Li7uQX9XKMfHkcgL3kiUoi', 
}


def download_file(file_id, output):
    url = BASE_URL.format(file_id)
    print('Downloading: {}'.format(url))
    gdown.download(url, output,quiet=False)


if __name__ == '__main__':

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for region in REGIONS:
        zip_file_name = '{}.zip'.format(region)
        output = os.path.join(OUTPUT_DIR, zip_file_name)
        download_file(REGIONS[region], output)
