# twireport
An application using Twitter streaming API to generate reports about different aspects.

# Getting started
You should have the following packages installed **system-wide**
- Python
- Pip
- Virtualenv
- Redis

## The init
In order to initialize the project, follow the commands written below in the exact sequence:
1. git clone https://github.com/shivan1b/twireport.git
2. virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt

Now, your project should have been initialized with all the requirements.

## Connecting to Twitter API
Making use of Twitter's API will require credentials for authenticating the app for using the API. Get your authentication credentials here: https://apps.twitter.com/ after giving your app a fancy new name.
Following this, create a file named .env in the root of the project and add the following variables and their corresponding values that you received from Twitter:
```
ACCESS_TOKEN='my_access_token'
ACCESS_SECRET='my_access_secret'
CONSUMER_KEY='my_consumer_key'
CONSUMER_SECRET='my_consumer_secret'
```
