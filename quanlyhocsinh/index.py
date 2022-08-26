from flask import render_template, request, url_for, send_file
from quanlyhocsinh import app, login, mail
from quanlyhocsinh.model import User, ExamDetail, Student, Class, ExamResult
from flask_login import login_user
import cloudinary.uploader
from quanlyhocsinh.forms import (ResetPasswordForm, RequestResetForm)
from flask_mail import Message
import hashlib


@app.route("/")
def home():
    return render_template('mainLogin.html')


@app.route("/loginAdmin", methods=['get', 'post'])
def login1():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        user = utils.check_user(fullname=fullname,
                                password=password,
                                role=UserRole.ADMIN)
        if user:
            login_user(user=user)
            return redirect('admin')
        else:
            err_msg = 'Fullname hoặc password không chính xác!!!'

    return render_template("admin/loginAdmin.html", err_msg=err_msg)


@app.route("/loginTeacher", methods=['get', 'post'])
def login2():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        user = utils.check_user2(fullname=fullname,
                                 password=password,
                                 role=UserRole.USER2)
        if user:
            login_user(user=user)
            return redirect('homeTeacher')
        else:
            err_msg = 'Fullname hoặc password không chính xác!!!'

    return render_template("teacher/loginTeacher.html", err_msg=err_msg)


@app.route("/loginMinistry", methods=['get', 'post'])
def login3():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        user = utils.check_user2(fullname=fullname,
                                 password=password,
                                 role=UserRole.USER)
        if user:
            login_user(user=user)
            return redirect('homeMinistry')
        else:
            err_msg = 'Fullname hoặc password không chính xác!!!'
    return render_template("ministry/loginMinistry.html", err_msg=err_msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='demoemail12345678910@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Để thay đổi mật khẩu vui lòng truy cập đường link:
{url_for('reset_token', token=token, _external=True)}
Nếu bạn bỏ qua email này thì mật khẩu sẽ không bị thay đổi
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        return redirect(url_for('login1'))
    return render_template('reset_request.html', title='Đổi mật khẩu', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = str(hashlib.md5(form.password.data.strip().encode('utf-8')).hexdigest())
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('login1'))
    return render_template('reset_token.html', title='Đổi mật khẩu', form=form)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('password_confirmation')
        email = request.form.get('email')

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get('avatar')
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res['secure_url']

            try:
                utils.add_user(fullname=fullname, password=password,
                               username=username, email=email,
                               avatar=avatar)

                return redirect(url_for('home'))
            except Exception as ex:
                err_msg = 'Đã có lỗi xảy ra: ' + str(ex)
            try:
                utils.validate_username(username=username)
            except:
                err_msg = 'Username đã tồn tại! Làm ơn sử dụng một username khác!'
            try:
                utils.validate_email(email=email)
            except:
                err_msg = 'Email đã tồn tại! Làm ơn sử dụng một email khác'
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/homeTeacher')
def homeTeacher():
    return render_template('teacher/mainTeacher.html')


@app.route('/homeTeacher/inputScore')
def homeTeacher_inputScore():
    all_data = ExamDetail.query.all()
    all_data2 = Class.query.all()
    all_data3 = Student.query.all()
    return render_template('teacher/inputScore.html', examDetail=all_data, classes=all_data2, students=all_data3)


@app.route('/updatescore', methods=['POST'])
def updatescore():
    if request.method == 'POST':
        my_data = ExamDetail.query.get(request.form.get('id'))

        my_data.fullname = request.form['fullname']
        my_data.testScore = request.form['className']
        my_data.subject = request.form['subject']
        my_data.point15 = request.form['point15']
        my_data.point60 = request.form['point60']
        my_data.testScore = request.form['testScore']
        my_data.semester = request.form['semester']
        my_data.schoolYear = request.form['schoolYear']

        db.session.commit()
        return redirect(url_for('homeTeacher_inputScore'))


@app.route('/add_examResult', methods=['GET', 'POST'])
def add_examResult():
    err_msg = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        className = request.form.get('className')
        subject = request.form.get('subject')
        point15 = request.form.get('point15')
        point60 = request.form.get('point60')
        testScore = request.form.get('testScore')
        semester = request.form.get('semester')
        schoolYear = request.form.get('schoolYear')
        try:
            utils.add_result(fullname=fullname, className=className, subject=subject,
                             point15=point15, point60=point60, testScore=testScore,
                             semester=semester, schoolYear=schoolYear)

            return redirect(url_for('homeTeacher_inputScore'))
        except Exception as ex:
            err_msg = 'Đã có lỗi xảy ra: ' + str(ex)

    return render_template('teacher/inputScore.html', err_msg=err_msg)


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete_result(id):
    my_data = ExamDetail.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('homeTeacher_inputScore'))


@app.route('/homeTeacher/outputScore')
def homeTeacher_outputScore():
    all_data = ExamResult.query.all()
    return render_template('teacher/outputScore.html', examResult=all_data, students_exam=utils.student_exam())


@app.route('/homeTeacher/outputScore/export')
def export():
    p = utils.export_csv()
    return send_file(p)


@app.route('/homeMinistry')
def homeMinistry():
    return render_template('ministry/homeMinistry.html')


@app.route('/homeMinistry/receiveApplication')
def receiveApplication():
    all_data = Student.query.all()
    return render_template('ministry/receiveApplication.html', students=all_data)


@app.route('/updateApplication', methods=['POST'])
def updateApplication():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))

        my_data.fullname = request.form['fullname']
        my_data.gender = request.form['gender']
        my_data.birth = request.form['birth']
        my_data.address = request.form['address']
        my_data.number = request.form['number']
        my_data.email = request.form['email']

        db.session.commit()
        return redirect(url_for('receiveApplication'))


@app.route('/addApplication', methods=['GET', 'POST'])
def addApplication():
    err_msg = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        gender = request.form.get('gender')
        birth = request.form.get('birth')
        address = request.form.get('address')
        number = request.form.get('number')
        email = request.form.get('email')

        try:
            utils.add_student(fullname=fullname, gender=gender,
                              birth=birth, address=address,
                              number=number, email=email)

            return redirect(url_for('receiveApplication'))
        except Exception as ex:
            err_msg = 'Đã có lỗi xảy ra: ' + str(ex)

    return render_template('ministry/receiveApplication.html', err_msg=err_msg)


@app.route('/delete_Application/<id>/', methods=['GET', 'POST'])
def delete_Application(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('receiveApplication'))


@app.route('/homeMinistry/classList')
def classList():
    all_data = Student.query.all()
    all_datas = Class.query.all()
    return render_template('ministry/classList.html', class_students=all_data, classes=all_datas)


@app.route('/updateClassList', methods=['POST'])
def updateClassList():
    if request.method == 'POST':
        my_data2 = Student.query.get(request.form.get('id'))
        my_data2.fullname = request.form['fullname']
        my_data2.gender = request.form['gender']
        my_data2.birth = request.form['birth']
        my_data2.address = request.form['address']
        my_data2.className = request.form['className']

        db.session.commit()
        return redirect(url_for('classList'))


# @app.route('/addClassList', methods=['GET', 'POST'])
# def addClassList():
#     err_msg = ""
#     if request.method.__eq__('POST'):
#         className = request.form.get('className')
#         try:
#             utils.add_classList(className=className)
#
#             return redirect(url_for('classList'))
#         except Exception as ex:
#             err_msg = 'Đã có lỗi xảy ra: ' + str(ex)
#
#     return render_template('ministry/classList.html', err_msg=err_msg)


@app.route('/delete_classList/<id>/', methods=['GET', 'POST'])
def delete_classList(id):
    my_data2 = Student.query.get(id)
    db.session.delete(my_data2)
    db.session.commit()
    return redirect(url_for('classList'))


@app.route('/templates/editClass')
def editClass():
    return render_template('ministry/editClass.html',
                           stats_class=utils.class_student(),
                           stats_class1=utils.class_student1(),
                           stats_class2=utils.class_student2(),
                           stats_class3=utils.class_student3(),
                           stats_class4=utils.class_student4(),
                           stats_class5=utils.class_student5(),
                           stats_class6=utils.class_student6(),
                           stats_class7=utils.class_student7(),
                           stats_class8=utils.class_student8())


if __name__ == '__main__':
    from quanlyhocsinh.admin import *
    app.run(debug=True)