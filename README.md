## Frappe Flask-Test

This is my try at Frappe's [Flask Test](https://frappe.io/flask-test). I didn't look at any other solution before writing this. If you did not complete the test yet, I encourage you to try it yourself, before looking at my solution. 

For reference, it took me about five hours to solve the challenge with plain HTML and a single python file. I spent another five hours to give it a better structure and an acceptable look.

The structure of this app is based on the [Flask Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/). I use [bootstrap's CSS](https://getbootstrap.com/docs/4.4/getting-started/introduction/#css) for styling.

## Setup

Create and activate venv, install dependencies:

```bash
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=flask_test
```

Initialize the database. This will create a database file in the instance directory.

```bash
flask init-db
```

Run the app:

```bash
flask run --reload
```
