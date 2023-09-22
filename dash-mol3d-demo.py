from dash import Dash, html, dash_table, Input, Output, callback
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
import pandas as pd

app = Dash(__name__)

parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='cartoon', color_element='residue'
)

df = pd.DataFrame(data["atoms"])
df = df.drop_duplicates(subset=['residue_name'])
df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))

app.layout = html.Div(
    [
        dash_table.DataTable(
            id="zooming-specific-residue-table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            row_selectable="single",
            page_size=10,
        ),
        dashbio.Molecule3dViewer(
            id="zooming-specific-molecule3d-zoomto",
            modelData=data,
            styles=styles
        ),
    ]
)


@callback(
    Output("zooming-specific-molecule3d-zoomto", "zoomTo"),
    Output("zooming-specific-molecule3d-zoomto", "labels"),
    Input("zooming-specific-residue-table", "selected_rows"),
    prevent_initial_call=True
)
def residue(selected_row):
    row = df.iloc[selected_row]
    row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])
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
