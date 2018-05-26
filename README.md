# twireport
An application using Twitter streaming API to generate reports about different aspects.


# Getting started
You should have the following packages installed **system-wide**
- Python 3
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

## Third Part packages
This project makes use of `nltk` python package which requires download of dataset in the following manner.
```
$ ▶ ipython
Python 3.6.5 (default, May 11 2018, 04:00:52) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import nltk

In [2]: nltk.download()
```

# Get the data stream coming
In order to run the program, get into the root directory of the project and type,
```
$ ▶ python pilot.py
```
You shall now be prompted for the keyword you'd like to stream Twitter for
```
Please enter the keyword which you'd like to track:
linux
```
After typing the keyword, press enter and open up another terminal to type
```
 $ ▶ python stream.py 
```
and wait for `Twireport` to generate beautiful reports for you.


# Sample Report
`Twireport` shall generate a report similar to below on the console where you ran `stream.py`
```

```


# Improvements
Following are the improvements that I see can be made.
1. `pilot.py` could be run as a daemon. Then, `stream` could be used as a command.
2. Performance improvements for very large datasets.


# Contributing
If you find any issue with the current implementation or have a more optimized solution, please consider sending a Pull Request. Make sure to have a different and descriptive name for your branch.
