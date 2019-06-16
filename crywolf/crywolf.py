from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', section = "Section title passed from View to Template",
                            text = "Text passed from View to Template")

@app.route('/prequestionnaire')
def prequestionnaire():
    return render_template('prequestionnaire.html')

@app.route('/experiment')
def experiment():
    return render_template('experiment.html')

@app.route('/postsurvey')
def postsurvey():
    return render_template('postsurvey.html')

if __name__ == "__main__":
    app.run(debug=True)