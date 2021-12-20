from sklearn.cluster import KMeans, MiniBatchKMeans

import pickle

def training_kmeans(config, data):
    """

    :param config:
    :param dataframe:
    :return:
    """

    if config['model']['minibatch']:
        km = MiniBatchKMeans(n_clusters=config['model']['n_clusters'],
                             init="k-means++",
                             n_init=1,
                             init_size=config['machine_learning_configuration']['init_size'],
                             batch_size=config['machine_learning_configuration']['batch_size'],
                             verbose=config['model']['verbose'])
    else:
        km = KMeans(n_clusters=config['model']['n_clusters'],
                    init="k-means++",
                    max_iter=config['model']['max_iter'],
                    n_init=1,
                    verbose=config['model']['verbose'])

    km.fit(data)

    return km

def test_kmeans(confg, data):
    """

    :param confg:
    :param dataframe:
    :return:
    """
    return None

def save_model(config, model):
    """

    :param config:
    :param model:
    :return:
    """
    pickle.dump(model, open(config['api_configuration']['model_path'], 'wb'))
    return None

def load_model(config):
    """

    :param config:
    :return:
    """

    model = pickle.load(open(config['api_configuration']['model_path'], 'rb'))

    return model

def infer_kmeans(config, input):
    """

    :param config:
    :param input:
    :return:
    """

    model = load_model(config)

    # Model inference

    return None

if __name__ == "__main__":
    config = {
        "machine_learning_configuration": {
            "init_size": 1000,
            "batch_size": 10,
            "verbose": True,
            "n_clusters": 25,
            "max_iter": 10
        },
        "api_configuration": {
            "model_path": ""
        }
    }
    