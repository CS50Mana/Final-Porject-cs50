
import re 
import os  
from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

#-----Google_cloud_part-----#
from google.cloud import texttospeech
from google.cloud import texttospeech_v1
from convert import convert2

#----Setting a virtual inv----#
#I had first to set a virtual environment for this project:
#py -m venv "pyvenv"
# I then installed different packages related to the project
#------------------------------#

credential_path= "C:\\Users\\Manel\\Desktop\\CS_50\\GoogleTextToSpeech\\massive-hexagon-351107-d6940f0d83db.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=credential_path

# configure application
app = Flask(__name__)
app.secret_key = "MoiManel070988?"
Bootstrap(app)
bcrypt=Bcrypt(app)

# allows our app and flask to work together when looging in 
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

#initialize Database and connecting it with the app
db=SQLAlchemy(app)
# configure sqlachemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["ALLOWED_EXTENTIONS"]=["PDF"]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].upper() in app.config["ALLOWED_EXTENTIONS"]

#----setting up paths for uploads and download dolders----#
UPLOAD_FOLDER="C:\\Users\\Manel\\Desktop\\CS_50\\GoogleTextToSpeech\\static\\uploads"
#os.path.dirname(os.path.abspath(__file__)) + "/uploads/"

app.config["UPLOAD_FOLDER"]= UPLOAD_FOLDER
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# used to reload the user object from the user id stored in the session 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----defining different classes----#
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

def __repr__(self):
        return '<User %r>' % self.username

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4, max=20)],render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"Placeholder": "Password"})
    
    submit = SubmitField("Sign in")
    
    #checks if the username already entered exists or not 
    def validate_username(self, username):
        existing_user_username= User.query.filter_by(
            username=username.data).first()
        print(existing_user_username)
        if existing_user_username:
            raise ValidationError(
            "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password= PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"Placeholder": "Password"})
    
    submit = SubmitField("Login")
    
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()],)
    start_page= StringField(validators=[InputRequired()], render_kw={"placeholder": "Insert a start page"})
    end_page= StringField(validators=[InputRequired()], render_kw={"placeholder": "Insert an end page"})
    submit = SubmitField("Upload/Download File")
    
#-----defining the routes----#
  
@app.route("/")
#@login_required
def index():
    return render_template("index.html", title="Home")

@app.route("/login", methods=["POST", "GET"])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Logged in successfully {form.username.data}!", category="success")
                return redirect (url_for("index"))
            else:
                flash(f"Login unsuccessful for {form.username.data}!", category="danger")
    return render_template("login.html", form=form)   


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        new_user= User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", category="success")
        return redirect(url_for('login'))
    else:
        return render_template("register.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

            
@app.route("/Upload", methods=["POST", "GET"] )
@login_required
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        startpage=form.start_page.data
        endpage=form.end_page.data
        # grab the file 
        file= form.file.data 
        if allowed_file(file.filename):
            filename= secure_filename(file.filename)
            print(filename)
            # save it in uploads_file
            file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename)) 
            process_file(filename=filename,startpage=startpage, endpage=endpage)
            return redirect(url_for("uploaded_file",filename="audio_file_pdf.mp3"))       
    return render_template("Upload.html", form= form)

        
@app.route("/download/<filename>")
def uploaded_file(filename):
   return send_from_directory(app.config['DOWNLOAD_FOLDER'],"audio_file_pdf.mp3", as_attachment=True)   


#-----process_file function uses google API TextToSpeech----#
def process_file(filename, startpage, endpage):
    text=convert2(filename,startpage, endpage)
    print(text)
    print(startpage)
    print(endpage)
    #instantiates a client
    client=texttospeech_v1.TextToSpeechClient()
    #Set the text input to be sythesized
    synthesis_input= texttospeech_v1.SynthesisInput(text=text)

    #Build the voice request, select the language code fr-FR and ssml
    # voice gender FEMALE 
    voice=texttospeech_v1.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
            )

    # Select the type of audio you want returned 
    audio_config=texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
            )

    #Perform the text-to-speech request on the input with the selected
    # voice parameters and audio file type
    response=client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
            )
    # The response's audio_content is binary
    with open(app.config["DOWNLOAD_FOLDER"] + "audio_file_pdf.mp3",'wb') as output:
        #write the response to the output file.
        output.write(response.audio_content)
        print("Audio content written to file audio_file_pdf.mp3")  
    return output    
    
    
#if we get any errors we can cast them immediatlly
if __name__ == "__main__":
    app.run(debug=True)
    

