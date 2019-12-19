from flask import Blueprint, render_template, redirect, url_for, jsonify, flash, request, current_app, abort
from app.forms import ReportForm, GetReportsForm, GetMonthlyReportsForm
from app.models import Report, Teacher
from app.auth import login_required, admin_required
from app import db, excel
from sqlalchemy import and_, or_
from datetime import datetime
import calendar

bp = Blueprint('report_bp', __name__)
app = current_app


@bp.route('/report/form', methods=['GET', 'POST'])
@login_required
def submit_report():
    """
    Create and submit report
    """
    form = ReportForm()
    form.main_teacher.choices = Teacher.get_teachers_for_choices()
    form.assistant_teacher.choices = Teacher.get_teachers_for_choices()
    form.submitted_by.choices = Teacher.get_teachers_for_choices()

    if form.validate_on_submit():
        report = Report(
            main_teacher_id=form.main_teacher.data,
            assistant_teacher_id=form.assistant_teacher.data,
            teaching_date=form.teaching_date.data,
            teaching_content=form.teaching_content.data,
            student_attendance=form.student_attendance.data,
            submitted_by_id=form.submitted_by.data
        )
        db.session.add(report)
        db.session.commit()
        flash(message='Report is successfully submitted.', category='success')
        return redirect(url_for('index.index'))

    return render_template('report/report_submit.html', title='Submit a Report', form=form)


@bp.route('/report/<id>', methods=['GET', 'DELETE'])
@admin_required
def get_or_delete_on_report(id):
    """
    Get or delete a report
    """
    report = Report.query.get(id)

    if request.method == 'DELETE' and request.is_xhr:
        db.session.delete(report)
        db.session.commit()
        flash(message='Report is deleted successfully.', category="success")
        return jsonify({'message': 'Report is deleted.'}), 200

    return render_template('report/report_detail.html', title="Report Detail", report=report)


@bp.route('/report')
@admin_required
def get_reports():
    """
    Get report for specified date period
    """
    form = GetReportsForm(formdata=request.args)
    form.teacher.choices = Teacher.get_teachers_for_choices(
        defaultOpt=(0, 'All'))

    if len(list(request.args.keys())) > 0 and request.is_xhr:
        form.validate()
        result = {'data': {}}
        page = request.args.get('page', 1, type=int)

        if len(form.teacher.errors) == 0 \
                or len(form.from_date.errors) == 0 \
                or len(form.to_date.errors) == 0:
            from_date = form.from_date.data
            to_date = form.to_date.data
            teacher_id = form.teacher.data

            if teacher_id == 0:
                search_type = 'ALL'
                reports = Report.query.filter(
                    and_(
                        Report.teaching_date >= from_date,
                        Report.teaching_date <= to_date
                    )
                ).order_by(Report.teaching_date.desc())
                result['data']['total_reports'] = reports.count()

            else:
                search_type = 'BY_TEACHER'
                reports = Report.query.filter(
                    and_(
                        Report.teaching_date >= from_date,
                        Report.teaching_date <= to_date,
                        or_(
                            Report.main_teacher_id == teacher_id,
                            Report.assistant_teacher_id == teacher_id
                        )
                    )
                ).order_by(Report.teaching_date.desc())
                result['data']['teacher_attendance'] = reports.count()
                result['data']['day_as_main'] = len(list(filter(
                    lambda report: report.main_teacher_id == form.teacher.data, reports)))
                result['data']['day_as_assistant'] = len(list(filter(
                    lambda report: report.assistant_teacher_id == form.teacher.data, reports)))

            paginated_reports = reports.paginate(
                page, app.config['REPORTS_PER_PAGE'], False)

            result['data']['search_type'] = search_type
            result['data']['reports'] = [report.to_dict()
                                         for report in paginated_reports.items]
            result['next_page_num'] = paginated_reports.next_num if paginated_reports.has_next else None

        result['errors'] = {
            'teacher_errors': form.teacher.errors,
            'from_date_errors': form.from_date.errors,
            'to_date_errors': form.to_date.errors
        }

        result['number_of_errors'] = len(form.teacher.errors) + \
            len(form.from_date.errors) + \
            len(form.to_date.errors)

        return jsonify(result)

    return render_template('report/get_reports.html', title='Get Reports', form=form)


@bp.route('/report/get-csv')
@admin_required
def get_report_csv():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    reports = Report.query.filter(
        and_(Report.teaching_date >= from_date, Report.teaching_date <= to_date)).all()
    column_names = ['teaching_date', 'main_teacher', 'assistant_teacher',
                    'teaching_content', 'student_attendance', 'submitted_by']
    file_name = f'{from_date} - {to_date}'
    return excel.make_response_from_query_sets(reports, column_names, file_type='csv', file_name=file_name)


@bp.route('/report/delete')
@admin_required
def delete_reports():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    try:
        Report.query.filter(and_(Report.teaching_date >= from_date,
                                 Report.teaching_date <= to_date)).delete()
        db.session.commit()
        return jsonify({'message': 'Successfully delete reports.'})
    except:
        return jsonify({'message': 'Failed to delete reports.'}), 500


@bp.route('/report/monthly-report', methods=['GET', 'POST'])
@admin_required
def get_monthly_report():
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

    return render_template('report/get_monthly_report.html', title='Get Monthly Report', form=form)
