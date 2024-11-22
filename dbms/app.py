from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'template'))  # Ensure template folder path is correct
app.secret_key = 'lakshmi'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'welcome 123'  # Your MySQL password
app.config['MYSQL_DB'] = 'singer'  # Your MySQL database name
mysql = MySQL(app)

# Home Route (index)
@app.route('/')
def index():
    return render_template('home.html')  # Ensure 'home.html' exists in the templates folder

# Route to view all singers or search for a specific singer by ID
@app.route('/singers', methods=['POST', 'GET'])
def singers():
    if request.method == 'POST':
        # Handle the search functionality
        search_term = request.form['singer_id']  # Get the search term from the form
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM singers WHERE id LIKE %s"  # Query to search by singer ID
            cur.execute(query, ('%' + search_term + '%',))  # Search query with LIKE operator
            search_results = cur.fetchall()  # Fetch the search results
            cur.close()  # Close the cursor
            return render_template('singers.html', singers=search_results)  # Render the singers.html with the search results
        except Exception as e:
            return f"Error: {e}"  # Return error message if an exception occurs
    else:
        # Handle the display of all singers
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM singers")  # Fetch all singers from the 'singers' table
            singers_info = cur.fetchall()  # Fetch all records
            cur.close()  # Close the cursor after the operation
            return render_template('singers.html', singers=singers_info)  # Render the singers.html template with fetched data
        except Exception as e:
            return f"Error: {e}"  # If there's an error, show it

# Route to insert a new singer
@app.route('/insert_singer', methods=['POST'])
def insert_singer():
    if request.method == "POST":
        singer_id = request.form['singer_id']
        name = request.form['name']
        email = request.form['email']
        genre = request.form['genre']
        
        # Validate input
        if not singer_id or not name or not email or not genre:
            return "Please fill all fields"  # Error message if any field is empty
        
        try:
            cur = mysql.connection.cursor()
            # Insert the new singer into the 'singers' table
            cur.execute("INSERT INTO singers (id, name, email, genre) VALUES (%s, %s, %s, %s)", 
                        (singer_id, name, email, genre))
            mysql.connection.commit()  # Commit the transaction
            cur.close()  # Close the cursor
            return redirect(url_for('singers'))  # Redirect to the singers page to see the updated list
        except Exception as e:
            return f"Error: {e}"  # Return error message if an exception occurs

# Route to delete a singer by ID
@app.route('/delete_singer/<string:singer_id>', methods=['GET'])
def delete_singer(singer_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM singers WHERE id = %s", (singer_id,))  # Delete singer by their ID
        mysql.connection.commit()  # Commit the deletion
        cur.close()  # Close the cursor
        return redirect(url_for('singers'))  # Redirect to the singers page after deletion
    except Exception as e:
        return f"Error: {e}"  # Return error message if an exception occurs

# Route to update an existing singer's details
@app.route('/update_singer/<string:singer_id>', methods=['POST', 'GET'])
def update_singer(singer_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        genre = request.form['genre']
        
        # Validate input
        if not name or not email or not genre:
            return "Please fill all fields"  # Error message if any field is empty
        
        try:
            cur = mysql.connection.cursor()
            # Update the singer's details based on their ID
            cur.execute("UPDATE singers SET name = %s, email = %s, genre = %s WHERE id = %s", 
                        (name, email, genre, singer_id))
            mysql.connection.commit()  # Commit the update
            cur.close()  # Close the cursor
            return redirect(url_for('singers'))  # Redirect to the singers page after update
        except Exception as e:
            return f"Error: {e}"  # Return error message if an exception occurs

    else:
        try:
            # Fetch the existing data for the singer to pre-fill the form
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM singers WHERE id = %s", (singer_id,))
            singer = cur.fetchone()  # Fetch the singer record
            cur.close()  # Close the cursor
            return render_template('update_singer.html', singer=singer)  # Render the update form with fetched data
        except Exception as e:
            return f"Error: {e}"  # Return error message if an exception occurs

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
