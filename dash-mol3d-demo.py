from dash import Dash, html, dash_table, Input, Output, callback
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the Dash app with Bootstrap support
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           external_scripts=['/static/js/mol3d-responsive.js']
           )

parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='cartoon', color_element='chain',
    color_scheme={'A': '#facd60', 'P': '#fb7756', 'T': '#fb7756'}
)

df = pd.DataFrame(data["atoms"])
df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))

# Enhanced layout with Bootstrap
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Protein Structure Viewer", href="#"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="#", id="home-link")),
                        dbc.NavItem(dbc.NavLink("Results", href="#", id="results-link")),
                    ],
                    className="navbar-nav",
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="navbar-expand-lg",
)

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(navbar)),  # NavBar
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Residue Information"),
                            dbc.CardBody(
                                dash_table.DataTable(
                                    id="zooming-specific-residue-table",
                                    columns=[{"name": i, "id": i}
                                             for i in df.columns],
                                    data=df.to_dict("records"),
                                    row_selectable="single",
                                    page_size=10,
                                    style_table={
                                        'overflowX': 'scroll',
                                    },
                                    style_cell={
                                        'textAlign': 'left',
                                        'font_family': 'Arial',
                                        'font_size': '16px'
                                    },
                                ),
                            ),
                        ]
                    ),
                    width={"size": 6, "offset": 0}
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("3D Protein Structure"),
                            dbc.CardBody(
                                # Add a box around Molecule3dViewer
                                dashbio.Molecule3dViewer(
                                    id="zooming-specific-molecule3d-zoomto",
                                    modelData=data,
                                    styles=styles,
                                    # Responsive
                                    style={"width": "100%", "height": "100%"}
                                ),
                                style={
                                    'padding': '10px',
                                    'width': '100%',  # Responsive
                                    'height': '600px',
                                }
                            ),
                        ]
                    ),
                    # Bootstrap responsive setting
                    width={"size": 12, "offset": 0, "order": "last"},
                    # Bootstrap responsive setting for medium screens
                    md={"size": 6, "offset": 0, "order": "first"}
                ),
            ]
        )
    ],
    fluid=True
)


@callback(
    Output("zooming-specific-molecule3d-zoomto", "zoomTo"),
    Output("zooming-specific-molecule3d-zoomto", "labels"),
    Input("zooming-specific-residue-table", "selected_rows"),
    prevent_initial_call=True
)
def residue(selected_row):
    row = df.iloc[selected_row]
    row['positions'] = row['positions'].apply(
        lambda x: [float(x) for x in x.split(',')])
    return [
        {
            "sel": {"chain": row["chain"], "resi": row["residue_index"]},
            "animationDuration": 1500,
            "fixedPath": True,
        },
        [
            {
                "text": "Residue Name: {}".format(row["residue_name"].values[0]),
                "position": {
                    "x": row["positions"].values[0][0],
                    "y": row["positions"].values[0][1],
                    "z": row["positions"].values[0][2],
                },
            }
        ],
    ]


if __name__ == "__main__":
    app.run(debug=True)
