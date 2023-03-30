from flask import Flask, request, render_template_string, redirect, session

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
            'name': 'None',
            'bio': 'None',
            'profile_pic': 'https://example.com/default_profile_pic.jpg'
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
@app.route('/profile')
def x():
    authenticated = session.get('authenticated', False)
    if authenticated:
        # Get the current user's username
        username = session.get('username', None)
        
        # Check if the user has a profile
        if username in profiles:
            # If the user has a profile, render their profile page
            profile = profiles[username]
            return render_template_string('''
                <h1>ProfilePageTest</h1>
                <p>Name: {{ profile.name }}</p>
                <p>Bio: {{ profile.bio }}</p>
                <img src="{{ profile.profile_pic }}" alt="Profile Picture">
            ''', profile=profile)
        else:
            # If the user does not have a profile, redirect them to the create profile page
            return redirect('/create_profile')

    else:
        return redirect('/login')


# Define a route for the editing profile page
@app.route('/edit_profile', methods=['GET', 'POST'])
def create_profile():
    authenticated = session.get('authenticated', False)
    if authenticated:
        # Get the current user's username
        username = session.get('username', None)
        
        if request.method == 'POST':
            # Handle form submission
            name = request.form['name']
            bio = request.form['bio']
            profile_pic = request.form['profile_pic']
            
            # Update the user's profile
            profiles[username]['name'] = name
            profiles[username]['bio'] = bio
            profiles[username]['profile_pic'] = profile_pic
            
            # Redirect to the user's profile page
            return redirect('/profile')
        else:
            # Render the create profile form
            return render_template_string('''
                <h1>Create Profile</h1>
                <form method="post">
                    <label>Name: <input type="text" name="name"></label><br>
                    <label>Bio: <textarea name="bio"></textarea></label><br>
                    <label>Profile Picture URL: <input type="text" name="profile_pic"></label><br>
                    <input type="submit" value="Save">
                </form>
            ''')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run()