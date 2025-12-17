from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    workouts_list = [{
        'id': workout.id,
        'date': workout.date.isoformat(),
        'duration_minutes': workout.duration_minutes,
        'notes': workout.notes
    } for workout in workouts]
    return make_response({'workouts': workouts_list}, 200)

@app.route('/workouts/<id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if workout:
        body = {
            'id': workout.id,
            'date': workout.date.isoformat(),
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes,
            'exercises': [
                {
                    'exercise_id': we.exercise.id,
                    'name': we.exercise.name,
                    'category': we.exercise.category,
                    'equipment_needed': we.exercise.equipment_needed,
                    'sets': we.sets,
                    'reps': we.reps,
                    'duration_seconds': we.duration_seconds
                } for we in workout.exercises
            ]
        }
        return make_response(body, 200)
    else:
        return make_response({'error': 'Workout not found'}, 404)
    
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes', '')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response({'message': 'Workout created', 'workout_id': new_workout.id}, 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
    
@app.route('/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return make_response({'message': 'Workout deleted'}, 200)
    else:
        return make_response({'error': 'Workout not found'}, 404)
    

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    exercises_list = [{
        'id': exercise.id,
        'name': exercise.name,
        'category': exercise.category,
        'equipment_needed': exercise.equipment_needed
    } for exercise in exercises]
    return make_response({'exercises': exercises_list}, 200)

@app.route('/exercises/<id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise:
        body = {
            'id': exercise.id,
            'name': exercise.name,
            'category': exercise.category,
            'equipment_needed': exercise.equipment_needed,
            'workouts': [
                {
                    'workout_id': we.workout.id,
                    'date': we.workout.date.isoformat(),
                    'duration_minutes': we.workout.duration_minutes,
                    'notes': we.workout.notes,
                    'sets': we.sets,
                    'reps': we.reps,
                    'duration_seconds': we.duration_seconds
                } for we in exercise.workouts
            ]
        }
        return make_response(body, 200)
    else:
        return make_response({'error': 'Exercise not found'}, 404)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response({'message': 'Exercise created', 'exercise_id': new_exercise.id}, 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
@app.route('/exercises/<id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
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
        workout = Workout.query.get(workout_id)
        exercise = Exercise.query.get(exercise_id)
        if not workout or not exercise:
            return make_response({'error': 'Workout or Exercise not found'}, 404)
        
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            sets=data.get('sets'),
            reps=data.get('reps'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response({'message': 'Exercise added to workout'}, 201)
    except Exception as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)