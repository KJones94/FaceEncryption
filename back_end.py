from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
import video_encryption as encrypt
app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/api/encryptVideo',methods = ['POST', 'GET'])
def encrypt_video():
    # print("Form", request.form)
    # print("Files",request.files)
    # file = request.files.get('video')
    # print("form", request.form.get('video'))
    # print("files", request.files)
    if request.method == 'POST':
        file = request.files.get('video')
        file.save('SavedVideo.mp4')
        encrypt.EncryptVideo('SavedVideo.mp4')
        return redirect('/api/encryptVideo')
    if request.method == 'GET':
        try:
            return send_file('Encrypted_Video.mp4',
                             attachment_filename='video.mp4',
                             as_attachment=True)
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run()