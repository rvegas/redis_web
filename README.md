# Redis Web
  
This is a website implemented purely in flask using redis as a backend for static content and cms.
  
  
## Installation
  
Simply run the inserts located in `db` in your redis server and then run:
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
FLASK_APP=main.py flask run --reload
```
  
After that, go to http://localhost:5000 and have fun.
  
## Pending
  
- Add the posts page
- Add the registration page
- Add the followers page
- Add the token implementation
