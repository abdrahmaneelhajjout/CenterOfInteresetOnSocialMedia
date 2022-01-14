from flask import Flask, render_template, request, redirect
import processing as prc  # jupyter methode and statements


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    url = request.form['url']
    if url.startswith('https://www.facebook.com') == False:
        return render_template('index.html')

    return render_template('output3.html', set=prc.start(url))


if __name__ == '__main__':
    app.run(debug=True)
