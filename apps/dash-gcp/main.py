import dash
import dash_core_components as dcc
import dash_html_components as html
import pfinsim
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes

dash_app = dash.Dash(__name__)
app = dash_app.server

default_salary = 24000

dash_app.layout = html.Div(children=[

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
            ],
            'layout': {
                'title': 'Heffingskortingen'
            }
        }
    ),

    html.Div(
        [html.H1('Jaarlijks inkomen'),
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
                   placeholder=default_salary),
         html.Div(id='output')],
        id="numerical_data"
    )

])

last_salary = default_salary
last_salary2 = default_salary
last_input_salary = default_salary


@dash_app.callback(
    Output(component_id='slider', component_property='value'),
    Input(component_id='salary_input', component_property='value'),
)
def update_slider(salary):
    if salary is None:
        salary = 0
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

    print(salary)
    print(salary2)
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
    taxable_income = input_salary - work_tax_credit - general_tax_credit
    return (
        html.Table(
            [
                html.Thead(
                    [html.Tr([html.Th('Component'),
                              html.Th('Bedrag')])]
                ),
                html.Tbody([
                    html.Tr(children=[html.Td('Arbeidsheffings korting'),
                                      html.Td(f'{work_tax_credit:.2f}  €', className="align_right")]),
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
    dash_app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
    # dash_app.run_server(debug=True)
