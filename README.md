# URL OF LIVE APP:  https://ankit-jailwal.github.io/Palo-Alto-Frontend/#/login

Command to test complete API flow : python manage.py test 

## Django based chat app : 
https://github.com/Ankit-jailwal/Palo-Alto-Chat-App/tree/auth_flow

## Web Socket using Node.js : 
https://github.com/adefemi/chatApp-socket

## Frontend using react: 
https://github.com/Ankit-jailwal/Palo-Alto-Frontend

## How to run:
1. Go to django root project
2. Run pip install requirements.txt
3. Run python manage.py makemigrations
4. Run python manage.py migrate
5. Run python manage.py runserver
6. Run python manage.py test (To test all API endpoints)
7. Go to root of socket project(https://github.com/Ankit-jailwal/Palo-Alto-Socket)
8. Run npm start (This will create live web socket  between host and client)
9. Then open this URL for frontend https://ankit-jailwal.github.io/Palo-Alto-Frontend/#/login

## Tech Used:
AWS S3 bucket for storing files
Django for creating backend APIs
React for frontend
Github hosting for deployment

## NOTE: Tried to deploy backend to Digital Ocean using docker container of backend project and using CloudFlare DNS but could not do it in given time constraints
 
Created endpoints for several API testing like:
Test generic functions
Test authentication
Test User info
Test message flow
Test File upload

## Features: 
1. Complete backend
2. Contains test cases in test.py for testing each API
3. Hosted on github
4. End to end encrypted
5. P2p chat supported
6. File transfer supported
7. File stored on S3 Bucket on local storage
8. Is online feature supported
9. Message count can be seen
10. Complete authentication flow
11. Contains admin portal where details of each user can be seen and managed at /admin
 Follows OWASP
