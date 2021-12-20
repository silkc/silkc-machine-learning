from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.externals import joblib
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

    return None

def load_model(config):

    return None

def infer_kmeans(model, input):
    return None