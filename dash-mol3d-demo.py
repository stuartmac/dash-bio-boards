from dash import Dash, html, dash_table, Input, Output, State, callback, dcc
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the Dash app with Bootstrap support
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
           external_scripts=['/static/js/mol3d-responsive.js']
           )

# Parse PDB from local file or URL
parser = PdbParser('data/pdb3tx7.ent')

# Create styles for Molecule3dViewer
data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='cartoon', color_element='chain',
    color_scheme={'A': '#facd60', 'P': '#fb7756'}
)

# Create a DataFrame with residue information
df = pd.DataFrame(data["atoms"])
df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))
df = df[df['name'] == 'CA']
df = df[['chain', 'residue_name', 'residue_index', 'positions']]

# Load variant table from HDF5 file
variants = pd.read_hdf(
    'data/PF00104.29-swiss-varalign-tables.h5', key='variants')
variants_columns = variants.columns.tolist()
# Drop problematic columns
variants_columns.pop(97)  # ('Row', 'FILTER')
variants_columns.pop(95)  # ('Row', 'ALT')
variants = variants[variants_columns]

# Flatten multi-level columns
variants.columns = ['_'.join(col).strip() for col in variants.columns.values]

# The column options for the dropdown
column_options = [{'label': col, 'value': col} for col in variants.columns]

# Default columns to display
try:
    default_columns = ['Alignment_Column', 'VEP_SWISSPROT',
                       'VEP_HGVSp', 'VEP_Consequence', 'Allele_INFO_AC', 'Site_INFO_AN']
except:
    default_columns = variants.columns[:10].tolist()

# Enhanced layout with Bootstrap
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Protein Structure Viewer", href="#"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(
                            "Home", href="#", id="home-link")),
                        dbc.NavItem(dbc.NavLink(
                            "Results", href="#", id="results-link")),
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
                                className="data-table-card-body"
                            ),
                        ],
                        className="data-table-card"
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
                                },
                                className="mol3d-card-body"
                            ),
                        ],
                        className="mol3d-card"
                    ),
                    # Bootstrap responsive setting
                    width={"size": 12, "offset": 0, "order": "last"},
                    # Bootstrap responsive setting for medium screens
                    md={"size": 6, "offset": 0, "order": "first"}
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Row(
                                [
                                    dbc.Col("Variants", width={"size": 11}),
                                    dbc.Col(
                                        dbc.Button(
                                            html.I(className="fa fa-cog"), id="toggle-button", color="light", className="me-1", size="sm",
                                        ),
                                        className="ms-auto text-end"  # Pushes the Col to the far right
                                    )
                                ]
                            )
                        ),
                        dbc.CardBody(
                            [
                                dbc.Collapse(
                                    dcc.Dropdown(
                                        id='column-dropdown',
                                        options=column_options,
                                        value=default_columns,
                                        multi=True
                                    ),
                                    id='dropdown-collapse',
                                    is_open=True  # Initially open
                                ),
                                dash_table.DataTable(
                                    id="zooming-specific-variants-table",
                                    columns=[{'name': i, 'id': i}
                                             for i in default_columns],
                                    data=variants.to_dict("records"),
                                    page_size=10,
                                    style_table={'overflowX': 'scroll'},
                                    style_cell={
                                        'textAlign': 'left', 'font_family': 'Arial', 'font_size': '16px'},
                                    sort_action='native',
                                    filter_action='native',
                                    row_selectable='single',
                                    tooltip_header={
                                        'Alignment_Column': 'Position in Pfam alignment',
                                        'VEP_SWISSPROT': 'UniProtKB/Swiss-Prot accession of the protein',
                                        'VEP_HGVSp': 'Variant protein sequence annotation in the format p.(<pos><ref_aa><pos><alt_aa>)',
                                        'VEP_Consequence': 'The VEP predicted consequence',  # http://www.ensembl.org/info/genome/variation/prediction/predicted_data.html
                                        'Allele_INFO_AC': 'Variant allele count',
                                        'Site_INFO_AN': 'Total number of alleles in called genotypes',
                                    },
                                    # Style headers with a dotted underline to indicate a tooltip
                                    style_header={
                                        'textDecoration': 'underline',
                                        'textDecorationStyle': 'dotted',
                                    },
                                    # TODO: Customise export UX
                                    export_format='csv',
                                    export_headers='names'
                                ),
                            ],
                            className="variants-table-card-body"

                        ),
                    ],
                    className="variants-table-card"
                ),
                width={"size": 12, "offset": 0}
            )
        ),
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


@callback(
    Output('zooming-specific-variants-table', 'columns'),
    Input('column-dropdown', 'value'),
    prevent_initial_call=True
)
def update_columns(selected_columns):
    return [{'name': i, 'id': i} for i in selected_columns]


@app.callback(
    Output('dropdown-collapse', 'is_open'),
    [Input('toggle-button', 'n_clicks')],
    [State('dropdown-collapse', 'is_open')]
)
def toggle_dropdown(n, is_open):
    return not is_open


if __name__ == "__main__":
    app.run(debug=True)
