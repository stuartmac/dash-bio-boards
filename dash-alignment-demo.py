from dash import Dash, html, Input, Output, callback
import dash_bio as dashbio
import urllib.request as urlreq


import json

app = Dash(__name__)



data = urlreq.urlopen(
    'https://git.io/alignment_viewer_p53.fasta'
).read().decode('utf-8')

app.layout = html.Div([
    dashbio.AlignmentChart(
        id='alignment-viewer-eventDatum-usage',
        data=data,
        height=900,
        tilewidth=30,
    ),
    html.P('Hover or click on data to see it here.'),
    html.Div(id='alignment-viewer-eventDatum-usage-output')
])

@callback(
    Output('alignment-viewer-eventDatum-usage-output', 'children'),
    Input('alignment-viewer-eventDatum-usage', 'eventDatum')
)
def update_output(value):
    if value is None:
        return 'No data.'

    value = json.loads(value)

    if len(value.keys()) == 0:
        return 'No event data to display.'

    return [
        html.Div('- {}: {}'.format(key, value[key]))
        for key in value.keys()
    ]

if __name__ == '__main__':
    app.run(debug=True)
