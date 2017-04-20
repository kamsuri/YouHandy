from flask import Flask, render_template, request
import os
from apiclient.errors import HttpError
from werkzeug import secure_filename
from oauth2client.tools import argparser
from upload import initialize_upload, get_authenticated_service


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['mp4'])
# These are the allowed privacy status
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Specifying the filename, title, description and other arguments
        argparser.add_argument("--file", required=True,
                               help="Video file to upload", default=filename)
        argparser.add_argument("--title", help="Video title",
                               default=filename)
        argparser.add_argument("--description", help="Video description",
                               default="Test Description")
        argparser.add_argument("--category", default="22",
                               help="Numeric video category. ")
        argparser.add_argument("--keywords",
                               help="Video keywords, comma separated",
                               default="")
        argparser.add_argument("--privacyStatus",
                               choices=VALID_PRIVACY_STATUSES,
                               default=VALID_PRIVACY_STATUSES[0],
                               help="Video privacy status.")
        args = argparser.parse_args(["--file", "uploads/"+filename])
        youtube = get_authenticated_service(args)
        try:
            initialize_upload(youtube, args)
            print "Video Uploaded Successfully"
            return render_template('index.html')
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
