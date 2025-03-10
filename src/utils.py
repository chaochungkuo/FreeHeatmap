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
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker

      
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

def generate_heatmap(df, selected_rows, selected_cols, row_order, col_order, log_transform, fig_width, fig_height, color_map, cluster_rows, cluster_columns, show_labels, rotate_column_labels, row_label_size, column_label_size, main_title, showtree_rows, showtree_columns):
    if log_transform:
        df = df.map(lambda x: np.log10(x+1))
    
    row_cluster = 'cluster-rows' in cluster_rows
    col_cluster = 'cluster-columns' in cluster_columns
    show_row_labels = 'show-row-labels' in show_labels
    show_col_labels = 'show-column-labels' in show_labels
    left_row_labels = 'left-row-labels' in show_labels
    if row_order == 'input':
        row_cluster = False
    if col_order == 'input':
        col_cluster = False

    g = sns.clustermap(df, cmap=color_map, linewidths=0.1,
                       linecolor=None, cbar=True,
                       xticklabels=show_col_labels, 
                       yticklabels=show_row_labels, 
                       row_cluster=row_cluster, 
                       col_cluster=col_cluster, 
                       figsize=(fig_width, fig_height),
                       tree_kws={'linewidths': 0.5} if showtree_rows or showtree_columns else {'linewidths': 0})
    
    if not showtree_rows:
        g.ax_row_dendrogram.set_visible(False)
    if not showtree_columns:
        g.ax_col_dendrogram.set_visible(False)
    
    if rotate_column_labels:
        plt.setp(g.ax_heatmap.get_xticklabels(), rotation=rotate_column_labels)
    
    if row_label_size:
        plt.setp(g.ax_heatmap.get_yticklabels(), fontsize=row_label_size)
    
    if column_label_size:
        plt.setp(g.ax_heatmap.get_xticklabels(), fontsize=column_label_size)
    
    if left_row_labels:
        g.ax_heatmap.yaxis.set_label_position("left")
        g.ax_heatmap.yaxis.tick_left()
    
    g.ax_heatmap.set_ylabel('')  # Remove y-axis label
    plt.tight_layout(rect=[0, 0.1, 0.65, 1])
    if main_title:
        g.fig.subplots_adjust(top=0.9, right=0.65)
        g.fig.suptitle(main_title, fontsize=16)
    else:
        g.fig.subplots_adjust(right=0.65)
    
    # Now position the color bar in that extra space
    g.ax_cbar.set_position((0.85, 0.25, 0.03, 0.50))
    g.ax_cbar.locator = ticker.MaxNLocator(nbins=5)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode the bytes from the buffer directly
    image_bytes = buffer.getvalue()
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    img_str = f"data:image/png;base64,{encoded}"
    
    # Save as PDF
    pdf_path = './assets/heatmap.pdf'
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(g.fig, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    return img_str
