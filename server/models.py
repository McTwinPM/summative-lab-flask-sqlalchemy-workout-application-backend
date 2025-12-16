from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    #relationships
    workouts = db.relationship('WorkoutExercise', back_populates='exercise', lazy=True)

    #validations
    @validates('name', 'category')
    def validate_strings(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError(f"{key} must be a non-empty string")
        return value
    @validates('equipment_needed')
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String)

    #relationships
    exercises = db.relationship('WorkoutExercise', back_populates='workout', lazy=True)

    #validations
    @validates('date')
    def validate_date(self, key, value):
        if not value:
            raise ValueError(f"{key} must be a valid date")
        return value
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer)

    #relationships
    workout = db.relationship('Workout', back_populates='exercises', lazy=True)
    exercise = db.relationship('Exercise', back_populates='workouts', lazy=True)

    #validations
    @validates('sets', 'reps')
    def validate_positive_integers(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value
