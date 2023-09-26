import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Generate some example data for demonstration (replace this with your own DataFrame)
df = pd.DataFrame({
    'Column_{}'.format(i): range(100) for i in range(218)
})

# Initialize the Dash app
app = dash.Dash(__name__)

# The column options for the dropdown
column_options = [{'label': col, 'value': col} for col in df.columns]

# Default columns to display
default_columns = df.columns[:10].tolist()

app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=column_options,
        value=default_columns,  # Default columns to display
        multi=True
    ),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': i, 'id': i} for i in default_columns],
        data=df.to_dict('records'),
    )
])

@app.callback(
    Output('data-table', 'columns'),
    [Input('column-dropdown', 'value')]
)
def update_columns(selected_columns):
    return [{'name': i, 'id': i} for i in selected_columns]

if __name__ == '__main__':
    app.run_server(debug=True)
