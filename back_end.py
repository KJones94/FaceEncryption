from flask import Flask, jsonify
from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
import video_encryption as encrypt
app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return render_template('w3template.html')
    # return render_template('index.html')
@app.route('/api/encryptVideo',methods = ['POST', 'GET'])
def encrypt_video():
    # print("Form", request.form)
    # print("Files",request.files)
    # file = request.files.get('video')
    # print("form", request.form.get('video'))
    # print("files", request.files)
    print(request.method)
    if request.method == 'POST':
        file = request.files.get('video')
        file.save('SavedVideo.avi')
        encrypt.EncryptVideo('SavedVideo.avi')
        # return redirect('/api/encryptVideo')
        return jsonify({"link":"/api/encryptVideo"})
    if request.method == 'GET':
        try:
            return send_file('Encrypted_Video.avi',
                             attachment_filename='Encrypted_Video.avi',
                             as_attachment=True)
        except Exception as e:
            return str(e)

@app.route('/api/verifyVideo',methods = ['POST'])
def verify_video():
    file = request.files.get('video')
    file.save('VerifyVideo.avi')
    result = str(encrypt.VerifyVideo('VerifyVideo.avi'))
    return jsonify({"result": str(result)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)