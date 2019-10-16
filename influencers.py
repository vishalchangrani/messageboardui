import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
from sklearn import preprocessing
import squarify

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('c:\\Users\\vishal\\mb\\renlist\\possible_influencers.csv')
df = df.sort_values(by=['compound_score'], ascending=False)
df = df.head(6)

fig = go.Figure()


x = 0.
y = 0.
width = 100.
height = 100.
normed = squarify.normalize_sizes(df['compound_score'], width, height)
rects = squarify.squarify(normed, x, y, width, height)

color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
                'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)']

shapes = []
annotations = []
counter = 0


for r, val, color in zip(rects, df['compound_score'], color_brewer):
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
            text = val,
            showarrow = False
        )
    )

fig.add_trace(go.Scatter(
    x = [ r['x']+(r['dx']/2) for r in rects ],
    y = [ r['y']+(r['dy']/2) for r in rects ],
    text = [ str(v) for v in df['compound_score'] ],
    mode = 'text',
))

fig.update_layout(
    height=700,
    width=700,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    shapes=shapes,
    annotations=annotations,
    hovermode='closest'
)

fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)

