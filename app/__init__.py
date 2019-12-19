from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
import flask_excel as excel
import logging
from app.logging_handlers import email_logging_handler as SMTPHandler
from app.admin.admin_view import AdminHomeView


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(index_view=AdminHomeView(
    name='Home',
    template='admin/index.html'
))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    excel.init_excel(app)
    admin.init_app(app)

    from app.account import bp as account_bp
    app.register_blueprint(account_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp)

    from app.report import bp as report_bp
    app.register_blueprint(report_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin.setup import setup_admin
    setup_admin()

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='TeacherHub Error',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app
