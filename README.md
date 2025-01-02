# Flask
- This is a side project using flask to mimic creating data from local database, getting data from local database, and fetching and syncing data from remote database.
- After running the file, please follow the step in each section to do the corresponding function. 

## (A) Create a User: 
- Command Prompt Command: curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d "{\"name\": \"John Doe\", \"email\": \"john.doe@example.com\"}" 

## (B) Get Users: 
- Command Prompt Command: curl http://127.0.0.1:5000/users 

## (C) Fetch external users: 
- Command Prompt Command: curl -X GET http://127.0.0.1:5000/external-users 

## (D) Sync external users: 
- Command Prompt Command: curl -X POST http://127.0.0.1:5000/sync-external-users

## Annotation: 
- In (A) and (B), local database is created at PostgreSQL. 
- In (C) and (D), response = requests.get('link'), link is the link to the external database. 
