import numpy as np
import matplotlib.pyplot as plt


# code extracted from https://stackoverflow.com/questions/19726663
def create_table(data, col_width=3.0, row_height=0.625, font_size=14,
                 header_color='#40466e', row_colors=None, edge_color='w',
                 bbox=None, header_columns=0,
                 ax=None, **kwargs):

    if row_colors is None:
        row_colors = ['#f1f1f2', 'w']

    if bbox is None:
        bbox = [0, 0, 1, 1]

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)

        ax.axis('off')

    table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    table.auto_set_font_size(False)
    table.set_fontsize(font_size)

    for k, cell in table.get_celld().items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    return ax


# function to create histogram
def create_histogram(x, y, clazz, x_label=None, y_label=None, font='medium', **kwargs):
    fig, ax = plt.subplots(figsize=(11, 7))

    group = ax.bar(x, y, **kwargs)

    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=font)

    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=font)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['bottom'].set_linewidth(2.5)

    ax.set_xticks(x)
    ax.set_xticklabels([clazz[index][1] for index in range(len(clazz))])

    for element in group:
        if element.get_height() > 0:
            height = element.get_height()
            position = (element.get_x() + element.get_width() / 2, height)

            ax.annotate(str(height), position, xytext=(0, 4), textcoords='offset points', ha='center')

    return ax
