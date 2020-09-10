# import modules
import dash
import dash_table as dt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Header image
banner = 'https://i.ibb.co/RPZHnw7/flag.png'

# import pandas as pd
# data

# import pandas as pd
data_path = 'data/'
df = pd.read_csv(data_path + 'settlement.csv')
df3 = pd.read_csv(data_path + 'coverage.csv')

# dropdown opetions

#  year dropdown options
year_options = [{"label": year, "value": year}
                for year in df3['YEAR'].unique()]


# region dropdown options
region_options = [{"label": region, "value": region}
                  for region in df3['REGION'].unique()]


def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (
                        i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                linear-gradient(90deg,
                #8e2bd4 0%,
                #8e2bd4 {max_bound_percentage}%,
                #010002 {max_bound_percentage}%,
                #010002 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


app = dash.Dash(__name__)

server = app.server


dropdowns = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup([
                dbc.Label('YEAR',
                          style={'color': 'white',
                                 'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '15px'}),
                dcc.Dropdown(id="year", options=year_options, value=df3['YEAR'].unique().max(),)]
            ), md=3),

        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('REGION', style={'color': 'white',
                                               'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '15px'}),
                    dcc.Dropdown(
                        id="region",
                        options=region_options,
                        value='Western 1'
                    ),

                ]
            ),
            md=3,
        ),

        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('DISTRICT', style={'color': 'white',
                                                 'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '15px'}),
                    dcc.Dropdown(
                        id="district"), ]
            ),
            md=3,
        ),

        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('FACILITY', style={'color': 'white',
                                                 'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '15px'}),
                    dcc.Dropdown(
                        id="facility"),
                ]),
            md=3,
        )
    ],
    form=True,
)


app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col
            ([
                html.Div
                ([
                    html.Img(className='img-fluid',
                             src='https://i.ibb.co/RPZHnw7/flag.png', style={'width': '100%', 'height': '30px'}),

                ]),

            ], md=12)]),
        dbc.Row([
            dbc.Col
            ([html.H4('THE GAMBIA EXPANDED PROGRAMME OF IMMUNIZATION', style={'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '35px', 'color': 'white'}), ], md=12)]),

        html.Hr(),
        dbc.Row([
            dbc.Col([html.Div([html.Section([html.Div([
                html.Div(id="image"),
                dcc.Interval(id='interval', interval=5000),
                html.H6('NEWS and UPDATES', style={'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '20px', 'padding': '10px', 'color': 'white'})], id="slideshow-container")], id="slideshow")])], width={"size": 8, "offset": 2},)
        ], align="center"),
        html.Hr(),

        dbc.Row(
            [
                dbc.Col(dropdowns, width={'size': 10, 'offset': 1}),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='bcg_graph'),
                        width={'size': 10, 'offset': 1}),
            ],
            align="center"

        ),
        html.Hr(),
        dbc.Row([
            dbc.Col([html.H4('Population Per Settlement', style={'font-family': "Comic Sans MS", 'text-align': 'center', 'font-size': '30px', 'padding': '10px', 'color': 'white'}),
                     dt.DataTable(id='table',
                                  data=df.to_dict('records'),
                                  sort_action='native',
                                  columns=[{'name': i, 'id': i}
                                           for i in df.columns],
                                  style_data_conditional=(
                                      data_bars(df, 'TOTAL')),
                                  style_header={
                                      'backgroundColor': '#1f007e', 'fontWeight': '600'},
                                  style_cell={'backgroundColor': '#020105',
                                              'color': 'white',
                                              'fontWeight': '200',
                                              'textAlign': 'left',
                                              'font-family': 'Droid Sans',
                                              'font-size': '18px'},
                                  page_size=20)],
                    width={'size': 10, 'offset': 1}),
        ]
        )

    ],
    fluid=True,
)


@app.callback(Output('image', 'children'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 3 == 1:
        img = html.Img(className='img-fluid rounded-lg',
                       src="https://i.ibb.co/Yympr7Y/gavi-shifo.jpg", style={'width': '100%', 'height': '250px'})
    elif n % 3 == 2:
        img = html.Img(className='img-fluid rounded-lg',
                       src="https://i.ibb.co/PrT62vs/nose-mask.jpg", style={'width': '100%', 'height': '250px'})
    elif n % 3 == 0:
        img = html.Img(className='img-fluid rounded-lg',
                       src="https://i.ibb.co/wwhV45w/EPI2.jpg", style={'width': '100%', 'height': '250px'})
    else:
        img = "None"
    return img


@app.callback(
    Output('district', 'options'),
    [Input('region', 'value')]
)
def district_options(selected_region):
    return [{'label': district, 'value': district}
            for district in df3[df3['REGION'] == selected_region]['DISTRICT'].unique()]


@app.callback(
    Output('district', 'value'),
    [Input('district', 'options')]
)
def district_values(available_options):
    return available_options[0]['value']


@app.callback(
    Output('facility', 'options'),
    [Input('district', 'value')]
)
def facility_options(selected_district):
    return [{'label': facility, 'value': facility}
            for facility in df3[df3['DISTRICT'] == selected_district]['FACILITY'].unique()]


@app.callback(
    Output('facility', 'value'),
    [Input('facility', 'options')]
)
def facility_values(available_options):
    return available_options[0]['value']


@app.callback(
    Output('bcg_graph', 'figure'),
    [
        Input('year', 'value'),
        Input('region', 'value'),
        Input('district', 'value'),
        Input('facility', 'value')
    ]

)
def create_graph(year, region, district, facility):
    fig = go.Figure()
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July',       'August', 'September', 'October', 'November', 'December']

    df = df3[(df3['YEAR'] == year) & (df3['REGION'] == region) &
             (df3['DISTRICT'] == district) & (df3['FACILITY'] == facility)]

    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "{} has no data available for {}".format(facility, year),

                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            'family': 'Droid Sans',
                            'color': '#ffffff'
                        }
                    }
                ],
                # 'bgcolor': '#010002',
                'paper_bgcolor': ' #061a00',
                'plot_bgcolor':  ' #061a00'
            }
        }
    else:

        df.groupby(pd.Grouper(key='PERIONDNAME'))[
            ['MONTH', 'BCG', 'PENTA_1', 'PENTA_3', 'MEASLES_1', 'DPT']].sum()
        month = df.MONTH
        bcg = df['BCG']
        penta1 = df['PENTA_1']
        penta3 = df['PENTA_3']
        msl = df['MEASLES_1']
        dpt = df['DPT']

        fig.add_trace(
            go.Bar(x=month, y=bcg, name='BCG', marker_color='#ff1dc9'))
        fig.add_trace(go.Bar(x=month, y=penta1,
                             name='PENTA ONE', marker_color='#ff1d58'))
        fig.add_trace(go.Bar(x=month, y=penta3,
                             name='PENTA THREE', marker_color='#ff531d'))
        fig.add_trace(
            go.Bar(x=month, y=msl, name='MEASLES_1', marker_color='#531dff'))
        fig.add_trace(
            go.Bar(x=month, y=dpt, name='DPT BOOSTER', marker_color='#c41dff'))

        fig.update_layout(title=('Monthly Immunization Coverage of {} for {}'.format(facility, year)), font_color='white', paper_bgcolor='#010002', plot_bgcolor='#010002', font={'family': 'Droid Sans'},
                          legend={"bgcolor": '#010002', })

        return fig


if __name__ == "__main__":
    app.run_server(debug=True)
