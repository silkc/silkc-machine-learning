from flask import Flask, request
from flask_restful import Api
import training

def start_api(ml_config, dataframe_path=None):
    training.set_config(ml_config)
    training.set_dataset_path(dataframe_path)
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(training.Training, "/training/<string:source>")