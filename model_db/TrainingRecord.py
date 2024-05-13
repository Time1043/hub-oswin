class TrainingRecord:
    def __init__(self, id, training_id, user_id, date, duration, distance, calories, heart_rate, steps, notes):
        self.id = id
        self.training_id = training_id
        self.user_id = user_id
        self.date = date
        self.duration = duration
        self.distance = distance
        self.calories = calories
        self.heart_rate = heart_rate
        self.steps = steps
        self.notes = notes