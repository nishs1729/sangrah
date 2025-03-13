import matplotlib.pyplot as plt
import pandas as pd

def change_plot(df, key=0, order=None, color='black', lc='gray', lw=1, axis=None):
    """
    Plots changes in a dataframe with lines connecting points.

    Args:
        df (pd.DataFrame): DataFrame containing the data to plot.
        key (int or str, optional): Column to use as the reference point for connecting lines. Defaults to 0.
        order (list, optional): Order of columns to plot. Defaults to None.
        axis (matplotlib.axes._axes.Axes, optional): Axis to plot on. Defaults to None.
        color (str or list, optional): Color of the points. Defaults to black.
        lc (str, optional): Line color. Defaults to gray.
        lw (float, optional): Line width. Defaults to 1.

    Raises:
        ValueError: If length of color list does not match number of columns in dataframe.
        ValueError: If key is not a valid column index or name.

    Returns:
        None
    """
    # Create a new axis if none is provided
    if not axis:
        _, axis = plt.subplots(figsize=(3, 5))

    # Set default line color if none is provided
    if lc is None:
        lc = 'gray'

    # Reorder dataframe columns if order is provided
    if order:
        df = df[order]

    ncols = len(df.columns)

    # Handle point color
    if color is None:
        color = ['black'] * ncols
    elif isinstance(color, str):
        color = [color] * ncols
    elif isinstance(color, list):
        if len(color) != ncols:
            raise ValueError("Length of color list must match number of columns in dataframe")

    # Handle key
    if isinstance(key, int):
        if key >= ncols:
            raise ValueError("Key must be less than number of columns in dataframe")
    elif isinstance(key, str):
        if key not in df.columns:
            raise ValueError("Key must be a column in the dataframe")
        key = df.columns.get_loc(key)

    # Plotting points
    for i, col in enumerate(df.columns):
        axis.scatter([i] * len(df), df[col], label=col, color=color[i], zorder=10)
        axis.set_xticks(range(len(df.columns)))
        axis.set_xticklabels(df.columns, rotation=90)

    # Plotting lines
    other_cols = list(range(ncols))
    other_cols.remove(key)

    for i in range(len(df)):
        for j in other_cols:
            axis.plot([key, j], [df.iloc[i, key], df.iloc[i, j]], color=lc, linewidth=lw)

    # Hide top and right spines
    axis.spines[['top', 'right']].set_visible(False)
    plt.show()