from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Welcome to our home page'

if __name__ == '__main__':
    app.run()
