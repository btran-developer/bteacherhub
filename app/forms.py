from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextField, IntegerField, SubmitField, SelectField
from wtforms.widgets.html5 import DateInput, NumberInput
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Optional, Length, ValidationError
from datetime import datetime
from app.models import Teacher


MONTHS = [
    (1, 1), (2, 2), (3, 3),
    (4, 4), (5, 5), (6, 6),
    (7, 7), (8, 8), (9, 9),
    (10, 10), (11, 11), (12, 12)
]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class AddTeacherForm(FlaskForm):
    teacher_name = StringField('Teacher', validators=[DataRequired()])
    submit = SubmitField('Add')


class ReportForm(FlaskForm):
    main_teacher = SelectField(
        'Main Teacher', validators=[DataRequired()], coerce=int)
    assistant_teacher = SelectField(
        'Assistant Teacher', validators=[Optional()], coerce=int)
    teaching_date = DateField(
        'Teaching Date', validators=[DataRequired()], widget=DateInput())
    teaching_content = TextField(
        'Teaching Content', validators=[DataRequired(), Length(max=200)], widget=TextArea())
    student_attendance = StringField(
        'Student Attendance', validators=[DataRequired()], widget=NumberInput(step=1))
    submitted_by = SelectField(
        'Submitted By', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit Report')

    def validate_assistant_teacher(self, teacher):
        if teacher.data == self.main_teacher.data:
            raise ValidationError(
                'Assitant and main teachers can\'t be the same.')

    def validate_teaching_date(self, date):
        if date.data > datetime.now().date():
            raise ValidationError('Cannot have date in the future.')

    def validate_student_attendance(self, attendance):
        if int(attendance.data) <= 0:
            raise ValidationError('Student attendance cannot be 0.')


class GetReportsForm(FlaskForm):
    from_date = DateField(
        'From', validators=[DataRequired()], widget=DateInput())
    to_date = DateField(
        'To', validators=[DataRequired()], widget=DateInput())
    teacher = SelectField(
        'Teacher', coerce=int)
    submit = SubmitField('Get')

    def validate_from_date(self, date):
        if self.to_date.data:
            if date.data > self.to_date.data:
                raise ValidationError(
                    '"from date" cannot be greater than "to date"')

    def validate_to_date(self, date):
        if self.from_date.data:
            if date.data < self.from_date.data:
                raise ValidationError(
                    '"to date" cannot be lesser than "from date"')


class GetReportsAdminForm(FlaskForm):
    from_date = DateField(
        'From', validators=[DataRequired()], widget=DateInput())
    to_date = DateField(
        'To', validators=[DataRequired()], widget=DateInput())
    submit = SubmitField('Get Report')

    def validate_from_date(self, date):
        if self.to_date.data:
            if date.data > self.to_date.data:
                raise ValidationError(
                    '"from date" cannot be greater than "to date"')

    def validate_to_date(self, date):
        if self.from_date.data:
            if date.data < self.from_date.data:
                raise ValidationError(
                    '"to date" cannot be lesser than "from date"')


class GetMonthlyReportsForm(FlaskForm):
    month = SelectField('Month', coerce=int, choices=MONTHS)
    year = StringField(
        'Year', validators=[DataRequired()], default=datetime.now().year, widget=NumberInput(step=1))
    pay_per_day = IntegerField('Pay per day', validators=[DataRequired()])
    teacher = SelectField('Teacher', coerce=int)
    submit = SubmitField('Get report')
