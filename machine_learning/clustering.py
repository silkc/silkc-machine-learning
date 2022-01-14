import random

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
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
                             init_size=config['model']['init_size'],
                             batch_size=config['model']['batch_size'],
                             verbose=config['model']['verbose'])
    else:
        km = KMeans(n_clusters=config['model']['n_clusters'],
                    init="k-means++",
                    max_iter=config['model']['max_iter'],
                    n_init=1,
                    verbose=config['model']['verbose'],
                    algorithm="full")

    km.fit(data)

    return km

def test_kmeans(confg, model, data, labels):
    """

    :param confg:
    :param dataframe:
    :return:
    """

    from data.preprocessing.text_features_extraction import load_vectorized
    # with label
    homogeneity_score = metrics.homogeneity_score(labels, model.labels_)
    completeness_score = metrics.completeness_score(labels, model.labels_)
    v_measure = metrics.v_measure_score(labels, model.labels_)
    adjusted_rand_index = metrics.adjusted_rand_score(labels, model.labels_)
    # no label
    silhouette_coefficient = metrics.silhouette_score(data, model.labels_, sample_size=config['model']['test_sample_size'])
    davies_bouldin = metrics.davies_bouldin_score(data.toarray(), model.labels_)


    return homogeneity_score, completeness_score, v_measure, adjusted_rand_index, silhouette_coefficient, davies_bouldin

def save_model(config, model):
    """

    :param config:
    :param model:
    :return:
    """
    import os
    save_path = os.path.join(config['api_configuration']['model_path'].split(os.sep)[0], config['api_configuration']['model_path'].split(os.sep)[1])
    os.makedirs(save_path, exist_ok=True)
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

    # load model
    model = load_model(config)
    # predict
    predict = model.predict(input)

    return predict

if __name__ == "__main__":
    from data.preprocessing.text_features_extraction import extract_features_from_text
    import pandas as pd
    config = {
        "model": {
            "init_size": 100,
            "batch_size": 10,
            "verbose": True,
            "n_clusters": 4,
            "max_iter": 10,
            "minibatch": True,
            "test_sample_size": 100
        },
        "api_configuration": {
            "model_path": "saved_data/model/cluster.sav",
            "extractor_path": "saved_data/vectorizer/vectorizer.sav"
        },
        "features": {
            "n_features": 500,
            "reduce": False,
            "reduced_n_features": 100,

        }
    }
    dataframe = pd.read_csv("data/export/Agglomeration3.csv")
    column_list = dataframe.columns.to_list()
    features = extract_features_from_text(config, dataframe, ['occupation_preferred_label', 'occupation_description',
                                                              'isco_preferred_label', 'isco_group_description',
                                                              'occupation_skill_skill_type'], "english", True,
                                          "hashing")
    km = training_kmeans(config, features)
    save_model(config, km)
    model = load_model(config)

    print(test_kmeans(config, model, features, [random.randint(0, config['model']['n_clusters'] - 1) for i in range(0, 5)]))

    print(model)

    input_data = dataframe.loc[975]

    input_features = extract_features_from_text(config, input_data, ['occupation_preferred_label', 'occupation_description',
                                                              'isco_preferred_label', 'isco_group_description',
                                                              'occupation_skill_skill_type'], "english", True,
                                          "hashing")

    prediction = infer_kmeans(config, input_features)

    print(prediction)