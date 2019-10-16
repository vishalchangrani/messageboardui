import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from app import app
import datetime
from calendar import monthrange

messages = pd.read_csv('c:\\Users\\vishal\\mb\\renlist\\complete_threads.csv')
messages['date'] = pd.to_datetime(messages['date'])
threads = messages.groupby(['thread_id']).sum()

maxm = messages[messages['thread_id'] == threads.counts.idxmax()][['date', 'counts']]
maxm = maxm.set_index('date')
maxm = maxm.asfreq('D', fill_value=0)
maxm = maxm.reset_index()
day = [(360 / monthrange(d.year, d.month)[1]) * d.day for d in maxm['date'] ]

threads = threads.reset_index()

#g = maxm.groupby(pd.Grouper(key='date', freq='D'))
#a = g.size().reset_index(name='counts')


layout = \
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                       dash_table.DataTable(
                            id='table',
                            columns=[{'id': c, 'name': c} for c in threads.columns],
                            data=threads.to_dict('records'),
                            fixed_rows={ 'headers': True, 'data': 0 },
                            style_table={
                                'maxHeight': '10',
                                'overflowY': 'scroll'
                            },
                        )
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='threadactivity-scatter-plot'),
                        dcc.Slider(
                            id='threadactivity-count-slider',
                            min=1,
                            max=3,
                            value=3,
                            marks={'1': 'day', '2': 'month', '3':'year'},
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
    ]



@app.callback(
    Output('threadactivity-scatter-plot', 'figure'),
    [Input('threadactivity-count-slider', 'value')])
def update_figure(influencers_count):
    return {
    'data': [go.Scatterpolar(
        r = maxm['date'],
        theta = [(360 / monthrange(d.year, d.month)[1]) * d.day for d in maxm['date'] ],
        mode = 'lines+markers',
        marker = dict(size=maxm['counts']),
        hovertext= [', total: '.join(i) for i in zip(pd.DatetimeIndex(maxm.date).strftime('%B %d, %Y'),maxm['counts'].map(str))],
        hoverinfo="text",
        line=dict(dash='dot', width=0.2, smoothing=1.3, shape='spline')
        #angularaxis=dict(visible=False)
   )],
    'layout': go.Layout(
        polar = dict(
            radialaxis = dict(visible=True, autorange=True, type="date", gridwidth=0),
            angularaxis = dict(visible=True, tickmode="array", tickvals=[0, 7*12,2 * 7 *12, 3 * 7 * 12 ],  ticktext=['First day', 'First week', 'Second week', 'Third week'])
        ),
        showlegend = False,
        width = 800,
        height = 800
    )
    }



