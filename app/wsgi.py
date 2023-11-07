import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from .controller import backend

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.config['RELATIVE_PATH'] = os.path.realpath(os.path.dirname(__file__))
app.config['DATABASE'] = os.path.join(app.config['RELATIVE_PATH'], 'statics', 'database')
app.config['INPUT_DIR'] = os.path.join(app.config['DATABASE'], 'inputs')
app.config['OUTPUT_DIR'] = os.path.join(app.config['DATABASE'], 'outputs')
if not os.path.exists(app.config['DATABASE']):
    os.makedirs(app.config['DATABASE'])

if not os.path.exists(app.config['INPUT_DIR']):
    os.makedirs(app.config['INPUT_DIR'])

if not os.path.exists(app.config['OUTPUT_DIR']):
    os.makedirs(app.config['OUTPUT_DIR'])


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        f =request.files['file']
        if f.filename != '':
            input_path = os.path.join(app.config['INPUT_DIR'], f.filename)
            f.save(input_path)
            output_path = backend(input_path, output_dir=app.config['OUTPUT_DIR'])
            name = output_path.split('/')[-1]
            return jsonify(result={'output_path': os.path.join('statics/database/outputs', name), 'input_path': os.path.join('statics/database/inputs', name)})
    return render_template("homepage.html")
    
if __name__ == '__main__':
    app.run(debug=True)