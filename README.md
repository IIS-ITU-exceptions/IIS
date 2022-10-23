# IIS

Smart City website. \
Team project for the "IIS - Information Systems" subject. 

## Local Setup
Install and start a MySQL server on your machine and create a database named `smartcity`.\
After that copy the environment variable overrides file like so `cp .env.example .env`. \
Edit the `DATABASE_URI` variable in `.env` to match your MySQL setup and run these next few commands:
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0
```
