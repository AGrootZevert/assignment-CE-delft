import plotly.graph_objects as go
from pandera.typing import DataFrame

from src.data_structures.data_structures import HeatData


def visualize_with_average(
    hourly_data: DataFrame[HeatData],
    x_column: str,
    y_column: str,
    x_label: str,
    y_label: str,
    title: str,
) -> go.Figure:
    """Plot the y column vs the x column and add the average trace


    Args:
        hourly_data (DataFrame[HeatData]): The hourly data
        x_column (str): the x column to plot
        y_column (str): the y column to plot
        x_label (str): the label of the x axis
        y_label (str): the label of the y axis
        title (str): the plot title

    Returns:
        go.Figure: The figure
    """
    # Calculate average heat request per hour across all days
    hourly_avg = hourly_data[y_column].mean()

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces for each day

    fig.add_trace(
        go.Scatter(
            x=hourly_data[x_column],
            y=hourly_data[y_column],
            mode="lines",
            name=y_label,
            opacity=0.3,
        )
    )

    # Add average line
    fig.add_trace(
        go.Scatter(
            x=hourly_data[x_column],
            y=[hourly_avg] * len(hourly_data),
            mode="lines",
            name="Average",
            line={"color": "red", "width": 3},
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x unified",
    )
    return fig
