import kaggle
import os



if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'EPA_Dataset')):
    os.mkdir("EPA_Dataset")

kaggle.api.authenticate()

kaggle.api.dataset_download_files('epa/carbon-monoxide', path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'EPA_Dataset'), unzip=True)
