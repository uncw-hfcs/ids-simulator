from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title = "Title passed from View to Template",
                            text = "Text passed from View to Template")

if __name__ == "__main__":
    app.run(debug=True)