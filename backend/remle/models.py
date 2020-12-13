from remle import db, ma


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.id}: {self.first_name} {self.last_name}>'


students_courses = db.Table('students_courses_membership',
                            db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
                            db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                            )


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    lessons = db.relationship('Lesson', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.id}: {self.name}>'


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    begin_date = db.Column(db.String(16))
    end_date = db.Column(db.String(16))
    html = db.Column(db.Text)
    students_activity = db.relationship('StudentsActivity', backref='lesson', lazy=True)

    def __repr__(self):
        return f'<Lesson {self.id}: {self.name}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    activity = db.relationship('StudentsActivity', backref='stud', lazy=True)
    courses = db.relationship('Course', secondary=students_courses, lazy='subquery',
                              backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'<Student {self.id}: {self.first_name} {self.last_name}>'


class StudentsActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    last_edited = db.Column(db.String(19))
    student = db.Column(db.Integer, db.ForeignKey('student.id'))
    data = db.Column(db.Text)

    def __repr__(self):
        return f'<StudentsActivity {self.id}: student {self.student}, lesson {self.student}>'


class SASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentsActivity
        include_fk = True


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        include_fk = True
