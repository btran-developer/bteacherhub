from .admin_view import AdminModelView


class TeacherAdminView(AdminModelView):
    column_list = ('teacher_name', 'is_active')
    column_searchable_list = ('teacher_name',)
