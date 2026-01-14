from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.getenv('API_KEY')
os.environ['KAGGLE_KEY'] = API_KEY
os.environ['KAGGLE_USERNAME'] ='pradeepgubbala'
import kaggle 
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / 'scrapers'/'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

dataset = 'pradeepgubbala/employees-data'
download_path = RAW_DIR

kaggle.api.authenticate()
kaggle.api.dataset_download_file(dataset, file_name= 'employees_linkedin_data.csv', path=download_path)

# Renaming the file by adding today's date
today_date = datetime.now().date()

old_path = Path(RAW_DIR / 'employees_linkedin_data.csv')
new_path = Path(RAW_DIR / f'employees_linkedin_data_{today_date}.csv')

old_path.rename(new_path)


"""import os
from dotenv import load_dotenv
#from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime
from pathlib import Path
import re"""
"""export KAGGLE_API_TOKEN=KGAT_fb9b33e4ba9e56dd94fb8e274abc0195

load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)

#os.environ['KAGGLE_API_TOKEN'] = API_KEY
os.environ['KAGGLE_USERNAME'] ='pradeepgubbala'
api = KaggleApi()
api.authenticate()

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / 'scrapers'/'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

dataset = 'pradeepgubbala/employees-data'
download_path = RAW_DIR

# downloading the file
api.dataset_download_file(dataset, file_name= 'employees_linkedin_data.csv', path=download_path)

# Renaming the file by adding today's date
today_date = datetime.now().date()

old_path = Path(RAW_DIR / 'employees_linkedin_data.csv')
new_path = Path(RAW_DIR / f'employees_linkedin_data_{today_date}.csv')

old_path.rename(new_path)"""


"""import kagglehub
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / 'scrapers'/'data' / 'raw'
# Download latest version
path = kagglehub.dataset_download("pradeepgubbala/employees")

print("Path to dataset files:", path)"""


