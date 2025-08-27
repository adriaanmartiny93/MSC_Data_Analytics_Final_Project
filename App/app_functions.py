import pandas as pd
import plotly.express as px

def plot_scatter(dataset,x_col,y_col,value_col,color_col,name_col,title=None):
    """
    Create a scatter plot with Plotly Express.
    """

    x2 = x_col.replace("_", " ").replace("90", " (per 90)").title()
    y2 = y_col.replace("_", " ").replace("90", " (per 90)").title()

    fig_scatter = px.scatter(
        dataset,
        x=x_col,
        y=y_col,
        labels={
            x_col: x2,
            y_col: y2
        },
        color=color_col,
        hover_name=name_col,
        size=value_col,
        title=title if title else f"{x2} vs {y2}",
        width=800,
        height=800
    )

    return fig_scatter



