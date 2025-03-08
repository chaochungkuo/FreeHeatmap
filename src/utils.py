import pandas as pd
import plotly.express as px
from io import StringIO
import base64
import math
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO

      
def parse_data(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode('utf-8')))  # Modify if Excel
    return df

# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def generate_heatmap(df, selected_rows, selected_cols, row_order, col_order, log_transform, fig_width, fig_height, cell_width, cell_height, color_map, cluster_rows, cluster_columns, show_labels, rotate_column_labels, row_label_size, column_label_size):
    if log_transform:
        df = df.map(lambda x: np.log10(x) if x > 0 else 0)
    
    if selected_rows:
        df = df.loc[selected_rows]
    if selected_cols:
        df = df[selected_cols]
    
    row_cluster = 'cluster-rows' in cluster_rows
    col_cluster = 'cluster-columns' in cluster_columns
    show_row_labels = 'show-row-labels' in show_labels
    show_col_labels = 'show-column-labels' in show_labels
    left_row_labels = 'left-row-labels' in show_labels

    plt.figure(figsize=(fig_width, fig_height))
    sns.clustermap(df, cmap=color_map, linewidths=0.5, linecolor='gray', cbar=True, xticklabels=show_col_labels, yticklabels=show_row_labels, row_cluster=row_cluster, col_cluster=col_cluster, figsize=(fig_width, fig_height))
    
    if rotate_column_labels:
        plt.setp(plt.gca().get_xticklabels(), rotation=rotate_column_labels)
    
    if row_label_size:
        plt.setp(plt.gca().get_yticklabels(), fontsize=row_label_size)
    
    if column_label_size:
        plt.setp(plt.gca().get_xticklabels(), fontsize=column_label_size)
    
    if left_row_labels:
        plt.gca().yaxis.set_label_position("left")
        plt.gca().yaxis.tick_left()
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"
