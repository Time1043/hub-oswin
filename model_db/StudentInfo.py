class StudentInfo:
    def __init__(self, name, age, gender, major, gpa):
        self.name = name
        self.age = age
        self.gender = gender
        self.major = major
        self.gpa = gpa

    def __str__(self):
        return (
                "Name: " + self.name + ", Age: " + str(self.age) + ", Gender: " + self.gender +
                ", Major: " + self.major + ", GPA: " + str(self.gpa)
        )
