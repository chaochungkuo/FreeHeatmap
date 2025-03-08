from dash import Input, Output, State
import pandas as pd
import plotly.express as px
from utils import parse_data, b64_image, generate_heatmap
import base64
import numpy as np
import io
from dash import html


def register_callbacks(app):
    @app.callback(
        Output('filter-column', 'options'),
        Input('upload-data', 'contents'),
        prevent_initial_call=True
    )
    def update_filter_column_options(contents):
        df = parse_data(contents)
        options = [{'label': col, 'value': col} for col in df.columns]
        return options

    @app.callback(
        [Output('filtered-rows-count', 'children'), Output('filtered-columns-count', 'children')],
        [Input('filter-column', 'value'), Input('selected-rows', 'value'), Input('selected-columns', 'value')],
        [State('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_filtered_counts(filter_column, selected_rows, selected_columns, file_content):
        df = parse_data(file_content)
        if filter_column:
            df = df[df[filter_column].notna()]
        if selected_rows:
            selected_rows = selected_rows.split('\n')
            df = df[df[filter_column].isin(selected_rows)]
        if selected_columns:
            selected_columns = selected_columns.split('\n')
            df = df.loc[:, selected_columns]
        
        filtered_rows_count = f"Filtered rows: {len(df)}"
        filtered_columns_count = f"Filtered columns: {len(df.columns)}"
        return filtered_rows_count, filtered_columns_count

    @app.callback(
        Output('heatmap', 'src'),
        [Input('filter-column', 'value'), Input('selected-rows', 'value'), Input('selected-columns', 'value'),
         Input('row-order', 'value'), Input('col-order', 'value'),
         Input('log-transform', 'value'), Input('fig-width', 'value'),
         Input('fig-height', 'value'), Input('cell-width', 'value'),
         Input('cell-height', 'value'), Input('color-map', 'value'),
         Input('cluster-rows', 'value'), Input('cluster-columns', 'value'),
         Input('show-labels', 'value'), Input('rotate-column-labels', 'value'),
         Input('row-label-size', 'value'), Input('column-label-size', 'value')],
        [State('upload-data', 'contents')],
        prevent_initial_call=True
    )
    def update_heatmap(filter_column, selected_rows, selected_columns, row_order, col_order, log_transform, fig_width, fig_height, cell_width, cell_height, color_map, cluster_rows, cluster_columns, show_labels, rotate_column_labels, row_label_size, column_label_size, file_content):
        df = parse_data(file_content)
        if filter_column:
            df = df[df[filter_column].notna()]
        if selected_rows:
            selected_rows = selected_rows.split('\n')
            df = df[df[filter_column].isin(selected_rows)]
        if selected_columns:
            selected_columns = selected_columns.split('\n')
            df = df.loc[:, selected_columns]
        
        if df.empty or not all(np.issubdtype(dtype, np.number) for dtype in df.dtypes):
            return ''
        else:
        
            heatmap_img = generate_heatmap(df, selected_rows, selected_columns, row_order, col_order, log_transform, fig_width, fig_height, cell_width, cell_height, color_map, cluster_rows, cluster_columns, show_labels, rotate_column_labels, row_label_size, column_label_size)
            return heatmap_img

    # Callback to process the uploaded file and display its info
    @app.callback(
        Output('file-info', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def update_file_info(contents, filename):
        if contents is None:
            return ""
        
        # Decode the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Check file type and load data
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(io.BytesIO(decoded), sheet_name=0)
            else:
                return "Unsupported file format"
            
            # Get the number of rows and columns
            row_count = len(df)
            col_count = len(df.columns)
            
            # Display the filename, row count, and column count
            return [f"File: {filename}", html.Br(), f"Rows: {row_count}", html.Br(), f"Columns: {col_count}"]
        except Exception as e:
            return f"Error processing file: {str(e)}"
