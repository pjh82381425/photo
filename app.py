from flask import *
import cv2
import os

app = Flask(__name__)

base = os.path.join(app.root_path, "static", "captures")
os.makedirs(base, exist_ok=True)
save, ret, frame = None, None, None
selected_photo = []

def generate_frames():
    global ret, frame
    cap = cv2.VideoCapture(1)
    print('카메라 연결 완료')

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # 좌우 반전
            frame = cv2.flip(frame, 1)
            # 프레임을 JPEG 형식으로 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_ = buffer.tobytes()

            # 멀티파트 메시지 형식으로 프레임 생성
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_ + b'\r\n')

app = Flask(__name__)

# app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = 'your_secret_key'

# @app.route('/about')
# def about():
#     return 'About Page'

# @app.route('/user/<username>')
# def show_user_profile(username):
#     return f'User {username}'

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # 디렉토리 트래버설 공격을 방지하기 위한 subpath를 검증
#     if '..' in subpath or subpath.startswith('/'):
#         abort(400, description="잘못된 경로")  # 잘못된 경로일 경우 400 에러를 반환합니다.
#     return render_template(f'{subpath}.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'Do the login'
#     else:
#         return 'Show the login form'

# @app.route('/json')
# def json_example():
#     return jsonify(message="Hello, World!", status=200)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/photo")
def photo():
    global save, selected_photo
    selected_photo = []
    i = 1
    while os.path.exists(os.path.join(base, str(i))):
        i += 1
    save = os.path.join(base, str(i))
    return render_template("photo.html")

@app.route('/video')
def video():
    # 비디오 스트리밍을 위한 Response 객체 생성
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['GET'])
def capture():
    global save, ret, frame
    os.makedirs(save, exist_ok=True)
    if not ret:
        return "err", 500

    i = len([f for f in os.listdir(save) if f.startswith('cap')]) + 1
    filename = f"capture{i}.jpg"
    cv2.imwrite(os.path.join(save, filename), frame)
    print(f'{save}/{filename} 이 촬영됨')
    return ("ok")

@app.route('/select')
def select():
    global save
    files = sorted(
        [f for f in os.listdir(save) if os.path.isfile(os.path.join(save, f))]
    )
    folder_rel = os.path.relpath(save, app.root_path).replace(os.sep, '/')
    return render_template('select.html', folder_rel=folder_rel, files=files) # 예시 뷰 코드

@app.route('/select/<int:item_id>', methods=['POST'])
def select_photo(item_id):
    global save, selected_photo
    files = sorted([f for f in os.listdir(save) if os.path.isfile(os.path.join(save, f))])
    if not 1 <= item_id <= len(files):
        return jsonify(status="error"), 400

    if save not in selected_photo:
        if item_id not in selected_photo:
            selected_photo.append(item_id)
            print(f'{save}/capture{item_id}.jpg 선택')
            print(f'현재 선택된 사진: {selected_photo}')
    return jsonify(status="ok", id=item_id)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_photo(item_id):
    global save, selected_photo
    files = sorted([f for f in os.listdir(save) if os.path.isfile(os.path.join(save, f))])
    if not 1 <= item_id <= len(files):
        return jsonify(status="error"), 400
    
    if save not in selected_photo:
        if item_id in selected_photo:
            selected_photo.remove(item_id)
            print(f'{save}/capture{item_id}.jpg 선택 취소됨')
            print(f'현재 선택된 사진: {selected_photo}')
    return jsonify(status="ok", id=item_id)

@app.route('/edit')
def edit():
    global save, selected_photo
    selected_photo_filenames = [f"capture{i}.jpg" for i in selected_photo]
    return render_template('edit.html', selected_photo_filenames=selected_photo_filenames)
    
@app.route('/view_captures/<path:filename>')
def view_captures(filename):
    return send_from_directory(save, filename)

@app.route('/result')
def result():
    return render_template('result.html')

port_num = 5001
host_adress = '0.0.0.0'

if __name__ == '__main__':
    app.run(debug=False, threaded=True, host=host_adress, port=port_num)