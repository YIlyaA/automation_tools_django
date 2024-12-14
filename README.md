# 6 Essential Automation Tools Django

## Features
### 1. **DATA IMPORT:**          
   **Import data from CSV files directly into your database using a Django management command.**     
   **Usage:**
   ```bash
    python manage.py importdata <path_to_csv_file> <model_name>
   ```

### 2. **DATA EXPORT:**          
   **Export data from your database to a CSV file.**     
   **Usage:**
   ```bash
    python manage.py exportdata <model_name>
   ```

----
<br/>

## How to Run Locally:
### Step 1: Set up the environment
**1. Create and activate a virtual environment:**
```bash
python -m venv env
.\env\Scripts\activate   # For Windows
source env/bin/activate  # For MacOS/Linux

```
**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up .env file:**
```py
SECRET_KEY=YOUR_KEY
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=db.sqlite3

# email configuration 
EMAIL_HOST=smtp.gmail.com                 # or your preferred SMTP server 
EMAIL_PORT=587                            # 587 for gmail
EMAIL_HOST_USER=YOUR_EMAIL_ADDRESS    
EMAIL_HOST_PASSWORD=YOUR_EMAIL_PASSWORD    
```
*P.S. if you are using gmail, you need to enable 2FA, then go to `Manage your Google Account → Security → 2FA → App Passwords`, Generate an App Password and use it as EMAIL_HOST_PASSWORD*

**4. Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```


### Step 2: Start the necessary services

**You will need three terminals open:**
1. Start the Django server:
```bash
python manage.py runserver
```

2. Start the Redis server:
```bash
redis-server
```

3. Start Celery:
```bash
celery -A awd_main worker --loglevel=info --pool=solo    # For Windows
celery -A awd_main worker --loglevel=info                # For Linux
```

----
<br/>

## Troubleshooting
### 1. Virtual Environment Activation Issue
If you encounter the following error when activating your virtual environment:
```powershell
<PATH> cannot be loaded because running scripts is disabled on this system. For more information, see 
about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .\env\Scripts\activate
```
**Solution::**
1. Open PowerShell as an Administrator.
2. Run the following command to bypass execution policy restrictions:
```powershell
powershell -ExecutionPolicy Bypass
```
