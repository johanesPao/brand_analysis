import matplotlib.pyplot as plt

class Plots:
    def __init__(self):
        pass

    def bar_chart(self, x: list, y: list):
        fig, ax = plt.subplots()

        ax.bar(x,y)
        plt.show()