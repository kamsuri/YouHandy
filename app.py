from flask import Flask, render_template, request
import os
from apiclient.errors import HttpError
from werkzeug import secure_filename
from oauth2client.tools import argparser
from upload import initialize_upload, get_authenticated_service
from my_uploads import main
from download import down

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
    try:
        text = main()
        return render_template('index.html', list=text)
    except HttpError, e:
        return render_template('index.html', text="An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    descp = request.form['descp']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        check = main()
        if filename in check:
          return render_template('index.html', text="Video %s already exists" % filename)
        # Move the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Specifying the filename, title, description and other arguments
        argparser.add_argument("--file", required=True,
                               help="Video file to upload", default="uploads/"+filename)
        argparser.add_argument("--title", help="Video title",
                               default=filename)
        argparser.add_argument("--description", help="Video description",
                               default=descp)
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
            return render_template('index.html', text="Video %s Uploaded Successfully" % filename)
        except HttpError, e:
            return render_template('index.html', text="An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)



@app.route('/download', methods=['GET','POST'])
def download():
  url = request.form['link']
  try:
    text = down(url)
    return render_template('index.html', text=text)
  except HttpError, e:
            return render_template('download.html', text="An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def list():
  try:
    text = main()
    return render_template('index.html', text=text)
  except HttpError, e:
            return render_template('index.html', text="An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

if __name__ == "__main__":
    app.run(debug=True)