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
`python3 main.py  -mlc config/configuration.json --train total`

This will query the database to aggregate the data, and write the trained model file in the folder defined in `configuration.json`.
It also provides you with feedback on several quality indicators for the algorithm as follows...
```
$ python3 main.py -mlc config/ml_config.json --train total
Preparing model training...
Extracting features...
Training model...
Init 1/1 with method k-means++
Inertia for init 1/1: 6.0
[MiniBatchKMeans] Reassigning 1 cluster centers.
Minibatch step 1/100: mean batch inertia: 0.6666666666666666
Minibatch step 2/100: mean batch inertia: 1.3333333333333333, ewa inertia: 1.3333333333333333
Minibatch step 3/100: mean batch inertia: 1.0136054421768708, ewa inertia: 1.0136054421768708
Minibatch step 4/100: mean batch inertia: 0.48148148148148145, ewa inertia: 0.48148148148148145
Minibatch step 5/100: mean batch inertia: 0.58203125, ewa inertia: 0.58203125
Minibatch step 6/100: mean batch inertia: 0.3922902494331066, ewa inertia: 0.3922902494331066
Minibatch step 7/100: mean batch inertia: 0.4398148148148149, ewa inertia: 0.4398148148148149
Minibatch step 8/100: mean batch inertia: 0.1203231292517007, ewa inertia: 0.1203231292517007
Minibatch step 9/100: mean batch inertia: 0.8799048751486326, ewa inertia: 0.8799048751486326
Minibatch step 10/100: mean batch inertia: 0.5673469387755102, ewa inertia: 0.5673469387755102
Minibatch step 11/100: mean batch inertia: 0.5291666666666667, ewa inertia: 0.5291666666666667
Minibatch step 12/100: mean batch inertia: 0.3192148760330578, ewa inertia: 0.3192148760330578
Minibatch step 13/100: mean batch inertia: 0.6069628229363578, ewa inertia: 0.6069628229363578
Minibatch step 14/100: mean batch inertia: 0.24016403947199794, ewa inertia: 0.24016403947199794
Minibatch step 15/100: mean batch inertia: 0.2661682686602587, ewa inertia: 0.2661682686602587
Minibatch step 16/100: mean batch inertia: 0.5908539944903582, ewa inertia: 0.5908539944903582
Minibatch step 17/100: mean batch inertia: 0.12515560662644834, ewa inertia: 0.12515560662644834
Minibatch step 18/100: mean batch inertia: 0.4896296296296297, ewa inertia: 0.4896296296296297
Converged (lack of improvement in inertia) at step 18/100
Saving model...
Training completed.
```

To launch the training process as a REST API, use the `--api` argument.

This should show feedback with connection details, like so:
```
$ python3 main.py -c config/configuration.json --api
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

The output of the API contains the structure:

```
{
  status: 200,
  response: {
    result: {dictionary with the training_id list},
    message: "A message that inform about the result of the executed model",
    score: inference_score,
    inference_time: time_required_for_the_inference
  }
}
```

The status in the response can assume the values:
* 200 : model executed corectly;
* 406 : the input keys do not exist in the model configuration;
* 406 : the model specified in the request does not exist;
* 406 : the model is not specified in the body of the request;

## Notes

DISCLAIMER: This project has been funded with support from the European Commission.
This publication [communication] reflects the views only of the author, and the Commission cannot be held responsible for any use which may be made of the information contained therein.
