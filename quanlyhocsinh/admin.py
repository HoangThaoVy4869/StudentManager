from quanlyhocsinh import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from quanlyhocsinh.model import Subject, Class, Grade, UserRole, MaxMinAge, MaxClassNumber
from flask_login import current_user, logout_user
from flask import redirect
import utils


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=utils.class_stats(), stats2=utils.class_stats2(),
                                               stats_studentClass=utils.class_student(),
                                               stats_studentClass1=utils.class_student1())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class SubjectView(ModelView):
    can_export = True
    can_view_details = True
    column_searchable_list = ['subjectName']
    column_exclude_list = ['active']
    column_labels = {
        'active': 'Trạng thái',
        'subjectName': 'Tên môn học',
        'description': 'Mô tả',
        'grade': 'Khối'
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AgeView(ModelView):
    can_create = False
    can_delete = False
    column_labels = {
        'maxAge': 'Độ tuổi tối đa',
        'minAge': 'Độ tuổi tối thiểu'
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ClassNumberView(ModelView):

    # if db.session.query(ClassNumber).filter(ClassNumber.maxClassNumber.__eq__(null)).first():
    #     can_create = True
    #     db.session.commit()
    # elif db.session.query(ClassNumber).filter(ClassNumber.maxClassNumber.__ne__(null)).first():
    #     can_create = False
    #     db.session.commit()
    can_create = False
    can_delete = False
    column_labels = {
        'maxClassNumber': 'Sĩ số tối đa'
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=utils.class_stats(),
                           stats2=utils.class_stats2())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app=app,
              name="Quản lý học sinh Administration",
              template_mode='bootstrap4',
              index_view=MyAdminIndex())

admin.add_view(SubjectView(Subject, db.session))
admin.add_view(AgeView(MaxMinAge, db.session))
admin.add_view(ClassNumberView(MaxClassNumber, db.session))
# admin.add_view(AuthenticatedModelView(Grade, db.session))
# admin.add_view(AuthenticatedModelView(Class, db.session))
# admin.add_view(AuthenticatedModelView(Student, db.session))
# admin.add_view(AuthenticatedModelView(Exam, db.session))
# admin.add_view(AuthenticatedModelView(ExamResult, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))

