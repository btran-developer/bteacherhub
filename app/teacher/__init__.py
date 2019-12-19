from flask import Blueprint, redirect, url_for, request, jsonify, render_template, flash, current_app
from app import db
from app.models import Teacher
from app.forms import AddTeacherForm
from app.auth import admin_required

bp = Blueprint('teacher_bp', __name__)
app = current_app


@bp.route('/teacher/add', methods=['GET', 'POST'])
@admin_required
def add_teacher():
    """
    Add new teacher
    """
    form = AddTeacherForm()

    if form.validate_on_submit():
        teacher = Teacher(teacher_name=form.teacher_name.data)
        db.session.add(teacher)
        db.session.commit()
        flash(message='Teacher is successfully added.', category='success')
        return redirect(url_for('teacher.add_teacher'))

    return render_template('teacher/add_teacher.html', title='Add Teacher', form=form)


@bp.route('/teacher')
@admin_required
def get_teachers():
    """
    Get list of teachers
    """
    teachers = Teacher.query.all()

    return render_template('teacher/teachers_list.html', title='Teachers List',
                           teachers=teachers)


@bp.route('/teacher/<teacher_id>/', methods=['PATCH'])
@admin_required
def update_teacher_name(teacher_id):
    """
    Update teacher name
    """
    teacher = Teacher.query.get(int(teacher_id))
    db.session.add(teacher)

    if not request.form['teacher_name']:
        return jsonify({'error': 'Teacher name is required.'})

    teacher.teacher_name = request.form['teacher_name']
    db.session.commit()
    message = f'Successfully update to {request.form["teacher_name"]}.'

    return jsonify({'message': message})


@bp.route('/teacher/<teacher_id>/set-active')
@admin_required
def set_teacher_active(teacher_id):
    """
    Set teacher active
    """
    teacher = Teacher.query.get(int(teacher_id))
    db.session.add(teacher)
    teacher.is_active = True
    db.session.commit()
    message = f'Successfully set {teacher.teacher_name} active.'

    return jsonify({'message': message})


@bp.route('/teacher/<teacher_id>/set-inactive')
@admin_required
def set_teacher_inactive(teacher_id):
    """
    Set teacher inactive
    """
    teacher = Teacher.query.get(int(teacher_id))
    db.session.add(teacher)
    teacher.is_active = False
    db.session.commit()
    message = f'Successfully set {teacher.teacher_name} inactive.'

    return jsonify({'message': message})
