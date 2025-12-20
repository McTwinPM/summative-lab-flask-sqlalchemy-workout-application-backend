# summative-lab-flask-sqlalchemy-workout-application-backend

PROJECT TITLE

    Welcome to Michael's Workout Application

PROJECT DESCRIPTION

    This application allows the user to make a list of exercises, and use those exercises to build custom workouts.

INSTALLATION INSTRUCTIONS

    1. Install necessary dependencies and modules by using the command 'pipenv install'
    2. To set up your virtual environment, run command 'pipenv shell'

    3. To initialize the database, run command 'flask db init'
    4. To initialize the database migration, run command 'flask db migrate -m "initial migration"'
    5. Run 'flask db upgrade head to bring the database schema to your migration.


RUN INSTRUCTIONS

    You are now ready to run the database.

    1. Run the command 'python seed.py' (or 'python3 seed.py' if you are running a newer version of Python). This will populate your database with data. 
        *Currently seed.py has hardcoded example exercise data, with workout data that randomizes every time you seed.

    2. Run the command 'python app.py' to begin running the flask server, an open the endpoints for the database

ENDPOINT DESCRIPTIONS

    Home /
        This is the home endpoint, with a simple welcome message
     /workouts (GET)
        This will list all workouts in the database
    /workouts/<id> (GET)
        This will display a single, specific workout, and all exercises involved with it.
    POST /workouts
        This will allow you to create a workout
    DELETE /workouts/<id>
        This will allow you to delete a specific workout
    GET /exercises
        This will list all exercises in the database
    GET /exercises/<id>
        Show an exercise and associated workouts
    POST /exercises
        This will allow you to create an exercise
    DELETE /exercises/<id>
        This will allow you to delete a specific exercise
    POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
        This will allow you to add a specific exercise to a specific workout.