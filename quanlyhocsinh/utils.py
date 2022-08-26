import csv
import json, os
from quanlyhocsinh import app, db
from quanlyhocsinh.model import User, Subject, UserRole, Class, ExamDetail, ExamResult, Student, Class
from sqlalchemy import func
import hashlib


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def export_csv():
    examResults = read_result()
    p = os.path.join(app.root_path, "data/newResults.csv")
    with open(p, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "schoolYear", "avg1", "avg2", "class_id", "exam_id"])
        writer.writeheader()
        for examResult in examResults:
            writer.writerow(examResult)

    return p


def add_user(fullname, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(fullname=fullname.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def add_result(fullname, className, subject, point15, point60, testScore, semester, schoolYear):
    examDetail = ExamDetail(fullname=fullname.strip(),
                            className=className,
                            subject=subject.strip(),
                            point15=point15,
                            point60=point60,
                            testScore=testScore,
                            semester=semester,
                            schoolYear=schoolYear)

    db.session.add(examDetail)
    db.session.commit()


def add_student(fullname, gender, birth, address, number, email):
    student = Student(fullname=fullname.strip(),
                      gender=gender,
                      birth=birth,
                      address=address.strip(),
                      number=number.strip(),
                      email=email.strip())

    db.session.add(student)
    db.session.commit()


def add_classList(className):
    classes_list = Class(className=className.strip())
    Student.className = Class.className
    db.session.add(classes_list)
    db.session.commit()


def validate_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        raise ValueError('Username đã tồn tại')


def validate_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValueError('Email đã tồn tại')


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_user(fullname, password, role=UserRole.USER):
    if fullname and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.fullname.__eq__(fullname.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def check_user2(fullname, password, role=UserRole.USER2):
    if fullname and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.fullname.__eq__(fullname.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def load_subjects(kw=None, grades=None):
    subjects = Subject.query.filter(Subject.active.__eq__(True))

    if kw:
        subjects = subjects.filter(Subject.subjectName.contains(kw))

    if grades:
        subjects = subjects.filter(Subject.grade_id.__eq__(grades))

    return subjects.query.all()


def read_result():

    return read_json(os.path.join(app.root_path, 'data/examResults.json'))


def class_stats():
    return db.session.query(Class.className, Class.classNumber, func.count(ExamResult.avg1.__ge__(5.0)),\
                            (((func.count(ExamResult.avg1.__ge__(5.0)))/Class.classNumber)*100))\
                            .join(ExamResult, Class.id.__eq__(ExamResult.class_id), isouter=True)\
                            .filter(ExamResult.avg1.__ge__(5.0))\
                            .group_by(Class.className, Class.classNumber).all()


def class_stats2():
    return db.session.query(Class.className, Class.classNumber, func.count(ExamResult.avg2.__ge__(5.0)),\
                            (((func.count(ExamResult.avg1.__ge__(5.0)))/Class.classNumber)*100))\
                            .join(ExamResult, Class.id.__eq__(ExamResult.class_id), isouter=True)\
                            .filter(ExamResult.avg2.__ge__(5.0))\
                            .group_by(Class.className, Class.classNumber).all()


def class_stats3():
    return db.session.query([class_student(), class_student1(), class_student2(), class_student3(), class_student4(),
                             class_student5(), class_student6(), class_student7(), class_student8()])


def student_exam():
    return db.session.query(Student.id, Student.fullname, Student.className, ExamResult.schoolYear,\
                            ExamResult.avg1, ExamResult.avg2)\
                            .join(ExamResult, Student.id.__eq__(ExamResult.student_id), isouter=True)\
                            .group_by(Student.fullname).all()


def class_student():
    return db.session.query(Student.className, func.count(Student.className.like('10A1'))) \
                            .filter(Student.className.like("10A1"))\
                            .all()


def class_student1():
    return db.session.query(Student.className, func.count(Student.className.like('10A2'))) \
                            .filter(Student.className.like("10A2"))\
                            .all()


def class_student2():
    return db.session.query(Student.className, func.count(Student.className.like('10A3'))) \
                            .filter(Student.className.like("10A3"))\
                            .all()


def class_student3():
    return db.session.query(Student.className, func.count(Student.className.like('11A1'))) \
                            .filter(Student.className.like("11A1"))\
                            .all()


def class_student4():
    return db.session.query(Student.className, func.count(Student.className.like('11A2'))) \
                            .filter(Student.className.like("11A2"))\
                            .all()


def class_student5():
    return db.session.query(Student.className, func.count(Student.className.like('11A3'))) \
                            .filter(Student.className.like("11A3"))\
                            .all()


def class_student6():
    return db.session.query(Student.className, func.count(Student.className.like('12A1'))) \
                            .filter(Student.className.like("12A1"))\
                            .all()


def class_student7():
    return db.session.query(Student.className, func.count(Student.className.like('12A2'))) \
                            .filter(Student.className.like("12A2"))\
                            .all()


def class_student8():
    return db.session.query(Student.className, func.count(Student.className.like('12A3'))) \
                            .filter(Student.className.like("12A3"))\
                            .all()
