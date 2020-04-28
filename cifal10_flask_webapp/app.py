from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from model_cifal_10.server import predict
from skimage import io

UPLOAD_FOLDER = './media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key='santoshtmp'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/upload")
def upload():
    return render_template('upload_img.html')

#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/output",  methods = ['GET', 'POST'])
def output():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        if file_name == '':
            flash('you have not selected the image')
            return redirect(url_for('upload')) #it passes to  'http://127.0.0.1:5000/upload'
        ext=file_name.rsplit('.')[1]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('you have  selected the wrong file '+ext)
            flash('please select images : [ jpg, png, jpeg ]')
            return redirect(url_for('upload'))  # it passes to  'http://127.0.0.1:5000/upload
    else:
        flash('please select images : [ jpg, png, jpeg ]')
        return redirect(url_for('upload'))
    #call for model to predict outcome
    img_data=io.imread('./media/'+file.filename)
    out_name,probability = predict(img_data)
    link='./media/'+file.filename
    #send_from_directory('media',file.filename, as_attachment=True) ## to download the uploaded images..
    return render_template('show_output.html' ,ext=ext , imglink=link ,filename=file.filename ,class_name=out_name, class_prob=probability)

@app.route("/output/<filename>" )
def send_img(filename):
    return send_from_directory('media',filename)


if __name__ == "__main__":
    app.run(debug = True)