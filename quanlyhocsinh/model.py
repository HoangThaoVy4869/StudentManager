from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Enum, Date
from quanlyhocsinh import db, app
from flask_login import UserMixin
from datetime import datetime, date
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship, backref
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    USER2 = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/default.png')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __str__(self):
        return self.fullname


student_subject = db.Table('student_subject',
                           Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
                           Column('subject_id', Integer, ForeignKey('subject.id'), primary_key=True))


student_exam = db.Table('student_exam',
                        Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
                        Column('exam_id', Integer, ForeignKey('exam.id'), primary_key=True))


# subject_class = db.Table('subject_class',
#                          Column('subject_id', Integer, ForeignKey('subject.id'), primary_key=True),
#                          Column('class_id', Integer, ForeignKey('class.id'), primary_key=True))


class Student(BaseModel):
    __tablename__ = 'student'
    fullname = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    birth = Column(Date, default=date.today())
    address = Column(String(100))
    number = Column(String(10))
    email = Column(String(50))
    className = Column(String(20))
    class_id = Column(Integer, ForeignKey('class.id'))
    maxMinAge_id = Column(Integer, ForeignKey('maxMinAge.id'))
    examResults = relationship('ExamResult', backref='student', lazy=True)
    subjects = relationship('Subject', secondary='student_subject', lazy='subquery',
                            backref=backref('students', lazy=True))


class Class(BaseModel):
    __tablename__ = 'class'
    className = Column(String(20), nullable=False)
    classNumber = Column(String(100), nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'))
    maxClassNumber_id = Column(Integer, ForeignKey('maxClassNumber.id'))
    students = relationship('Student', backref='class', lazy=True)
    examResults = relationship('ExamResult', backref='class', lazy=True)

    def __str__(self):
        return self.className


class Grade(BaseModel):
    __tablename__ = 'grade'
    nameGrade = Column(String(20), nullable=False)
    classes = relationship('Class', backref='grade', lazy=True)
    subjects = relationship('Subject', backref='grade', lazy=True)

    def __str__(self):
        return self.nameGrade


class Exam(BaseModel):
    __tablename__ = 'exam'
    examType = Column(String(20), nullable=False)
    examResults = relationship('ExamResult', backref='exam', lazy=True)
    examDetails = relationship('ExamDetail', backref='exam', lazy=True)

    def __str__(self):
        return self.examType


class ExamResult(BaseModel):
    __tablename__ = 'examResult'
    schoolYear = Column(String(100))
    avg1 = Column(Float, nullable=False, default=0)
    avg2 = Column(Float, nullable=False, default=0)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    exam_id = Column(Integer, ForeignKey('exam.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))


class ExamDetail(BaseModel):
    __tablename__ = 'examDetail'
    fullname = Column(String(50), nullable=False)
    className = Column(String(20), nullable=False)
    subject = Column(String(100), nullable=False)
    point15 = Column(Float, nullable=False, default=0)
    point60 = Column(Float, nullable=False, default=0)
    semester = Column(String(100))
    schoolYear = Column(String(100))
    testScore = Column(Float, nullable=False, default=0)
    examResult_id = Column(ForeignKey('examResult.id'))
    exam_id = Column(Integer, ForeignKey("exam.id"))


class Subject(BaseModel):
    __tablename__ = 'subject'
    active = Column(Boolean, default=True)
    subjectName = Column(String(100), nullable=False)
    description = Column(String(200))
    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)


class MaxMinAge(BaseModel):
    __tablename__ = 'maxMinAge'
    maxAge = Column(Integer, nullable=False)
    minAge = Column(Integer, nullable=False)
    students = relationship('Student', backref='maxMinAge', lazy=True)


class MaxClassNumber(BaseModel):
    __tablename__ = 'maxClassNumber'
    maxClassNumber = Column(Integer, nullable=False)
    classes = relationship('Class', backref='maxClassNumber', lazy=True)


if __name__ == '__main__':
    db.create_all()
