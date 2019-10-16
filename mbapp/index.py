from app import app
from apps import influencer_app, thread_app
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


subnav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Influencers", active=True, href="/apps/influencers")),
        dbc.NavItem(dbc.NavLink("Threads", href="/apps/threads"))
    ],
    #pills=True, ##doesn't toggle
)

navbar = dbc.NavbarSimple(
    children=[
        subnav,
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Account",
            children=[
                dbc.DropdownMenuItem("Settings", href="#"),
                dbc.DropdownMenuItem("Profile", href="#"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Logout"),
            ],
        ),
    ],
    brand="Message Board",
    brand_href="#",
    sticky="top"
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className="mt-4"),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/influencers' or pathname == '/':
        return influencer_app.layout
    elif pathname == '/apps/threads':
        return thread_app.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)