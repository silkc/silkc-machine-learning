from flask import Flask, request
from flask_restful import Api
import api.training as training
import api.inference as inference

def start_api(ml_config, db_connector, dataframe_path=None, debug=True):
    training.set_config(ml_config)
    training.set_dataset_path(dataframe_path)
    training.set_db(db_connector)
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(training.Training, "/training/<string:source>")

    app.run(debug=debug)