from .admin_view import AdminModelView
from wtforms import PasswordField
from app import db
from flask_admin.form import rules
from flask import flash


class UserAdminView(AdminModelView):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'is_admin')
    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash',)
    form_edit_rules = (
        'username', 'is_admin',
        rules.Header('Reset Password'),
        'new_password', 'confirm'
    )
    form_create_rules = (
        'username', 'password', 'is_admin'
    )

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm New Password')
        return form_class

    def create_model(self, form):
        model = self.model(username=form.username.data,
                           is_admin=form.is_admin.data)
        model.set_password(form.password.data)
        db.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
        return model

    def update_model(self, form):
        model = self.model(username=form.username.data,
                           is_admin=form.is_admin.data)

        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('New password and confirm must match')
                return False
            model.set_password(form.new_password.data)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()
        return True
