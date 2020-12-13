from remle import app, db
from flask import jsonify, request
from remle.models import StudentsActivity, SASchema, Student, StudentSchema
from datetime import datetime
import os
import pytz


@app.route('/data/students-activity/student=<int:id>')
def students_activity(id):
    sa = StudentsActivity.query.with_entities(StudentsActivity.student,
                                              StudentsActivity.last_edited).filter_by(student=id)
    sa_schema = SASchema(many=True)
    student = Student.query.with_entities(Student.first_name, Student.last_name).filter_by(id=id)
    student_schema = StudentSchema(many=True)
    output = [{**sa_schema.dump(sa)[0], **student_schema.dump(student)[0]}]
    return jsonify({'studentsActivity': output})


@app.route('/data/students-work/student=<int:id>')
def students_work(id):
    sa = StudentsActivity.query.with_entities(StudentsActivity.data).filter_by(student=id)
    sa_schema = SASchema(many=True)
    output = sa_schema.dump(sa)
    return jsonify({'studentsWork': output})


@app.route('/data/students-icons/student=<int:id>')
def students_icons(id):
    si = Student.query.with_entities(Student.first_name, Student.last_name).filter_by(id=id)
    student_schema = StudentSchema(many=True)
    output = student_schema.dump(si)
    return jsonify({'studentsIcons': output})


@app.route('/work-input', methods=['POST'])
def put_work():
    if request.method == "POST":
        lesson_id = request.form['lesson_id']
        student_id = request.form['student_id']
        work = request.form['work']
        dt = datetime.now(pytz.timezone('Europe/Warsaw'))
        sa = StudentsActivity.query.filter_by(student=student_id).first()
        if sa:
            sa.last_edited = dt.strftime("%d-%m-%Y %H:%M:%S")
        else:
            activity = StudentsActivity(lesson_id=lesson_id, last_edited=dt.strftime("%d-%m-%Y %H:%M:%S"),
                                        student=student_id, data=work)
            db.session.add(activity)
        db.session.commit()

        return "200"


@app.route('/shared/httpreq')
def httpreq_down():
    document_path = os.getcwd() + '\shared\httpreq.js'
    with open(document_path, "r") as f:
        text = f.read()

        return text, {'Content-Type': 'text/javascript; charset=utf-8'}

@app.route('/shared/demo')
def demo_down():
    document_path = os.getcwd() + '\shared\demo_lesson.html'
    with open(document_path, "r") as f:
        text = f.read()

        return text, {'Content-Type': 'text/html; charset=utf-8'}
