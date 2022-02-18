# SILKC project Machine Learning algorithm

The SILKC (Skills Integration in a Learning, Knowledge and Career PATHway) project
pursues the goal of simplifying the search of career-changing training to provide
people with a greater professional mobility.

The present code is focused on analysing the data provided by thousands of users 
and institutions, and provide users with recommendations on which training better
fits their career goals.

Final users are looking for a career improvement.
Institutions want to make their training offers more accessible to all.

The [silkc-platform](https://github.com/silkc/silkc-platform) project develops the
user interface and general logic of the application, while this project focuses
on the Machine Learning algorithms behind the training recommendation.

## Installation

This project is meant to be run on a recent Linux distribution.

Requirements:
* Python 3.9 or superior
* pip 20 or superior

To install the required Python modules, run `sh configure.sh`. 
This will execute a `pip install` on the packages defined in `requirements.txt`.

The Docker setup is experimental.

Next, go to the `config/` directory and copy all `.json.dist` files to a local `.json` version of each file.
Open `database.json` and configure a read access to the database used by the `silkc-platform` project.

## Run

### Training

To run, position yourself in the base folder of the project and launch:
```
python3 main.py --config config/configuration.json --train occupation
python3 main.py --config config/configuration.json --train skill
```

This will query the database to aggregate the data, and write the trained model file in the folder defined in `configuration.json`.
It also provides you with feedback on several quality indicators for the algorithm as follows...
```
$ python3 main.py --config config/configuration.json --train occupation
Preparing the OCCUPATION MODEL for the training
The NaN data are: 0
Done training OCCUPATION MODEL
```

To launch the training process as a REST API, use the `--api` argument.

This should show feedback with connection details, like so:
```
$ python3 main.py --config config/configuration.json --api
 * Serving Flask app 'api.api' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 908-224-099
```
You can then load `http://127.0.0.1:5000/training/database` in a browser or in 
Postman to trigger the model training through the database input. 

### API/Inference

Once the API is launched above, you can issue a POST request to `http://127.0.0.1:5000/infer`
with a request body of
```
{
    "model": "occupation",
    "input": { 
        "skill_occupation_id": 2154
    } 
}
```

This will generate a JSON result of the following type (to be improved):
```
{
    "status": 200,
    "response": {
        "message": "Classification model executed",
        "result": [
            "4,5,6,7"
        ],
        "accuracy": 0.14876033060000002,
        "inference_time": 0.0009620189666748047
    }
}
```

## Notes

DISCLAIMER: This project has been funded with support from the European Commission.
This publication [communication] reflects the views only of the author, and the Commission cannot be held responsible for any use which may be made of the information contained therein.