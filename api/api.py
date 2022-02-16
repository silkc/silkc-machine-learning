from flask import Flask, request
from flask_restful import Api
import api.training as training
import api.inference as inference

def start_api(config, db_connector, dataframes_path=None, debug=True):
    training.set_config(config)
    training.set_datasets_path(dataframes_path)
    training.set_db(db_connector)
    inference.set_config(config=config)
    inference.set_db(db_connector)
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(training.Training, f"/{config['api']['training']['base_uri']}/<string:model>/<string:source>")
    api.add_resource(inference.Inference, f"/{config['api']['inference']['base_uri']}")

    app.run(debug=debug)