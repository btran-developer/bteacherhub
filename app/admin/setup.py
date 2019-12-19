from app import admin, db
from app.models import User, Teacher, Report
from .user_admin_view import UserAdminView
from .teacher_admin_view import TeacherAdminView
from .report_admin_view import ReportAdminView
from .monthly_report_view import MonthlyReportView
from .teacher_attendance_report_view import TeacherAttendanceReportView


def setup_admin():
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(TeacherAdminView(Teacher, db.session))
    admin.add_view(ReportAdminView(Report, db.session))
    admin.add_view(TeacherAttendanceReportView(
        name='Attenance Report', endpoint='attendance'))
    admin.add_view(MonthlyReportView(
        name='Monthly Report', endpoint='monthly'))
