# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import squarify
import plotly.graph_objs as go

max_influencer_count = 10

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


df = pd.read_csv('c:\\Users\\vishal\\mb\\renlist\\possible_influencers.csv')
df['compound_score'] = df['compound_score'].round().astype(int)
df = df.sort_values(by=['compound_score'], ascending=False)
df = df.head(max_influencer_count)

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)','rgb(51,160,44)',\
    'rgb(251,154,153)','rgb(227,26,28)','rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)',\
    'rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Message Board",
    brand_href="#",
    sticky="top"
)


body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='influencer-scatter-plot'),
                        html.Div(id='influencer-div', children='Top influencers'),
                        dcc.Slider(
                            id='influencer-count-slider',
                            min=1,
                            max=max_influencer_count,
                            value=5,
                            marks={str(i): str(i) for i in range(1, max_influencer_count + 1)},
                            step=1
                        )
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        dcc.Markdown('''
                        # This is an <h1> tag

                        ## This is an <h2> tag

                        ###### This is an <h6> tag
                        ''')
                    ]
                ),
            ])
    ],  className="mt-4")


app.layout = html.Div([navbar, body])

def generate_rects(df):
    x = 0.
    y = 0.
    width = 100.
    height = 100.
    normed = squarify.normalize_sizes(df['compound_score'], width, height)
    rects = squarify.squarify(normed, x, y, width, height)
    return rects

def generate_shapes(df):
    rects = generate_rects(df)
    shapes = []
    annotations = []
    for r, author, score, color in zip(rects, df['author'], df['compound_score'], color_brewer):
        shapes.append(
        dict(
                type = 'rect',
                x0 = r['x'],
                y0 = r['y'],
                x1 = r['x']+r['dx'],
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color
            )        
    )

        annotations.append(
                dict(
                    x = r['x']+(r['dx']/2),
                    y = r['y']+(r['dy']/2),
                    text = '<b>' + author + '</b><br> Score: ' + str(score),
                    showarrow = False
                )
        )
    return (rects, shapes, annotations)

@app.callback(
    Output('influencer-scatter-plot', 'figure'),
    [Input('influencer-count-slider', 'value')])
def update_figure(influencers_count):
    top_df = df.head(influencers_count)
    (rects, shapes, annotations) = generate_shapes(top_df)
    return {
    'data': [go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ],
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = [ str(v) for v in top_df['compound_score'] ],
        mode = 'text'
        )],
    'layout': go.Layout(
        #height=700,
        #width=700,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
       # plot_bgcolor='rgba(1,1,1,1)'
    )
    }



if __name__ == '__main__':
    app.run_server(debug=True)