from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    #relationships
    workouts = db.relationship('WorkoutExercise', back_populates='exercise', lazy=True)

    def __repr__(self):
        return f"<Exercise {self.name} - Category: {self.category} - Equipment Needed: {self.equipment_needed}>"

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

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

    workouts = fields.Nested(lambda: WorkoutExerciseSchema,exclude=("exercise",), many=True)

    @validates('name')
    def validate_strings(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Must be a non-empty string")
        return value
    @validates('equipment_needed')
    def validate_equipment_needed(self, value):
        if not isinstance(value, bool):
            raise ValueError("Must be a boolean")
        return value

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String)

    #relationships
    exercises = db.relationship('WorkoutExercise', back_populates='workout', lazy=True)

    def __repr__(self):
        return f"<Workout on {self.date} - Duration: {self.duration_minutes} minutes>"

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

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()

    exercises = fields.Nested(lambda: WorkoutExerciseSchema, exclude=("workout",), many=True)

    @validates('duration_minutes')
    def validate_duration(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("duration_minutes must be a positive integer")
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

    def __repr__(self):
        return f"<WorkoutExercise: {self.id} Workout ID: {self.workout_id} - Exercise ID: {self.exercise_id} - Sets: {self.sets} - Reps: {self.reps} - Duration: {self.duration_seconds} seconds>"

    #validations
    @validates('sets', 'reps')
    def validate_positive_integers(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(required=True)
    reps = fields.Int(required=True)
    duration_seconds = fields.Int()

    workout = fields.Nested(WorkoutSchema, exclude=("exercises",))
    exercise = fields.Nested(ExerciseSchema, exclude=("workouts",))

    @validates('sets', 'reps')
    def validate_positive_integers(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Must be a positive integer")
        return value