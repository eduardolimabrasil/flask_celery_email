"""Form."""
from wtforms import Form, StringField, validators


class SendEmailForm(Form):
    """Send Email Form."""

    email = StringField('Email Address', [validators.Length(min=6, max=35),
                                          validators.DataRequired(),
                                          validators.Email()])
    email_body = StringField(
        'Body Email',
        [
            validators.length(min=5, max=140),
            validators.data_required()
        ]
    )
