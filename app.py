from flask import *
import cv2

app = Flask(__name__)

def generate_frames():
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
            frame = buffer.tobytes()

            # 멀티파트 메시지 형식으로 프레임 생성
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
def capture():
    return render_template("photo.html")

@app.route('/video')
def video():
    # 비디오 스트리밍을 위한 Response 객체 생성
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/select') # 위의 주석 처리된 예시 코드로 보안관련 수정 필요함
def select():
    return render_template('select.html')

@app.route('/edit') # 위의 주석 처리된 예시 코드로 보안관련 수정 필요함
def edit():
    return render_template('edit.html')

@app.route('/result') # 위의 주석 처리된 예시 코드로 보안관련 수정 필요함
def result():
    return render_template('result.html')

port_num = 5001
host_adress = '0.0.0.0'

if __name__ == '__main__':
    app.run(debug=False, threaded=True, host=host_adress, port=port_num)