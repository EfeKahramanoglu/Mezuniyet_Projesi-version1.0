
from flask import Flask, render_template, request, redirect, url_for
import os
from model import get_class
app = Flask(__name__)

# Yüklenen dosyaların kaydedileceği dizin
UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dosyanın izin verilen bir uzantıya sahip olup olmadığını kontrol eden fonksiyon
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sa')
def goruntu():
    return render_template('gorsel.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Görseli model ile analiz et
        class_name, confidence = get_class(file_path)
        
        # Sonuçları kullanıcıya göster
        return render_template('result.html', class_name=class_name, confidence=confidence, filename=filename)

    return 'Geçersiz dosya tipi'

if __name__ == '__main__':
    # images klasörünün var olduğundan emin olalım
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=8080)






if __name__ == '__main__':
    app.run(debug=True)