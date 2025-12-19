from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise, ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Welcome to the Workout Tracker API</h1>'

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    workouts_list = [WorkoutSchema().dump(workout) for workout in workouts]
    return make_response({'workouts': workouts_list}, 200)

@app.route('/workouts/<id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout:
        return make_response(WorkoutSchema().dump(workout), 200)
    else:
        return make_response({'error': 'Workout not found'}, 404)
    
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        workouts_list = WorkoutSchema().load(data)
        new_workout = Workout(**workouts_list)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(WorkoutSchema().dump(new_workout), 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
    
@app.route('/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return make_response({'message': 'Workout deleted'}, 200)
    else:
        return make_response({'error': 'Workout not found'}, 404)
    

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    exercises_list = [ExerciseSchema().dump(exercise) for exercise in exercises]
    return make_response({'exercises': exercises_list}, 200)

@app.route('/exercises/<id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise:
        return make_response(ExerciseSchema().dump(exercise), 200)
    else:
        return make_response({'error': 'Exercise not found'}, 404)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        exercise_list = ExerciseSchema().load(data)
        new_exercise = Exercise(**exercise_list)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(ExerciseSchema().dump(new_exercise), 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
@app.route('/exercises/<id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        return make_response({'message': 'Exercise deleted'}, 200)
    else:
        return make_response({'error': 'Exercise not found'}, 404)

@app.route('/workouts/<workout_id>/exercises/<exercise_id>', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json()
    try:
        workout = db.session.get(Workout, workout_id)
        exercise = db.session.get(Exercise, exercise_id)
        if not workout or not exercise:
            return make_response({'error': 'Workout or Exercise not found'}, 404)
        
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        workout_exercise_data = WorkoutExerciseSchema().load(data)
        workout_exercise = WorkoutExercise(**workout_exercise_data)
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(WorkoutExerciseSchema().dump(workout_exercise), 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)