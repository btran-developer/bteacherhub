from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    main_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    main_teacher = db.relationship(
        'Teacher', foreign_keys=[main_teacher_id], lazy=True)
    assistant_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    assistant_teacher = db.relationship(
        'Teacher', foreign_keys=[assistant_teacher_id], lazy=True)
    teaching_date = db.Column(db.Date, index=True)
    submit_date = db.Column(db.DateTime, default=datetime.utcnow)
    teaching_content = db.Column(db.String(200))
    student_attendance = db.Column(db.Integer)
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    submitted_by = db.relationship(
        'Teacher', foreign_keys=[submitted_by_id], lazy=True)

    def __repr__(self):
        return f'<Report {self.main_teacher} {self.assistant_teacher} {self.teaching_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'main_teacher': self.main_teacher.to_dict(),
            'assistant_teacher': self.assistant_teacher.to_dict() if self.assistant_teacher_id != 0 else '',
            'teaching_date': self.teaching_date,
            'teaching_content': self.teaching_content,
            'student_attendance': self.student_attendance,
            'submitted_by': self.submitted_by.to_dict()
        }


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Teacher {self.teacher_name} {"Active" if self.is_active else "Inactive"}>'

    def __str__(self):
        return f'{self.teacher_name}'

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_name': self.teacher_name,
            'is_active': self.is_active
        }

    @staticmethod
    def get_teachers_for_choices(defaultOpt=(0, '')):
        return [defaultOpt] + [(t.id, t.teacher_name) for t in Teacher.query.filter_by(is_active=True).order_by('teacher_name')]
