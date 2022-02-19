from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = ''

app = Flask(__name__)
app.secret_key = "\xee\x18]\xed\\\xe9F\xee\xcd\xee\x9f~\xb3\xcai\xa5\xb2?\xe8_y\xe8!"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/json', methods=['GET'])
def json():
    return open("widgets.json").read()


@app.route('/json_ru', methods=['GET'])
def json_ru():
    return io.open("widgetsRU.json", encoding='utf-8').read()


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/user', methods=['GET'])
def user():
    return io.open("user.json", encoding='utf-8').read()


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/admin', methods=['POST'])
def get_image():
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        im = Image.open(file)
        im_new = crop_max_square(im)
        im_new.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), quality=95)
        return jsonify(request.json)


@app.route('/json', methods=['POST'])
def update_json():
    with open("widgets.json", "w") as out:
        out.write(str('{"widgets":' + request.json['data'] + '}'))
    return jsonify(request.json)


@app.route('/json_ru', methods=['POST'])
def update_json_ru():
    with open("widgetsRU.json", "w", encoding='utf-8') as out:
        out.write(str('{"widgets":' + request.json['dataRU'] + '}'))
    return jsonify(request.json)


@app.route('/123', methods=['POST'])
def get_request():
    if 'data' in request.json:
        print(request.json['data'])
    if 'file' in request.files:
        print(123)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            im = Image.open(file)
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), quality=95)
    return jsonify(request.json)


app.run('0.0.0.0', debug=True)
