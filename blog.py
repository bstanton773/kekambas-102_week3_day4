class Blog:
    def __init__(self):
        self.users = set()
        self.posts = []
        self.current_user = None # attribute used to determine if there is a logged in user

    def _get_post_from_id(self, post_id):
        for post in self.posts:
            if post.id == int(post_id):
                return post
        
    # Method to add new users to the blog
    def create_new_user(self):
        # Get user info from input
        username = input('Please enter a username: ')
        # Check if there is a user that already has that username
        if username in {u.username for u in self.users}:
            print(f"User with username {username} already exists")
        else:
            # Get password
            password = input('Please enter a password: ')
            # Create a new User instance with info from user input
            new_user = User(username, password)
            # Add user instance to the blog user set
            self.users.add(new_user)
            print(f"{new_user} has been created!")
            
    # Method to log a user in
    def log_user_in(self):
        # Get user credentials
        username = input('What is your username? ')
        password = input('What is your password? ')
        # Loop through each user in the blog
        for user in self.users:
            # Check is a user has the same username and the password word check passes
            if user.username == username and user.check_password(password):
                # If user has correct credentials, set the blog's current user to that user instance
                self.current_user = user
                print(f"{user} has been logged in")
                break
        # If no users in our blog user list have correct username/password, let them know
        else:
            print('Username and/or Password is incorrect.')
                  
    # Method to log a user out
    def log_user_out(self):
        # Change the current_user attribute from the user to None
        self.current_user = None
        print('You have successfully logged out')
        
    # Method to create and add post to blog
    def create_post(self):
        # Check to make sure the user is logged in before creating post
        if self.current_user is not None:
            # Get the title and body from user input
            title = input('Enter the title of your post: ').title()
            body = input('Enter the body of your post: ')
            # Create a new Post instance with user input
            new_post = Post(title, body, self.current_user)
            # Add the new post to the blog's list of posts
            self.posts.append(new_post)
            print(f"{new_post.title} has been created!")
        else:
            print("You must be logged in to perform this action")

    # Method to view all posts in the blog
    def view_posts(self):
        # Check to see if there are any posts
        if self.posts:
            # Loop through all of the posts
            for post in self.posts:
                # Display the post via print
                print(post)
        else:
            print("There are currently no posts for this blog :(")

    # Method to view a single post by its ID
    def view_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with an ID of {post_id} does not exist")


    # Method to edit a single post
    def edit_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            # Check that the user is logged in AND that the logged in user is the owner of this post
            if self.current_user is not None and self.current_user == post.author:
                print(post)
                # Ask the user which part of the post they would like to edit
                edit_part = input("Would you like to edit the title, body, both, or exit? ").lower()
                # Make sure the user response is valid
                while edit_part not in {'title', 'body', 'both', 'exit'}:
                    edit_part = input("Invalid. Please choose title, body, both, or exit")
                # if the user puts exit, exit the function
                if edit_part == 'exit':
                    return
                elif edit_part == 'both':
                    # Get a new title and body
                    new_title = input('Enter the new title: ').title()
                    new_body = input('Enter the new body: ')
                    # Edit the post with the post.update method
                    post.update(title=new_title, body=new_body)
                elif edit_part == 'title':
                     # Get a new title
                    new_title = input('Enter the new title: ').title()
                    post.update(title=new_title)
                elif edit_part == 'body':
                    # Get a new body
                    new_body = input('Enter the new body: ')
                    post.update(body=new_body)

                print(f"{post.title} has been updated")
            # If the user is logged in but not the owner of the post
            elif self.current_user != post.author:
                print("You do not have permission to edit this post") # 403 HTTP Status Code
            # If the user is not logged in
            else:
                print("You must be logged in to perform this action") # 401 HTTP Status Code
        else:
            print(f"Post with an ID of {post_id} does not exist") # 404 HTTP Status Code


    # Method to delete a single post
    def delete_post(self, post_id):
        # Get the post by id or return None
        post = self._get_post_from_id(post_id)
        # If Post Object
        if post:
             # Check that the user is logged in AND that the logged in user is the owner of this post
            if self.current_user is not None and self.current_user == post.author:
                # Remove the post from the blog's list of posts
                self.posts.remove(post)
                print(f"{post.title} has been deleted")
            # If the user is logged in but not the owner of the post
            elif self.current_user != post.author:
                print("You do not have permission to delete this post") # 403 HTTP Status Code
            # If the user is not logged in
            else:
                print("You must be logged in to perform this action") # 401 HTTP Status Code
        else:
            print(f"Post with an ID of {post_id} does not exist") # 404

class User:
    id_counter = 1 # Class attribute keeping track of User Ids
    
    def __init__(self, username, password):
        self.username = username
        self.password = password[::-2]
        self.id = User.id_counter
        User.id_counter += 1
        
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def check_password(self, password_guess):
        return self.password == password_guess[::-2]


class Post:
    id_counter = 1
    
    def __init__(self, title, body, author):
        """
        title: str
        body: str
        author: User
        """
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1
        
    def __str__(self):
        formatted_post = f"""
        {self.id} - {self.title}
        By: {self.author}
        {self.body}
        """
        return formatted_post
        
    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, value)
        
    

# Define a function to run the blog
def run_blog():
    # Create an instance of the blog
    my_blog = Blog()
    # Set up fake data
    initial_user1 = User('brians', 'abc123')
    initial_user2 = User('mj23', 'sixrings')
    my_blog.users.add(initial_user1)
    my_blog.users.add(initial_user2)
    my_blog.posts.append(Post('First Post', 'This is my first post', initial_user1))
    my_blog.posts.append(Post('Second Post', 'This is my second post', initial_user2))
    # Keep looping while blog is 'running'
    while True:
        # if there is no current user logged in
        if my_blog.current_user is None:
            # Print menu options
            print("1. Sign Up\n2. Log In\n3. View All Posts\n4. View Single Post\n5. Quit")
            # Ask user which option they would like to do
            to_do = input("Which option would you like to do? ")
            # keep asking if user chooses an invalid option
            while to_do not in {'1', '2', '5', '3', '4'}:
                to_do = input('Not valid. Please choose 1, 2, 3, 4, or 5 ')
            # clear_output()
            if to_do == '5':
                print("Thanks for checking out the blog!")
                break
            elif to_do == '1':
                # method to create a new user
                my_blog.create_new_user()
            elif to_do == '2':
                # method to log a user in
                my_blog.log_user_in()
            elif to_do == '3':
                # method to view all posts
                my_blog.view_posts()
            elif to_do == '4':
                # Get the id of the post
                post_id = input('What is the id of the post you would like to view? ')
                # Call the view single post method with post_id as an argument
                my_blog.view_post(post_id)
        # If the current user is not None aka a user is logged in
        else:
            print("1. Log Out\n2. Create A New Post\n3. View All Posts\n4. View Single Post\n5. Edit A Post\n6. Delete A Post")
            to_do = input('Which option would you like to choose ')
            while to_do not in {'1', '2', '3', '4', '5', '6'}:
                to_do = input('Not valid. Please choose 1, 2, 3, 4, 5, or 6 ')
            # clear_output()
            if to_do == '1':
                # method to log a user out
                my_blog.log_user_out()
            elif to_do == '2':
                # method to create a new post
                my_blog.create_post()
            elif to_do == '3':
                # method to view all posts
                my_blog.view_posts()
            elif to_do == '4':
                # Get the id of the post
                post_id = input('What is the id of the post you would like to view? ')
                # Call the view single post method with post_id as an argument
                my_blog.view_post(post_id)
            elif to_do == '5':
                # Get the id of the post that you would like to edit
                post_id = input('What is the id of the post you would like to edit? ')
                # Call the edit single post method with post_id as an argument
                my_blog.edit_post(post_id)
            elif to_do == '6':
                # Get the id of the post that you would like to delete
                post_id = input('What is the id of the post you would like to delete? ')
                # Call the delete single post method with post_id as an argument
                my_blog.delete_post(post_id)
            
            
run_blog()