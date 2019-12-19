from logging.handlers import SMTPHandler


class email_logging_handler(SMTPHandler):
    def emit(self, record):
        import smtplib
        import ssl
        from email.message import EmailMessage
        import email.utils

        context = ssl.create_default_context()

        port = self.mailport
        if not port:
            port = smtplib.SMTP_SSL_PORT
        with smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout, context=context) as smtp:
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
