from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from quanlyhocsinh.model import User
import email_validator


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Xác nhận Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email không tồn tại. Vui lòng đăng ký trước')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    confirm_password = PasswordField('Nhập lại mật khẩu',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Thay đổi mật khẩu')