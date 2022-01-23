from datetime import datetime
import numpy as np
import pandas_profiling
import scipy

from zones.config import config


def remove_outliers(df):
    max_deviation = int(config['TRUST']['MaxDeviation'])
    df[(np.abs(scipy.stats.zscore(df)) < max_deviation).all(axis=1)]


def remove_duplicates(df):
    df.drop_duplicates(keep='last')


def profile_data(df):
    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile=f"{config['TRUST']['ProfilingFile']}-{datetime.now()}")


data_quality_processes = [
    remove_duplicates, remove_outliers, profile_data
]
