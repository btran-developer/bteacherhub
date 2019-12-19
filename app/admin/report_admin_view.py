from .admin_view import AdminModelView
from wtforms import TextAreaField


class ReportAdminView(AdminModelView):
    column_list = ('main_teacher', 'assistant_teacher',
                   'submitted_by', "teaching_date", "submit_date")

    def scaffold_form(self):
        form_class = super(ReportAdminView, self).scaffold_form()
        form_class.teaching_content = TextAreaField('Teaching Content')
        return form_class
