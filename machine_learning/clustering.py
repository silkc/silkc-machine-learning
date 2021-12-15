from sklearn.cluster import KMeans, MiniBatchKMeans

import pandas as pd

def training_kmeans(config, dataframe: pd.DataFrame):
    """

    :param config:
    :param dataframe:
    :return:
    """

    if config['model']['minibatch']:
        km = MiniBatchKMeans(n_clusters=config['model']['n_clusters'],
                             init="k-means++",
                             n_init=1,
                             init_size=1000,
                             batch_size=1000,
                             verbose=config['model']['verbose'])
    else:
        km = KMeans(n_clusters=config['model']['n_clusters'],
                    init="k-means++",
                    max_iter=config['model']['max_iter'],
                    n_init=1,
                    verbose=config['model']['verbose'])

    km.fit(dataframe)

    return km

def test_kmeans(confg, dataframe:pd.DataFrame):
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