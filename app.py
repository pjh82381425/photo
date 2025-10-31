from flask import *

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

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/result')
def result():
    return render_template('result.html')

port_num = 5001
host_adress = '0.0.0.0'

if __name__ == '__main__':
    app.run(debug=False, threaded=True, host=host_adress, port=port_num)