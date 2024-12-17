from db import Database
from queries import Queries
from plots import Plots
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import dotenv_values

db = Database()
queries = Queries()
plot = Plots()

test = dotenv_values('.testing.env')

data = pd.read_sql(queries.get_retail_sales(
    brands=test['BRAND'],
    loc_brands=test['LOC_BRANDS'],
    years=test['YEAR'],
    intra_mode=test['INTRA_MODE'],
    intras_loc=test['INTRAS_LOC']
), db.sos_conn())

plot.bar_sales_by_month(test['BRAND'], test['YEAR'], data)