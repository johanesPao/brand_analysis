import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from funcs import convert_int_to_month_name

class Plots:
    def __init__(self):
        pass

    def bar_sales_by_month(self, brand = str, year = int, data = pd.DataFrame):
        # Data selection and grouping by month
        data = data[
            [
                'month',
                'cost',
                'retail_tag',
                'customer_paid'
            ]
        ].groupby(['month'], as_index=False).sum()
        data["month"] = data['month'].apply(lambda x: convert_int_to_month_name(x))

        # Rename columns for display
        data.rename(columns={
            "month":"Month", 
            "cost": "COGS", 
            "retail_tag": "Sales at Tag Price", 
            "customer_paid": "Customer Paid"
        }, inplace=True)

        # Plot line for COGS, Tag Price and Customer Paid
        fig = px.line(
            data, 
            x="Month", 
            y=["COGS", "Sales at Tag Price", "Customer Paid"], 
            color_discrete_sequence=['#FF2E63','#252A34','#00ADB5'], 
            title=f"{brand} Sales Metrics in {year}", 
            line_shape="spline"
        )

        # Update traces in figures
        fig.update_traces(
            mode="markers+lines", 
            hovertemplate='Rp %{y:,.0f}<extra></extra>'
        )
        fig.update_yaxes(title_text="Amount")
        fig.update_layout(
            legend_title_text="Metrics", 
            hovermode="x", 
            autosize=True
        )

        # Show line plot
        fig.show()