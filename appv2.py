from flask import Flask, render_template, request, render_template_string, redirect, session

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'my_secret_key'

# Dictionary to store user signup information
users = {}

# Define a route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user is registered and the password is correct
        if username in users and users[username] == password:
            # If the credentials are correct, set a session variable to indicate the user is authenticated and redirect to x.html
            session['authenticated'] = True
            session['username'] = username
            return redirect('/profile')
        else:
            # If the credentials are incorrect, render the login form again with an error message
            return render_template_string('''
                <h1>Login</h1>
                <p>Incorrect username or password.</p>
                <form method="post">
                    <label>Username: <input type="text" name="username"></label><br>
                    <label>Password: <input type="password" name="password"></label><br>
                    <input type="submit" value="Login">
                </form>
            ''')
    else:
        # Render the login form
        return render_template_string('''
            <h1>Login</h1>
            <form method="post">
                <label>Username: <input type="text" name="username"></label><br>
                <label>Password: <input type="password" name="password"></label><br>
                <input type="submit" value="Login">
            </form>
        ''')
profiles = {}

# Define a route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        password = request.form['password']
     
        
        # Register the new user
        users[username] = password
        
        # Create a default profile for the new user
        profiles[username] = {
        'name': None,
        'bio': None,
        'profile_pic': 'https://example.com/new_default_profile_pic.jpg',
        'courses': ['math101', 'english101']
    }

        
        # Redirect to the login page
        return redirect('/login')
    else:
        # Render the signup form
        return render_template_string('''
            <h1>Sign Up</h1>
            <form method="post">
                <label>Username: <input type="text" name="username"></label><br>
                <label>Password: <input type="password" name="password"></label><br>
                <input type="submit" value="Sign Up">
            </form>
        ''')


# Define a route for profile page  that requires authentication
# Define a route for profile page that requires authentication
@app.route('/profile')
def profile():
    authenticated = session.get('authenticated', False)
    if authenticated:
        # Get the current user's username
        username = session.get('username', None)
        
        # Check if the user has a profile
        profile = profiles.get(username)
        if profile:
            # If the user has a profile, render their profile page
            return render_template('profile.html', profile=profile)
        else:
            # If the user does not have a profile, redirect them to the create profile page
            
            return redirect('/create_profile')

    else:
        return redirect('/login')


#Edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    authenticated = session.get('authenticated', False)
    if authenticated:
        username = session.get('username', None)
        if request.method == 'POST':
            print(request.form) # Add this line to see the form data that is being submitted
            # Update the user's profile
            profiles[username]['name'] = request.form['name']
            profiles[username]['bio'] = request.form['bio']
            profiles[username]['profile_pic'] = request.form['profile_pic']
            new_course = request.form['new_course']
            if new_course:
                # Add the new course to the user's profile
                profiles[username]['courses'].append(new_course)
            # Print the updated profile object
            print(profiles)
            # Redirect to the user's profile page
            return redirect('/profile')
        else:
            # Render the edit profile form
            profile = profiles.get(username, {})
            return render_template('edit_profile.html', profile=profile)
    else:
        return redirect('/login')











if __name__ == '__main__':
    app.run()