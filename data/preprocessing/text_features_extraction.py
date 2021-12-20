from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from typing import Union

import pandas as pd
import numpy as np


def extract_features_from_text(config, dataframe: pd.DataFrame, columns: list, stop_words: Union[str, list], normalize: bool, modality: str, alternate_sign: bool = False) -> pd.DataFrame:
    """

    :param config:
    :param dataframe:
    :param columns:
    :param stop_words:
    :param normalize:
    :param modality:
    :param alternate_sign:
    :return:
    """
    if modality.lower() not in ['hashing', 'vectorize']:
        raise NotImplemented("You have to choose between hashing or vectorize modality")
    extractor = None
    if modality.lower() == 'hashing':
        if normalize:
            hasher = HashingVectorizer(
                n_features=config['features']['n_features'],
                stop_words=stop_words,
                alternate_sign=alternate_sign,
                norm=None
            )
            extractor = make_pipeline(hasher, TfidfTransformer())
        else:
            extractor = HashingVectorizer(
                n_features=config['features']['n_features'],
                stop_words=stop_words,
                alternate_sign=alternate_sign,
                norm="l2"
            )
    else:
        extractor = TfidfVectorizer(
            max_df=0.7,
            max_features=config['features']['n_features'],
            min_df=2,
            stop_words=stop_words,
            use_idf=normalize
        )

    feature_extracted = extractor.fit_transform(dataframe[columns])

    return feature_extracted

def reduce_features(config, data) -> pd.DataFrame:
    """

    :param config:
    :param dataframe:
    :param columns:
    :return:
    """
    svd = TruncatedSVD(config['features']['reduced_n_features'])
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    feature_extracted = lsa.fit_transform(data)

    return feature_extracted

if __name__ == "__main__":
    config = {
        "features" : {
            "n_features": 250,
            "reduced_n_features": 100
        }
    }

    dataframe = pd.read_csv("../export/Agglomeration3.csv")
    column_list = dataframe.columns.to_list()
    features = extract_features_from_text(config, dataframe, ['occupation_preferred_label', 'occupation_description', 'isco_preferred_label', 'isco_group_description', 'occupation_skill_skill_type'], "english", True, "hashing")
    features2 = reduce_features(config, features)