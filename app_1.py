# Imports: The code imports necessary libraries: Flask for creating the web application, 
# request and jsonify for handling HTTP requests and responses, 
# psycopg2 for PostgreSQL database interaction, 
# and requests for making external API calls. 
from flask import Flask, request, jsonify 
import psycopg2 
import requests  # Import requests for external API calls. 

# App Initialization: An instance of the Flask application is created. 
app = Flask(__name__) 

# PostgreSQL Database connection 
def get_db_connection(): 
    conn = psycopg2.connect( 
        host = 'localhost', 
        database = 'internal_app', 
        user = 'postgres', 
        password = 'your_password' 
    ) 
    return conn 

# Define a route for the root URL歐
@app.route('/') 
def index(): 
    return jsonify({"message": "Welcome to the User API!"}) 

# Purpose: This function handles the creation of a new user. 
# It is mapped to the /users endpoint and accepts POST requests. 
@app.route('/users', methods = ['POST']) 
def create_user(): 
    # It retrieves JSON data from the request using request.json, 
    # extracting the name and email fields. 
    data = request.json 
    name = data['name'] 
    email = data['email'] 

    # A database connection is established using get_db_connection(), 
    # and a cursor is created for executing SQL commands. 
    conn = get_db_connection() 
    cur = conn.cursor() 

    # Check if the email already exists. 
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        return jsonify({"message": "Email already exists!"}), 400  # Return an error if the email is taken. 
    
    # Proceed to insert the new user. 
    # After committing the transaction, it closes the cursor and the database connection. 
    cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email)) 
    conn.commit() 
    cur.close() 
    conn.close() 

    # Finally, it returns a JSON response indicating that 
    # the user was created successfully with a 201 HTTP status code. 
    return jsonify({"message": "User created successfully!"}), 201 

# Purpose: This function retrieves all users from the database. 
# It is mapped to the /users endpoint and accepts GET requests. 
@app.route('/users', methods = ['GET']) 
def get_users(): 
    # A database connection is established using get_db_connection(), 
    # and a cursor is created for executing SQL commands. 
    conn = get_db_connection() 
    cur = conn.cursor() 

    # It executes a SELECT query to fetch all records from the users table. 
    # After retrieving the data, it closes the cursor and the database connection. 
    cur.execute('SELECT * FROM users;') 
    users = cur.fetchall() 
    cur.close() 
    conn.close() 

    # Format the output. 
    formatted_users = [{"id": user[0], "name": user[1], "email": user[2]} for user in users] 

    # Return the formatted list of users as a JSON response. 
    return jsonify(formatted_users) 

# Purpose: This helper function transforms user data from an external source into a specific format used by the application. 
# Function to transform user data. 
def transform_user(user): 
    return { 
        "name": user['full_name'], 
        "email": user['email_address'] 
    } 

# Purpose: This function retrieves external user data from a mock API. 
@app.route('/external-users', methods = ['GET']) 
def get_external_users(): 
    response = requests.get('https://run.mocky.io/v3/886409ea-2677-407c-82b4-e72296fb2046') 
    external_users = response.json() 
    return jsonify(external_users) 

""" 
The sync_external_users function is designed to synchronize user data from an external API into the local database. 
It checks for duplicates based on email addresses to prevent inserting the same user multiple times. 
The function effectively handles external data integration while ensuring data integrity in the local database. 
""" 

# Purpose: This function synchronizes external user data with the internal database. 
# sync_external_users function will be executed when a POST request is made to the /sync-external-users endpoint. 
@app.route('/sync-external-users', methods = ['POST']) 
def sync_external_users(): 
    # Fetch External Users. 
    # The function uses the requests library to make a GET request to a specified URL, 
    # which returns a list of external users in JSON format. 
    # The response is parsed into a Python dictionary (or list) using response.json(). 
    response = requests.get('https://run.mocky.io/v3/886409ea-2677-407c-82b4-e72296fb2046') 
    external_users = response.json() 

    # A database connection is established using get_db_connection(), 
    # and a cursor is created for executing SQL commands. 
    conn = get_db_connection() 
    cur = conn.cursor() 

    # Iterate Over External Users. 
    for user in external_users: 
        transformed_user = transform_user(user) 

        # Check if the email already exists. 
        cur.execute('SELECT * FROM users WHERE email = %s', (transformed_user['email'],)) 
        existing_user = cur.fetchone() 

        if existing_user: 
            # Optionally, you can log this or handle it as you see fit. 
            print(f"User with email {transformed_user['email']} already exists. Skipping.") 
            continue  # Skip to the next user if the email exists. 
        
        # Proceed to insert the new user. 
        cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (transformed_user['name'], transformed_user['email'])) 
    
    # Once all users have been processed, the changes are committed to the database. This step ensures that all insertions are saved. 
    # The cursor and database connection are closed to free up resources. 
    conn.commit() 
    cur.close() 
    conn.close() 

    # Return Response. 
    return jsonify({"message": "External users synced successfully!"}), 200 

# Purpose: This block checks if the script is run directly (not imported as a module). 
if __name__ == '__main__': 
    app.run(debug = True) 