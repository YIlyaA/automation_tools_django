# 6 Essential Automation Tools Django

## Features
### 1. **DATA IMPORT:**          
   **This feature streamlines the process of importing data by allowing users to upload CSV files directly into the database. It is highly effective for handling large datasets, utilizing background processing with Celery to ensure smooth, efficient imports without slowing down the application.**     
   *P.S. Usage in the console:
   `python manage.py importdata <path_to_csv_file> <model_name>`*

### 2. **DATA EXPORT:**          
   **This feature allows users to easily extract and download data from their database in CSV format.**     
   *P.S. Usage in the console:
   `python manage.py exportdata <model_name>`*

### 3. **BULK EMAILS:**          
   **This tool allows users to efficiently send personalized emails to large groups of recipients simultaneously. It is ideal for marketing campaigns, newsletters, and announcements, ensuring timely delivery and improved outreach.**     

### 4. **Complete Email Tracking System with Open Rate & Click Rate:**          
   **This system monitors and analyzes email performance by tracking open rates and click rates, providing insights into recipient engagement. It helps users optimize their email campaigns by identifying which messages are most effective.**     

### 5. **COMPRESS IMAGES:**          
   **This tool reduces the file size of images by a chosen percentage of compression. It supports various image formats like JPEG, PNG, JPG, allowing users to optimize images for faster website loading times, reduced storage usage, and quicker sharing.**

### 6. **STOCK MARKET ANALYSIS TOOL:** 
   **This tool collects and displays up-to-date stock market data from various exchanges, helping users track price movements, market trends, and key financial metrics.**

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
SENDINBLUE_API_KEY=your_sendinblue_api_key
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

4. Ngrok (you can test the website using ngrok):       
Instalation guide: *https://ngrok.com/downloads*
----
<br/>

## Troubleshooting
### **1. VIRTUAL ENVIROMENT ACTIVATION ISSUE**
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
<br/>

### **2. PORT FOR REDIS ALREADY IN USE**
In case the port 6379 is already in use, you may get the warning something like below:
```powershell
(env) PS <PATH>
[11528] <date> # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
[11528] <date> # Redis version=5.0.14.1, bits=64, commit=ec77f72d, modified=0, pid=11528, just started
[11528] <date> # Warning: no config file specified, using the default config. In order to specify a config file use c:\program files\redis\redis-server.exe 
/path/to/redis.conf
[11528] 14 Dec 11:24:55.215 # Could not create server TCP listening socket *:6379: bind: An operation was attempted on something that is not a socket.
```
**Solution::**
1. Check which process is running on port 6379.
```powershell
netstat -ano | findstr :6379.
```
2. Kill this process (Note: Here 15916 is the PID received in above command. Run this command as an Administrator):
```powershell
taskkill /F /PID 15916
```

