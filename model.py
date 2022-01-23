import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sqlalchemy import create_engine

from zones.config import config

tables_query = "SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'data%';"

postgres_access = "postgresql://{}:{}/{}".format(
    config["POSTGRES"]["Host"], config["POSTGRES"]["Port"], config["TRUST"]["TrustedDBName"]
)
engine = create_engine(postgres_access)
tables = engine.execute(tables_query).fetchall()

dfs = []
for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, con=engine)
    df.drop("index", axis=1, inplace=True)
    dfs.append(df)

df = pd.concat(dfs)


df = pd.read_csv ('data/Population-EstimatesData-1.csv')


pd.set_option('display.float_format', lambda x: '%.6f' % x)



N = 20
# Get Last N columns of dataframe
df = df.iloc[: , -N:-1]
df = df[df['2050'] < 100000]


X = df.iloc[: , -N:-2]
X = X.dropna()
y = df.iloc[: , -2:-1]
y = y.dropna()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
LR = LinearRegression()
# fitting the training data
LR.fit(x_train,y_train)
y_prediction =  LR.predict(x_test)
y_prediction


# importing r2_score module
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
# predicting the accuracy score
score=r2_score(y_test,y_prediction)
print('r2 socre is ',score)
print('mean_sqrd_error is==',mean_squared_error(y_test,y_prediction))
print('root_mean_squared error of is==',np.sqrt(mean_squared_error(y_test,y_prediction)))


