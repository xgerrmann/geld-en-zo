import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pfinsim
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes

dash_app = dash.Dash(__name__)
app = dash_app.server

default_salary = 24000


def plot_tax_credits():
    fig = go.Figure()
    gross_incomes = range(0, 120000, 10)
    column_names = ['work_tax_credit', 'general_tax_credit', 'total_credit']
    df = pd.DataFrame(index=gross_incomes, columns=column_names)
    for gross_income in gross_incomes:
        work_discount = taxes.calc_work_tax_discount(gross_income)
        general_discount = taxes.calc_general_tax_discount(gross_income)
        total_discount = work_discount + general_discount
        df.loc[gross_income] = (work_discount, general_discount, total_discount)

    df.index.name = 'gross'
    df = df.reset_index()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df.work_tax_credit,
        mode='lines',
        name='Arbeidskorting'
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df.general_tax_credit,
        mode='lines',
        name='Algemene heffingskorting'
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df.total_credit,
        mode='lines',
        name='Totaal'
    ))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig


def create_layout():
    global dash_app
    dash_app.layout = html.Div(children=[

        dcc.Graph(figure=plot_tax_credits(), id='tax_credit_graph'),

        html.Div(
            [html.H1('Bereken eigen situatie'),
             html.Div([
                 dcc.Slider(
                     id='slider',
                     min=0,
                     max=100000,
                     step=1,
                     value=default_salary,
                     tooltip={'always_visible': True}
                 ),
                 dcc.Input(id="salary_input",
                           type="number",
                           value=default_salary,
                           min=0,
                           max=100000,
                           placeholder=default_salary)
             ], id="input_div"),
             html.Div(id='output')],
            id="numerical_data"
        ),

    ])


last_salary = default_salary
last_salary2 = default_salary
last_input_salary = default_salary


@dash_app.callback(
    Output(component_id='slider', component_property='value'),
    Input(component_id='salary_input', component_property='value'),
)
def update_slider(salary):
    return salary


@dash_app.callback(
    Output(component_id='salary_input', component_property='value'),
    Input(component_id='slider', component_property='value'),
)
def update_input_field(salary):
    return salary


@dash_app.callback(
    Output(component_id='output', component_property='children'),
    Input(component_id='salary_input', component_property='value'),
    Input(component_id='slider', component_property='value')
)
def determine_taxable_income(salary, salary2):
    if salary is None:
        salary = 0

    global last_salary, last_salary2, last_input_salary
    if last_salary != salary:
        input_salary = salary
        last_salary = salary
    elif last_salary2 != salary2:
        input_salary = salary2
        last_salary2 = salary2
    else:
        input_salary = last_input_salary

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
                    html.Tr(children=[html.Td('Arbeidskorting'),
                                      html.Td(f'{work_tax_credit:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Algemene heffingskortingkorting', className='border_bottom'),
                                      html.Td(f'{general_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Totaal belastbaar inkomen'),
                                      html.Td(f'{taxable_income:.2f} €', className="align_right")])
                ])
            ]
        )
    )


def init_taxes():
    tax_settings = pfinsim.common.load_settings('settings.yml')['taxes']
    return Taxes(tax_settings)


if __name__ == '__main__':
    taxes = init_taxes()
    create_layout()
    dash_app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False, port=8080)
    # dash_app.run_server(debug=True)
