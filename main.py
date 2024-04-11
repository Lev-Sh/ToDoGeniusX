from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template(f"mainpage/mainpage.html", title="ToDoGenius")
@app.route('/login')
def index():
    return render_template(f"login/login.html", title="ToDoGenius")


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
