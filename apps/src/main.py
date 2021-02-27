import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from common import app, server
from income_taxes import income_taxes_app
from tax_credit import tax_credit_app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def default_app(pathname):
    return '404, Page not found'


app_dict = {
    '/tax_credit': tax_credit_app,
    '/income_taxes': income_taxes_app
}


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    page = app_dict.get(pathname, default_app)
    return page(pathname)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=8080,
                   debug=False,
                   dev_tools_ui=False,
                   dev_tools_props_check=False,
                   use_reloader=False)
