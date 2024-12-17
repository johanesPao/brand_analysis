import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd

class Plots:
    def __init__(self):
        pass

    def bar_sales_by_month(self, brand = str, year = int, data = pd.DataFrame):
        # Data Transformation
        data = data[['month','cost','retail_tag','customer_paid']].groupby(['month'], as_index=False).sum()
        data.rename(columns={"month":"Month", "cost": "COGS", "retail_tag": "Sales at Tag Price", "customer_paid": "Customer Paid"}, inplace=True)
        sns_data = data.melt(id_vars=['Month'], var_name="Metrics", value_name="Amount (in Billion Rupiah)")

        # Plot properties
        sns.set_theme(palette="Paired")
        fig, ax = plt.subplots()
        fig.set_size_inches(15,5)

        # Plotting
        barplot = sns.barplot(sns_data, x="Month", y="Amount (in Billion Rupiah)", hue="Metrics", ax=ax)

        # Title
        ax.set_title(f"{brand} Sales Metrics in {year}")

        # Remove legend title
        handles, labels = barplot.get_legend_handles_labels()
        barplot.legend(handles=handles[0:], labels=labels[0:])

        # Remove scientific notation in yaxis
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.2f}B'.format(x/10**9)))

        plt.show()