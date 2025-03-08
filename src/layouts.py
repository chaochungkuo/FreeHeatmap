from dash import dcc, html
import dash_bootstrap_components as dbc
import base64
import dash_daq as daq
from utils import b64_image



def create_layout(app_title):
    return dbc.Container([
        create_banner(app_title=app_title),
        dbc.Row([
            dbc.Col([
                html.H1("FreeHeatmap"),
                html.Div("Upload your CSV file and configure the heatmap."),
                html.Br(),
                # Input Data
                html.H3("Input Data"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select a CSV File')
                    ]),
                    style={
                        'width': '95%',
                        'height': '50px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
                ),
                html.Div(id='file-info'),  # Div to display file name and row count
                # Filter rows
                html.H4("Filter rows:"),
                dcc.Dropdown(
                    id='filter-column',
                    placeholder='Select column for filtering rows',
                    style={'width': '100%'}
                ),
                html.Div("Enter row names (one per line)"),
                dcc.Textarea(
                    id='selected-rows',
                    placeholder='Enter row names (one per line)',
                    style={'width': '100%', 'height': '150px'}
                ),
                html.Div(id='filtered-rows-count'),  # Div to display the number of filtered rows
                html.Div("Row order:"),
                dcc.Dropdown(id='row-order', 
                             options=[{'label': 'Input Order', 'value': 'input'},
                                      {'label': 'Cluster', 'value': 'cluster'}],
                             value='input'),
                # Filter columns
                html.H4("Filter columns:"),
                html.Div("Enter column names (one per line)"),
                dcc.Textarea(
                    id='selected-columns',
                    placeholder='Enter column names (one per line)',
                    style={'width': '100%', 'height': '150px'}
                ),
                html.Div(id='filtered-columns-count'),  # Div to display the number of filtered columns
                html.Div("Column order:"),
                dcc.Dropdown(id='col-order',
                             options=[{'label': 'Input Order', 'value': 'input'},
                                      {'label': 'Cluster', 'value': 'cluster'}],
                             value='input'),
                # Transformation
                html.H4("Transformation:"),
                dcc.Checklist(id='log-transform',
                              options=[{'label': 'Log10 Transform', 'value': 'log'}],
                              inline=False),
                # Figure Theme
                html.H4("Figure Theme"),
                html.Div("Main title:"),
                dcc.Input(id='main-title', type='text',
                          style={'width': '100%'},
                          placeholder='Title', value=""),
                html.Div("Figure width:"),
                dcc.Input(id='fig-width', type='number',
                          style={'width': '100%'},
                          placeholder='Width', value=10),
                html.Div("Figure height:"),
                dcc.Input(id='fig-height', type='number',
                          style={'width': '100%'},
                          placeholder='Height', value=10),
                html.Div("Cell width: (default is None)"),
                dcc.Input(id='cell-width', type='number',
                          style={'width': '100%'},
                          placeholder='Cell width', value=None),
                html.Div("Cell height: (default is None)"),
                dcc.Input(id='cell-height', type='number',
                          style={'width': '100%'},
                          placeholder='Cell height', value=None),
                html.Div("Color map:"),
                dcc.Dropdown(id='color-map',
                             style={'width': '100%'},
                             options=[{'label': 'Viridis', 'value': 'viridis'},
                                      {'label': 'Plasma', 'value': 'plasma'},
                                      {'label': 'Inferno', 'value': 'inferno'},
                                      {'label': 'Magma', 'value': 'magma'},
                                      {'label': 'Cividis', 'value': 'cividis'}],
                             value='viridis'),
            ], width=3),

            dbc.Col([
                # Heatmap Section
                html.H3("Heatmap"),
                html.Img(id='heatmap', src='', 
                         alt='Heatmap will be displayed here.',
                         style={'width': '100%', 'height': 'auto'})
            ], width=5),
            
            dbc.Col([
                # Heatmap Section
                html.H3("Clustering on rows"),
                dcc.Checklist(id='cluster-rows',
                              options=[{'label': 'Cluster rows', 'value': "cluster-rows"},
                                       {'label': 'Show cluster trees on rows', 'value': "showtree-rows"}],
                              inline=False, value=["cluster-rows", "showtree-rows"]),
                
                html.H3("Clustering on columns"),
                dcc.Checklist(id='cluster-columns',
                              options=[{'label': 'Cluster columns', 'value': "cluster-columns"},
                                       {'label': 'Show cluster trees on columns', 'value': "showtree-columns"},],
                              inline=False, value=["cluster-columns", "showtree-columns"]),
                html.H3("Labels"),
                dcc.Checklist(id='show-labels',
                              options=[{'label': 'Show row labels', 'value': "show-row-labels"},
                                       {'label': 'Set row labels on the left', 'value': "left-row-labels"},
                                       {'label': 'Show column labels', 'value': "show-column-labels"}],
                              inline=False, value=["show-row-labels", "show-column-labels"]),
                html.Div("Rotate the column labels:"),
                dcc.Input(id='rotate-column-labels', type='number',
                          style={'width': '100%'},
                          placeholder='Degree of rotation', value=0),
                html.Div("Row label font size:"),
                dcc.Input(id='row-label-size', type='number',
                          style={'width': '100%'},
                          placeholder='Width', value=5),
                html.Div("Column label font size:"),
                dcc.Input(id='column-label-size', type='number',
                          style={'width': '100%'},
                          placeholder='Width', value=5),
            ], width=3)
        ])
    ])


def create_banner(app_title):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=b64_image('./assets/plotly_logo.png'),
                                     style={'height': '40px'}), width=10),
                    dbc.Col(html.A(
                        id='gh-link',
                        children=[
                            'View on GitHub'
                        ],
                        href="https://github.com/chaochungkuo/FreeHeatmap",
                        style={'color': 'black'}
                    ))
                ], justify="start")
        ],
        style={'padding': '0.5em'},
    )


