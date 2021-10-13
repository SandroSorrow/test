from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired, NumberRange


class LogInForm(FlaskForm):
    e_mail = StringField("E-mail: ",
                         validators=[DataRequired(), Email()])
    password = PasswordField("Password: ",
                             validators=[Length(min=9, max=24), InputRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    key = StringField("Registration Key: ",
                      validators=[DataRequired(), Length(min=9, max=12)])
    e_mail = StringField("E-mail: ",
                         validators=[DataRequired(), Email()])
    password1 = PasswordField("Password: ",
                              validators=[Length(min=9, max=24), InputRequired()])
    password2 = PasswordField("Repeat password: ",
                              validators=[Length(min=9, max=24), InputRequired()])
    submit = SubmitField("Sign Up")


class NewAccForm(FlaskForm):
    name = StringField("Name*: ",
                       validators=[DataRequired()])
    surname = StringField("Surname: ", default='')
    sex = SelectField("Sex*: ",
                      render_kw={'class': 'form-control'},
                      validate_choice=[DataRequired()],
                      choices=[("Male", "Male"),
                               ("Female", "Female")
                               ])
    month = SelectField("Month*: ",
                        render_kw={'class': 'form-control'},
                        validate_choice=[DataRequired()],
                        choices=[("January", "January"),
                                 ("February", "February"),
                                 ("March", "March"),
                                 ("April", "April"),
                                 ("May", "May"),
                                 ("June", "June"),
                                 ("Jule", "Jule"),
                                 ("August", "August"),
                                 ("September", "September"),
                                 ("October", "October"),
                                 ("November", "November"),
                                 ("December", "December")
                                 ])
    day = IntegerField("Day*: ",
                       validators=[NumberRange(min=1, max=31), InputRequired()],
                       default=1)
    post = StringField("Post*: ", validators=[DataRequired()])
    vision = SelectField("Vision*: ",
                         render_kw={'class': 'form-control'},
                         validate_choice=[DataRequired()],
                         choices=[("None", "None"),
                                  ("Anemo", "Anemo"),
                                  ("Cryo", "Cryo"),
                                  ("Dendro", "Dendro"),
                                  ("Electro", "Electro"),
                                  ("Geo", "Geo"),
                                  ("Hydro", "Hydro"),
                                  ("Pyro", "Pyro")
                                  ])
    weapon = SelectField("Weapon*: ",
                         render_kw={'class': 'form-control'},
                         validate_choice=[DataRequired()],
                         choices=[("None", "None"),
                                  ("Bow", "Bow"),
                                  ("Catalyst", "Catalyst"),
                                  ("Claymore", "Claymore"),
                                  ("Spear", "Spear"),
                                  ("Sword", "Sword")
                                  ])
    description = TextAreaField("About you: ", default=' ')
    submit = SubmitField("Save")


class MissionsForm(FlaskForm):
    status = SelectField("Incident type: ",
                         coerce=int,
                         render_kw={'class': 'form-control'},
                         validate_choice=[DataRequired()],
                         choices=[(0, "Not complete"),
                                  (1, "Complete"),
                                  (2, "Need support",),
                                  (3, "All"),
                                  ])
    submit = SubmitField("Search")


class ReportForm(FlaskForm):
    status = SelectField("Incident type: ",
                         coerce=int,
                         render_kw={'class': 'form-control'},
                         validate_choice=[DataRequired()],
                         choices=[(0, "Not complete"),
                                  (1, "Complete"),
                                  (2, "Need support"),
                                  ])
    report = TextAreaField("Report: ")
    submit = SubmitField("Send")


class MessageForm(FlaskForm):
    from_name = StringField("Your name: ",
                            validators=[DataRequired()])
    from_email = StringField("Your e-mail: ",
                          validators=[DataRequired(), Email()])
    # StringField() - поле для однострочного ввода
    # DataRequired() - "обязательное поле"
    to_mail = StringField("To e-mail: ",
                          validators=[DataRequired(), Email()])
    # Email() - проверка формата введенного email
    message = TextAreaField("Message: ",
                            validators=[DataRequired()])
    # TextAreaField() - поле для многострочного ввода
    submit = SubmitField("Send")
    # кнопка с надписью, отправляющая данные на сервер


class IncidentForm(FlaskForm):
    from_name = StringField("Your name: ",
                            validators=[DataRequired()])
    place = StringField("Region: ",
                        validators=[DataRequired()])
    incident_type = SelectField("Incident type: ",
                                coerce=int,
                                render_kw={'class': 'form-control'},
                                validate_choice=[DataRequired()],
                                choices=[(0, "Commissions"),
                                         (1, "Wild animals"),
                                         (2, "Bandits"),
                                         (3, "Abyss Mages"),
                                         (4, "The Fatui"),
                                         (5, "Anomaly")
                                         ])
    incident_description = TextAreaField("Description: ",
                                         validators=[DataRequired()])
    submit = SubmitField("Submit")


class CheckForm(FlaskForm):
    incident_id = StringField("Commission ID: ",
                              validators=[DataRequired(), Length(min=1)]
                              )
    submit = SubmitField("Submit")
