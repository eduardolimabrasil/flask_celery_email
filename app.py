"""App."""
from flask import Flask, render_template, request
from celery import Celery

from forms import SendEmailForm

APP = Flask(__name__, template_folder="template")

APP.config['CELERY_BROKER_URL'] = 'amqp://localhost:5672'
APP.config['CELERY_RESULT_BACKEND'] = 'amqp://localhost:5672'


CELERY = Celery(APP.name, broker=APP.config['CELERY_BROKER_URL'])
CELERY.conf.update(APP.config)


@APP.route('/')
def index():
    """Pagina Principal."""
    return render_template("form.html")


@APP.route('/enviar', methods=['POST'])
def email():
    """Enviar e-mail."""
    form = SendEmailForm(request.form)
    if request.method == 'POST' and form.validate():
        data_email = {
            "email": form.email.data,
            "body": form.email_body.data
        }
        send_email.delay(data_email)
        message = "Enviado com sucesso!"
    else:
        message = "Problemas no formulário"
    return render_template("form.html", message=message)


@CELERY.task
def send_email(data_email) -> bool:
    """Worker to send e-mail."""
    print(data_email.get('email'),data_email.get('body'))
    return data_email


if __name__ == '__main__':
    APP.run()
