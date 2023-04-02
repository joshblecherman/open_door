from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

def create_app():
    app = ...

    from . import auth
    app.register_blueprint(auth.bp)

    return app

if __name__ == '__main__':
    app.run()
