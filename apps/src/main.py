import dash
import dash_core_components as dcc
import dash_html_components as html
import pfinsim
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes


# --------------------------------- PYTHON FUNCTIONS ----------------------------- #
from tax_credit import tax_credit_app
from common import default_salary
from income_taxes import income_taxes_app, plot_income_taxes

# --------------------------------- DASH ----------------------------- #

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True

# --------------------------------- DASHBOARD ----------------------------- #


tax_settings = pfinsim.common.load_settings()['taxes'][2021]
taxes = Taxes(tax_settings)

input_salary = default_salary

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def default_app(pathname):
    return '404, Page not found'


@app.callback(dash.dependencies.Output(component_id='test_output', component_property='children'),
              [dash.dependencies.Input(component_id='include_tax_credit_checkbox', component_property='value')])
def display_page(value):
    if value and value[0] is True:
        return plot_income_taxes()
    return plot_income_taxes(include_tax_credits=False)


app_dict = {
    '/tax_credit': tax_credit_app,
    '/income_taxes': income_taxes_app
}


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    page = app_dict.get(pathname, default_app)
    return page(pathname)


@app.callback(
    Output(component_id='output', component_property='children'),
    Input(component_id='salary_input', component_property='value'),
)
def determine_taxable_income(salary):
    global taxes
    if salary is None:
        salary = 0

    global input_salary
    if input_salary != salary:
        input_salary = salary

    work_tax_credit = taxes.calc_work_tax_discount(input_salary)
    general_tax_credit = taxes.calc_general_tax_discount(input_salary)
    taxable_income = max(input_salary - work_tax_credit - general_tax_credit, 0)
    total_tax_credit = work_tax_credit + general_tax_credit

    return (
        html.Table(
            [
                html.Tbody([
                    html.Tr(children=[html.Td('Arbeidskorting'),
                                      html.Td(f'{work_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Algemene heffingskorting', className='border_bottom'),
                                      html.Td(f'{general_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal heffingskortingen'),
                                      html.Td(f'{total_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    html.Tr(children=[html.Td('Inkomsten uit loon'),
                                      html.Td(f'{input_salary:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Totaal heffingskortingen', className='border_bottom'),
                                      html.Td(f'- {total_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal belastbaar inkomen'),
                                      html.Td(f'{taxable_income:.2f} €', className="align_right bottom_row")])
                ])
            ]
        )
    )


@app.callback(
    Output(component_id='output_income_taxes_app', component_property='children'),
    Input(component_id='salary_input_2', component_property='value'),
)
def determine_nett_income(gross_income):
    global taxes
    gross_income = gross_income or 0

    work_tax_credit = taxes.calc_work_tax_discount(gross_income)
    general_tax_credit = taxes.calc_general_tax_discount(gross_income)
    taxable_income = max(gross_income - work_tax_credit - general_tax_credit, 0)
    total_tax_credit = work_tax_credit + general_tax_credit

    total_income_tax, income_tax_buckets = taxes.calc_income_tax(taxable_income)

    nett_income = gross_income - total_income_tax

    # tax_settings
    tax_settings = pfinsim.common.load_settings()['taxes'][2021]
    # self.income_tax_brackets = tax_settings['income_tax']['brackets']
    income_tax_rates = [rate*100 for rate in tax_settings['income_tax']['rates']]
    return (
        html.Table(
            [
                html.Tbody([
                    html.Tr(children=[html.Td('Arbeidskorting'),
                                      html.Td(f'{work_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Algemene heffingskorting', className='border_bottom'),
                                      html.Td(f'{general_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal heffingskortingen'),
                                      html.Td(f'{total_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    html.Tr(children=[html.Td('Inkomsten uit loon'),
                                      html.Td(f'{gross_income:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Totaal heffingskortingen', className='border_bottom'),
                                      html.Td(f'- {total_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal belastbaar inkomen'),
                                      html.Td(f'{taxable_income:.2f} €', className="align_right bottom_row")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    *[
                        html.Tr(children=[html.Td(f'Belasting schijf {ii + 1} ({income_tax_rates[ii]}%) '),
                                          html.Td(f'{income_tax_bucket:.2f} €', className="align_right")], className=f"{'border_bottom' if ii +1 == len(income_tax_buckets) else ''}")
                        for ii, income_tax_bucket in enumerate(income_tax_buckets)],
                    html.Tr(children=[html.Td('Totale inkomstenbelasting'),
                                      html.Td(f'{total_income_tax:.2f} €', className="align_right bottom_row")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    html.Tr(children=[html.Td('Bruto inkomen'),
                                      html.Td(f'{gross_income:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Totale inkomstenbelasting'),
                                      html.Td(f'{- total_income_tax:.2f} €', className="align_right")],
                            className="border_bottom"),
                    html.Tr(children=[html.Td('Netto salaris'),
                                      html.Td(f'{nett_income:.2f} €', className="align_right bottom_row")]),
                ])
            ]
        )
    )


# --------------------------------- PYTHON FUNCTIONS ----------------------------- #

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=8080,
                   debug=False,
                   dev_tools_ui=False,
                   dev_tools_props_check=False,
                   use_reloader=False)
