# DAD JOKES GENERATOR
#### Video Demo: https://youtu.be/EYoMdWBHNuQ
#### Description:

##### How to use:

Index page:
- Generate a joke: generate a joke and display it on the website.
- Add to favorites: add the current generated joke to user's favorites (requires log in)

Login page:
- A form in which user inputs username, password and a button to submit.
- A link which redirect user to registration page.

Register page:
- A form in which user inputs username, password twice and a button to submit.
- On registration, redirect back to login.

Favorites page:
- A table which shows user's favorite with a button to remove the joke for each joke in the table.

##### Inside the project:

/static:
- /img: Images files.
- /css: Css files
- js: Javascript files (jquery's ajax())
    - generate: Send an ajax request back to server then update html file with the data received.
    - favorites: Send an ajax **POST** request back to server, then alert the callback message.
    - delete: Send an ajax request back to server to delete a joke in the user's favorites database.

/templates:
- layout.html: A template for other html files.
- index.html: The homepage where you generate jokes.
- login.html: Log in page.
- register.html: Registration page.
- favorites.html: Favorites page in which user view their saved jokes.

application.py:
- delete(): Receive an ajax request then delete the joke mentioned in the request.

- index(): Render homepage.

- favorites(): If **GET** render favorites.html, if **POST** add a joke to favorites.

- login():
    - Check user's username and password.
    - Username cannot be empty.
    - Username must be unique.
    - Password cannot be empty
    - If all the requirements above is satisfied, log user in and give them a unique id for their session. If not, redirect them back to log in page and inform them about the error.

- logout(): Log user out.

- register():
    - Check user's username, password and password confirmation.
    - Username cannot be empty.
    - Username must be unique.
    - Password cannot be empty
    - Password and password confirmation must match.
    - If all the requirements above is satisfied, insert a new username and password into the database and redirect user back to login page. If not, redirect them back to register page and inform them about the error.

jokes.db:
- users: A table which stores user's login credential with their unique id.
- jokes: A table which stores all the jokes used to generate with a unique id for each joke.
- favorites: A table which stores user's id and joke's id equivalent to the joke they've saved.

##### Why did you make it and how?
First of all, I want to thank you all for visiting my project. This project took me a week to
make and I'm proud of what I've made during that time. So why did I make this? I love dad jokes
and I love sending dad jokes to annoy my friends. One day while I was sending dad jokes to my
friends, I thought to myself: "Should I make a website that generate a random dad jokes for me
and use it as my final project?". My answer to that question was "YES" and I started working on
the project immediately. Making a website from scratch was hard and I spent my first few days
thinking how should I implement this website. On the fourth day, I started writting my first
few codes for the project. My greatest obstacle for this project is how to save user's favorite
jokes. My first solution is to generate a hash code for every list of jokes they saved, then I
switch to have them give a password for that list of jokes. To me, both of those options were
way too inefficient and I didn't really know how to implement it. In the end, I settle with
username and password which was way easier to implement and control the data. I spent the next
few days adjusting my code and decorating my website (with some advices from my friends). Finally
on the first thursday of March, I completed my project. Again, thank you all for visitting my project
and I hope you have a great time. This was CS50.
