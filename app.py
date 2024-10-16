import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the gene expression dataset
data = pd.read_csv('data/gene_expression.csv')

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout using Bootstrap
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Gene Expression Data Visualization", style={'text-align': 'center'}), width=12)
    ], justify='center'),
    
    dbc.Row([
        dbc.Col(html.P("A simple dashboard for visualizing biological data.", style={'text-align': 'center'}), width=12)
    ], justify='center'),

    dbc.Row([
        # Dropdown for selecting multiple genes
        dbc.Col([
            html.Label("Select Genes:"),
            dcc.Dropdown(
                id='gene-dropdown',
                options=[{'label': gene, 'value': gene} for gene in data['Gene'].unique()],
                value=[data['Gene'].unique()[0]],  # Default selected gene
                multi=True  # Enable multi-select
            )
        ], width=6),

        # Dropdown for selecting multiple conditions
        dbc.Col([
            html.Label("Select Conditions:"),
            dcc.Dropdown(
                id='condition-dropdown',
                options=[{'label': condition, 'value': condition} for condition in data.columns[1:]],  # Conditions start from the second column
                value=[data.columns[1]],  # Default selected condition
                multi=True  # Enable multi-select
            )
        ], width=6)
    ], className='mt-3'),  # Add margin-top for better spacing

    dbc.Row([
        # Radio buttons for selecting graph type
        dbc.Col([
            html.Label("Select Graph Type:"),
            dcc.RadioItems(
                id='graph-type',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Heatmap', 'value': 'heatmap'}
                ],
                value='bar',  # Default graph type
                labelStyle={'display': 'inline-block'}
            )
        ], width=12)
    ], className='mt-3'),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='gene-graph'),  # Graph component
            width=12
        )
    ], className='mt-4')
], fluid=True)

# Define callback to update graph based on user input
@app.callback(
    Output('gene-graph', 'figure'),
    [Input('gene-dropdown', 'value'),
     Input('condition-dropdown', 'value'),
     Input('graph-type', 'value')]
)
def update_graph(selected_genes, selected_conditions, selected_graph_type):
    # Ensure we handle multi-selection for both genes and conditions
    filtered_data = data[data['Gene'].isin(selected_genes)]

    if selected_graph_type == 'bar':
        # Bar chart for gene expression across multiple conditions
        fig = px.bar(
            data_frame=filtered_data.melt(id_vars='Gene', value_vars=selected_conditions, var_name='Condition', value_name='Expression'),
            x='Gene',
            y='Expression',
            color='Condition',
            title=f"Expression of Selected Genes under Selected Conditions"
        )

    elif selected_graph_type == 'scatter':
        # Scatter plot for gene expression
        fig = px.scatter(
            data_frame=filtered_data.melt(id_vars='Gene', value_vars=selected_conditions, var_name='Condition', value_name='Expression'),
            x='Gene',
            y='Expression',
            color='Condition',
            title=f"Scatter Plot of Selected Genes under Selected Conditions"
        )

    elif selected_graph_type == 'heatmap':
        # Heatmap for gene expression across multiple conditions
        heatmap_data = filtered_data.set_index('Gene')[selected_conditions]
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Conditions", y="Genes", color="Expression Level"),
            x=selected_conditions,  # Conditions on x-axis
            y=filtered_data['Gene'],  # Genes on y-axis
            title="Heatmap of Gene Expression Levels"
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
