import dash
import dash_core_components as dcc
import dash_html_components as html
import pfinsim
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes


# --------------------------------- PYTHON FUNCTIONS ----------------------------- #

def plot_tax_credits():
    fig = go.Figure()
    gross_incomes = range(0, 120000, 10)
    discount_work = []
    discount_general = []
    discount_total = []
    for gross_income in gross_incomes:
        work_discount = taxes.calc_work_tax_discount(gross_income)
        general_discount = taxes.calc_general_tax_discount(gross_income)
        total_discount = work_discount + general_discount
        discount_work.append(work_discount)
        discount_general.append(general_discount)
        discount_total.append(total_discount)

    fig.add_trace(go.Scatter(
        x=list(gross_incomes),
        y=discount_work,
        mode='lines',
        name='Arbeidskorting'
    ))

    fig.add_trace(go.Scatter(
        x=list(gross_incomes),
        y=discount_general,
        mode='lines',
        name='Algemene heffingskorting'
    ))

    fig.add_trace(go.Scatter(
        x=list(gross_incomes),
        y=discount_total,
        mode='lines',
        name='Totaal'
    ))

    fig.update_layout(legend=dict(
        orientation="v",
        yanchor="top",
        y=-0.2,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0)'
    ), title="Heffingskortingen vs inkomen",
        margin=dict(l=0, r=0, t=30, b=0))
    fig.update_yaxes(title="Hoogte korting [€]")
    fig.update_xaxes(title="Inkomen [€]")

    return fig


# --------------------------------- DASH ----------------------------- #

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True

# --------------------------------- DASHBOARD ----------------------------- #


default_salary = 24000
tax_settings = pfinsim.common.load_settings('settings.yml')['taxes']
taxes = Taxes(tax_settings)

input_salary = default_salary
last_input_salary = default_salary

app.layout = html.Div(children=[

    dcc.Graph(figure=plot_tax_credits(), id='tax_credit_graph'),

    html.Div(
        [html.H1('Bereken eigen situatie'),
         html.Div([
             dcc.Input(id="salary_input",
                       type="number",
                       value=default_salary,
                       min=0,
                       max=10000000,
                       placeholder=default_salary)
         ], id="input_div"),
         html.Div(id='output')],
        id="input_form"
    ),

])


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
    return (
        html.Table(
            [
                html.Thead(
                    [html.Tr([html.Th('Component'),
                              html.Th('Bedrag')])]
                ),
                html.Tbody([
                    html.Tr(children=[html.Td('Inkomsten uit loon'),
                                      html.Td(f'{input_salary:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Arbeidskorting'),
                                      html.Td(f'- {work_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Algemene heffingskortingkorting', className='border_bottom'),
                                      html.Td(f'- {general_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal belastbaar inkomen'),
                                      html.Td(f'{taxable_income:.2f} €', className="align_right bottom_row")])
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
