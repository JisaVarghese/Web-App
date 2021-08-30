## python -m http.server
## from the output folder to open http on 8000 port

from flask import Flask, render_template, request, Response
import os
from werkzeug.utils import secure_filename
import main


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = r'C:\Mz_things\JISA\1.LYIT\Dissertation\webApp\cleanedCode\cleanedCode\Favourite_Visitors'


@app.route('/')
def main_page():
   #main.addImage()
   return render_template('login.html')


@app.route('/video_feed_1')
def video_feed_1():
   main.addImage()
   return render_template('login.html')

@app.route('/video_feed_end')
def video_feed_end():
   main.endCapture()
   return render_template('login.html')

@app.route('/uploader', methods = ['GET', 'POST']) 
def upload_file():
   return render_template('image_load.html')


@app.route('/uploader/add', methods = ['GET', 'POST']) 
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      name = request.form['text']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], name +'.jpg'))
   if request.method == "GET":
      name = "file uploaded successfully"

   return render_template('image_load.html',ident=name)

if __name__ == '__main__':

   app.run(debug=True, port=4996)
