# get_post_with_bottle
Working with GET and POST requests to sqlite3 database with bottle and sqlalchemy in the middle.

All the processes are divided into two files:
1. work with http requests - server.py
2. work with database - DB_api.py

GET request gets the information from the DB.
POST request puts new information into the DB.

You can launch server.py and try it by sending requests with httpie. For example:
http -f GET http://localhost:8080/albums/queen                                                 
http -f POST http://localhost:8080/albums/ year=2006 artist="Pink" genre="pop-rock" album="Funhouse"
