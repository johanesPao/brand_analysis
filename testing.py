from db import Database
from queries import Queries
from plots import Plots
import pandas as pd

db = Database()
queries = Queries()
plot = Plots()
data = pd.read_sql(queries.get_retail_sales(
    brands="ZAXY",
    loc_brands=['ZAXY','ALL'],
    years=2024,
    intra_mode="NIC",
    intras_loc=['BAZZAR']
), db.sos_conn())

plot.bar_chart(data['month'], data['customer_paid'])

