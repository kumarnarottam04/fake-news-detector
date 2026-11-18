import zipfile
import shutil
from pathlib import Path

workspace = Path(__file__).resolve().parent.parent
nltk_data_dir = workspace / 'data' / 'nltk_data' / 'corpora'
nltk_data_dir.mkdir(parents=True, exist_ok=True)

source_roaming = Path(r"C:\Users\kumar\AppData\Roaming\nltk_data\corpora")
wordnet_zip = source_roaming / "wordnet.zip"
stopwords_src = source_roaming / "stopwords"

print(f"Extracting {wordnet_zip} to {nltk_data_dir}...")
with zipfile.ZipFile(wordnet_zip, 'r') as zip_ref:
    zip_ref.extractall(nltk_data_dir)

print(f"Copying stopwords from {stopwords_src} to {nltk_data_dir / 'stopwords'}...")
if not (nltk_data_dir / 'stopwords').exists():
    shutil.copytree(stopwords_src, nltk_data_dir / 'stopwords')

print("NLTK data successfully unpacked inside workspace!")
