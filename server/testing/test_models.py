from server.models import Exercise, Workout, WorkoutExercise
from marshmallow import ValidationError
import pytest
from datetime import date

def test_exercise_model():
    exercise = Exercise(name="Test Exercise", category="Strength", equipment_needed=False)
    assert exercise.name == "Test Exercise"
    assert exercise.category == "Strength"
    assert exercise.equipment_needed is False
    assert repr(exercise) == "<Exercise Test Exercise - Category: Strength - Equipment Needed: False>"
    with pytest.raises(ValueError):
        Exercise(name="", category="Strength", equipment_needed=False)
    with pytest.raises(ValueError):
        Exercise(name="Test Exercise", category="", equipment_needed=False)



def test_workout_model():
    workout = Workout(date=date(2024, 1, 1), duration_minutes=60, notes="Test workout")
    assert workout.date == date(2024, 1, 1)
    assert workout.duration_minutes == 60
    assert workout.notes == "Test workout"
    assert repr(workout) == "<Workout on 2024-01-01 - Duration: 60 minutes>"
    with pytest.raises(ValueError):
        Workout(date="", duration_minutes=60, notes="Test workout")
    with pytest.raises(ValueError):
        Workout(date="2024-01-01", duration_minutes=-10, notes="Test workout")



def test_workout_exercise_model():
    workout_exercise = WorkoutExercise(id=1, workout_id=1, exercise_id=1, sets=3, reps=10)
    assert workout_exercise.id == 1
    assert workout_exercise.workout_id == 1
    assert workout_exercise.exercise_id == 1
    assert workout_exercise.sets == 3
    assert workout_exercise.reps == 10
    assert repr(workout_exercise) == "<WorkoutExercise: 1 Workout ID: 1 - Exercise ID: 1 - Sets: 3 - Reps: 10 - Duration: None seconds>"
    with pytest.raises(ValueError):
        WorkoutExercise(workout_id=1, exercise_id=1, sets=0, reps=10)
    with pytest.raises(ValueError):
        WorkoutExercise(workout_id=1, exercise_id=1, sets=3, reps=-5)

