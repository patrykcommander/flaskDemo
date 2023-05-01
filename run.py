# once we want to create the DataBase, command app.app_context().push() has to be run just before the db.create_all() command
# same when we want to add a new record into the db
# db.session.add() -> function to add a record to the database
# db.session.commit() -> commits the changes made with the .add() function to the database
# User.query.all() -> returns back all of the users
# User.query.first() -> returns the first user back
# User.query.filter_by(userName='Patryk').all() -> returns back the list of all of the users, but in this app the username is unique
# User.query.filter_by(userName='Patryk').first() 
# User.query.get(primary_key) -> legacy function (still possible to use), exchanged by the db.session.get(User, primary_key)
# db.drop_all() removes all of the tables

# when workin with packages (in this case the flaskblog folder is our package), the import below imports the variable 
# from the __init__ file
from flaskblog import app


if __name__ == '__main__':
    app.run(debug=True)
