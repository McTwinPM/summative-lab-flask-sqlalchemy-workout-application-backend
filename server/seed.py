#!/usr/bin/env python3

from app import app
from models import *
from random import choice, randint
from faker import Faker
import os

# Delete existing database
if os.path.exists('instance/app.db'):
    os.remove('instance/app.db')
    print("Old database deleted")

with app.app_context():

    # Create all tables
    db.create_all()
    faker = Faker()

    # Clear existing data
    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()
    
    
    #add exerceses manually
    exercises = [
        Exercise(name="Push-ups", category="Strength", equipment_needed=False),
        Exercise(name="Squats", category="Strength", equipment_needed=False),
        Exercise(name="Bench Press", category="Strength", equipment_needed=True),
        Exercise(name="Running", category="Cardio", equipment_needed=False),
        Exercise(name="Cycling", category="Cardio", equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()

    #add workouts using faker
    workouts = []
    for w in range(5):
        workout = Workout(
            date = faker.future_date(),
            duration_minutes = randint(20, 120),
            notes = faker.sentence(nb_words=6)
        )
        workouts.append(workout)
    db.session.add_all(workouts)
    db.session.commit()

    #add workout_exercises using faker
    workout_exercises = []
    for we in range(15):
        workout_exercise = WorkoutExercise(
            workout_id = choice(workouts).id,
            exercise_id = choice(exercises).id,
            sets = randint(1, 5),
            reps = randint(5, 20),
            duration_seconds = randint(30, 300) 
        )
        workout_exercises.append(workout_exercise)
    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")
