from flask import g, redirect, flash, url_for
from flask_admin import BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView


class AdminRestriction():
    @staticmethod
    def is_accessible():
        return g.user and g.user.is_admin

    @staticmethod
    def inaccessible_callback(name, **kwargs):
        flash('Insufficient privilege.', category='danger')
        return redirect(url_for('index.index'))


class AdminModelView(ModelView):
    def is_accessible(self):
        return AdminRestriction.is_accessible()

    def inaccessible_callback(self, name, **kwargs):
        return AdminRestriction.inaccessible_callback(name, **kwargs)


class AdminBaseView(BaseView):
    def is_accessible(self):
        return AdminRestriction.is_accessible()

    def inaccessible_callback(self, name, **kwargs):
        return AdminRestriction.inaccessible_callback(name, **kwargs)


class AdminHomeView(AdminIndexView):
    def is_accessible(self):
        return AdminRestriction.is_accessible()

    def inaccessible_callback(self, name, **kwargs):
        return AdminRestriction.inaccessible_callback(name, **kwargs)
