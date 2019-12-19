from flask_admin import expose
from .admin_view import AdminBaseView
from app.forms import GetReportsAdminForm
from app.models import Report
from app import excel
from sqlalchemy import and_, or_
from flask import redirect, flash


class TeacherAttendanceReportView(AdminBaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = GetReportsAdminForm()

        if form.validate_on_submit():
            from_date = form.from_date.data
            to_date = form.to_date.data

            reports = Report.query.filter(
                and_(Report.teaching_date >= from_date, Report.teaching_date <= to_date)).all()

            if len(reports) == 0:
                flash(message='No reports are found.')
                return redirect(self.url)

            column_names = ['teaching_date', 'main_teacher', 'assistant_teacher',
                            'teaching_content', 'student_attendance', 'submitted_by']
            file_name = f'{from_date} - {to_date}'
            return excel.make_response_from_query_sets(reports, column_names, file_type='csv', file_name=file_name)

        return self.render('admin/teacher_attendance.html', form=form)
