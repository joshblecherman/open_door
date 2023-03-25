from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Welcome to the template for the Open Door portal'

if __name__ == '__main__':
    app.run()
