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
                norm=normalize
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

    feature_dataframe = pd.DataFrame()

    for column in columns:
        data_list = dataframe[column].to_list()
        feature_extracted = extractor.fit_transform(data_list)
        f_d = pd.DataFrame(columns=[column])
        f_d[column] = np.array(feature_extracted)
        feature_dataframe = pd.concat(feature_dataframe, f_d)

    return feature_dataframe

def reduce_features(config, dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
    """

    :param config:
    :param dataframe:
    :param columns:
    :return:
    """
    svd = TruncatedSVD(config['features']['reduced_n_features'])
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    feature_dataframe = pd.DataFrame()

    for column in columns:
        data_list = dataframe[column].to_list()
        feature_extracted = lsa.fit_transform(data_list)
        f_d = pd.DataFrame(columns=[column])
        f_d[column] = np.array(feature_extracted)
        feature_dataframe = pd.concat(feature_dataframe, f_d)

    return feature_dataframe