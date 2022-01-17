from io import StringIO
import pandas as pd
import re
from zones.config import config
from zones.utils import persistent_mongodb_collection


class Formatter:
    def __init__(self):
        pass

    @staticmethod
    def load(use_config=config):
        # Get persistent storage collection.
        collection = persistent_mongodb_collection(use_config=use_config)
        # Query the collection for every document with an origin that matches the file name.
        # Escapes must be done with \\ instead of \.
        query = re.compile(r"^.*Population-EstimatesData-[\d]+\.csv$")
        # Converting to list may be inefficient, but the alternative is querying again with count_documents().
        documents = list(collection.find({"metadata.origin": query}))
        # Create an empty list with length equal to the number of retrieved documents.
        dataframes = [0] * len(documents)
        # Sort documents by looking at the origin number, and insert the data to dataframes as a dataframe.
        for document in documents:
            print(document["metadata"]["origin"])
            index = int(re.findall(r"[\d]+", document["metadata"]["origin"])[-1])
            data = pd.read_csv(StringIO(document["data"]))
            dataframes[index - 1] = data

        # Concatenate dataframes into a single one.
        single_df = pd.concat(dataframes)
        return single_df
