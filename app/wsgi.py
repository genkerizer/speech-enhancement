import os
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from .controller import backend
from .log_func import logger
from .database import collection

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.config['RELATIVE_PATH'] = os.path.realpath(os.path.dirname(__file__))
app.config['DATABASE'] = os.path.join(app.config['RELATIVE_PATH'], 'statics', 'database')
app.config['INPUT_DIR'] = os.path.join(app.config['DATABASE'], 'inputs')
app.config['OUTPUT_DIR'] = os.path.join(app.config['DATABASE'], 'outputs')

MAX_TIME  = 24 * 60 * 60

if not os.path.exists(app.config['DATABASE']):
    os.makedirs(app.config['DATABASE'])

if not os.path.exists(app.config['INPUT_DIR']):
    os.makedirs(app.config['INPUT_DIR'])

if not os.path.exists(app.config['OUTPUT_DIR']):
    os.makedirs(app.config['OUTPUT_DIR'])


def _insert_db(file_name, result_path, duration):
    num_id = collection.count_documents({})
    now = datetime.now()
    id = "".join(now.strftime("%Y%m%d%H%M%S")) + f'_{num_id}'
    post = {
        "id": id,
        "fileName": file_name,
        "formatFile": file_name.split('.')[-1],
        "path": result_path,
        "createTime": now,
        "duration": f'{duration}s'
    }
    collection.insert_one(post)


def _delete_db():
    now = datetime.datetime.now()
    start_progress = now.replace(hour=17, minute=0, second=0, microsecond=0)
    end_progress = now.replace(hour=17, minute=60, second=0, microsecond=0)
    pop_id_path = []
    if now > start_progress and now < end_progress:
        for col in collection.find():
            if (now - col['createTime']).total_seconds() > MAX_TIME:
                pop_id_path.append([col['id'], col['path']])
        if len(pop_id_path) > 0:
            for id_path in pop_id_path:
                id_,delpath = id_path
                os.remove(delpath)
                collection.delete_one({'id': id_})
    return None

  

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    
    if request.method == 'POST':
        logger.log_info('method:\t{request.method}')
        try:
            f =request.files['file']
            if f.filename != '':
                logger.log_info(f'filename:\t{f.filename}')
                input_path = os.path.join(app.config['INPUT_DIR'], f.filename)
                f.save(input_path)
                
                start = time.time()
                output_path, duration = backend(input_path, output_dir=app.config['OUTPUT_DIR'])
                process_time = time.time() - start
                logger.log_info(f'time:\t{round(process_time, 2)}')

                name = output_path.split('/')[-1]
                logger.log_info(f'status:\t{200}')
                
                vis_input_path = os.path.join('statics/database/inputs', name)
                vis_output_path = os.path.join('statics/database/outputs', name)
                _insert_db(name, vis_output_path, duration)
                # print(">>>>>>>>>>>>")
                # _delete_db()
                # print(">>>>>>>>>>>>>B")

                return jsonify(result={'output_path': vis_output_path, 'input_path': vis_input_path})
        except:
            logger.log_exception("Error occurred while printing GeeksforGeeks") 
    return render_template("homepage.html")
    
if __name__ == '__main__':
    app.run(debug=True)