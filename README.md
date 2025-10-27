# Testing Stopwords in uoguelph-engg4450-F24-Group8-NLTK

## 1. Install Python
Make sure Python 3 is installed on your system.  
To install using PowerShell (Windows 10/11), run:

```bash
winget install --id Python.Python.3.12 -e
```

Verify the installation:
```bash
python --version
```

If this command prints a version (e.g., Python 3.12.x), Python is installed successfully.

## 2. Clone the Repository
Use Git to clone the repository to your local machine:
```bash
git clone https://github.com/uoguelph-engg4450/uoguelph-engg4450-F24-Group8-NLTK.git
```

Navigate into the project folder:
```bash
cd uoguelph-engg4450-F24-Group8-NLTK
```

## 3. Create and Activate a Virtual Environment
Create a new virtual environment:
```bash
python -m venv venv
```

If this is your first time using PowerShell for Python, allow script execution:
```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Activate the virtual environment:
```bash
.env\Scripts\Activate.ps1
```

## 4. Install Dependencies
Install required packages:
```bash
pip install -e .\nltk
pip install pytest pytest-mock regex
```

## 5. Point NLTK to Local Data
Set the environment variable for NLTK data:
```bash
$env:NLTK_DATA = "$(Get-Location)\nltk_data\packages"
```

## 6. Run the Stopwords Test

### Expected FAIL (Original Stopwords)
```bash
$env:STOPWORDS_VERSION = "english"
pytest -q -s .\nltk\nltk\test\unit\test_stopwords_contractions.py
```
This test should fail, showing missing stopwords such as “ain’t”, “you’re”, and “shouldn’t”.

### Expected PASS (Modified Stopwords)
```bash
$env:STOPWORDS_VERSION = "modified"
pytest -q -s .\nltk\nltk\test\unit\test_stopwords_contractions.py
```
This test should pass, confirming that the modified stopwords list includes all contractions and slang terms.

To deactivate the environment when finished:
```bash
deactivate
```