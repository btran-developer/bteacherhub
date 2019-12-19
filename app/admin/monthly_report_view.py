from flask_admin import expose
from app.forms import GetMonthlyReportsForm
from app.models import Teacher, Report
from sqlalchemy import and_, or_
from datetime import datetime
from app import excel
from .admin_view import AdminBaseView
import calendar


class MonthlyReportView(AdminBaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = GetMonthlyReportsForm()
        form.teacher.choices = Teacher.get_teachers_for_choices(
            defaultOpt=(0, 'All'))

        if form.validate_on_submit():
            monthly_report_list = [['Teacher', 'Days as main teacher',
                                    'Days as assistant teacher', 'Total days', 'Salary']]

            month = int(form.month.data)
            year = int(form.year.data)
            pay_per_day = int(form.pay_per_day.data)

            if form.teacher.data != 0:
                teachers = Teacher.query.filter_by(id=form.teacher.data)
            else:
                teachers = Teacher.query.all()

            num_days_in_month = calendar.monthrange(year, month)[1]
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month, num_days_in_month).date()

            for teacher in teachers:
                report_row = []
                report_row.append(teacher.teacher_name)
                days_as_main = Report.query.filter(
                    and_(
                        Report.teaching_date >= start_date,
                        Report.teaching_date <= end_date,
                        Report.main_teacher_id == teacher.id
                    )
                ).count()
                days_as_assistant = Report.query.filter(
                    and_(
                        Report.teaching_date >= start_date,
                        Report.teaching_date <= end_date,
                        Report.assistant_teacher_id == teacher.id
                    )
                ).count()
                total_teaching_days = days_as_main + days_as_assistant
                salary = pay_per_day * total_teaching_days
                report_row.append(days_as_main)
                report_row.append(days_as_assistant)
                report_row.append(total_teaching_days)
                report_row.append(salary)
                monthly_report_list.append(report_row)
            return excel.make_response_from_array(
                monthly_report_list, file_type='csv', file_name=f'{month}-{year} monthly report'
            )

        return self.render('admin/monthly.html', form=form)
