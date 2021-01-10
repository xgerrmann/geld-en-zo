import dash
import dash_core_components as dcc
import dash_html_components as html
import pfinsim
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes
from plotly.subplots import make_subplots


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
    ), plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "Heffingskortingen vs inkomen",
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis={
            'linecolor': '#BCCCDC',
            'showgrid': False,
            'fixedrange': True,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': "#999999",
            'spikemode': "across"
        },
        yaxis={
            'linecolor': '#BCCCDC',
            'showgrid': False,
            'fixedrange': True,
            'range': [0, 4000]
        },
        font=dict(
            size=16,
        )
    )
    fig.update_yaxes(title="Hoogte korting [€]")
    fig.update_xaxes(title="Inkomen [€]")

    return fig


def plot_income_taxes(include_tax_credits=True):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    gross_incomes = range(0, 120000, 50)
    tax_list = []
    tax_list_perc = []
    for gross_income in gross_incomes:
        taxable_income = gross_income
        if include_tax_credits:
            work_discount = taxes.calc_work_tax_discount(gross_income)
            general_discount = taxes.calc_general_tax_discount(gross_income)
            total_discount = work_discount + general_discount
            taxable_income -= total_discount

        total_income_tax, income_tax_buckets = taxes.calc_income_tax(taxable_income)

        tax_list.append(total_income_tax)
        tax_list_perc.append(total_income_tax / (gross_income + 1e-6) * 100)

    fig.add_trace(go.Scatter(
        x=list(gross_incomes),
        y=tax_list,
        mode='lines',
        name='Belasting (€)',
    ),
        secondary_y=False)

    fig.add_trace(go.Scatter(
        x=list(gross_incomes),
        y=tax_list_perc,
        mode='lines',
        name='Belasting (%)',
    ),
        secondary_y=True)

    fig.update_layout(legend=dict(
        orientation="v",
        yanchor="top",
        y=-0.2,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0)'
    ), plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "Belasting vs inkomen",
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis={
            'linecolor': '#BCCCDC',
            'showgrid': False,
            # 'fixedrange': True,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': "#999999",
            'spikemode': "across"
        },
        font=dict(
            size=16,
        )
    )

    fig.update_yaxes(title_text="Absolute belasting", secondary_y=False, ticksuffix="€",
                     range=[0, 50000])
    fig.update_yaxes(title_text="Procentuele belasting", secondary_y=True, ticksuffix="%",
                     range=[0, 50])
    fig.update_xaxes(title_text="Inkomen uit werk", ticksuffix="€")

    return dcc.Graph(figure=fig, id='income_taxes_graph',
                     config={'displayModeBar': False})


# --------------------------------- DASH ----------------------------- #

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True

# --------------------------------- DASHBOARD ----------------------------- #


default_salary = 24000
tax_settings = pfinsim.common.load_settings()['taxes'][2021]
taxes = Taxes(tax_settings)

input_salary = default_salary

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def default_app(pathname):
    return '404, Page not found'


def tax_credit_app(pathname):
    return html.Div(children=[
        dcc.Graph(figure=plot_tax_credits(), id='tax_credit_graph',
                  config={'displayModeBar': False}),

        html.Div(
            [html.H1('Bereken eigen situatie'),
             html.Div([
                 html.Label(children=['Bruto inkomen'], className='input_label'),
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


def income_taxes_app(pathname):
    return html.Div(children=[
        html.Div(children=[plot_income_taxes()], id='test_output'),
        dcc.Checklist(
            options=[
                {'label': 'Inclusief heffingskortingen', 'value': True},
            ],
            value=[True],
            id='include_tax_credit_checkbox'
        ),
        html.Div(
            [html.H1('Bereken eigen situatie'),
             html.Div(children=[
                 html.Label(children=['Bruto inkomen'], className='input_label'),
                 dcc.Input(id="salary_input_2",
                           type="number",
                           value=default_salary,
                           min=0,
                           max=10000000,
                           placeholder=default_salary)
             ], className="input_div"),
             html.Div(id='output_income_taxes_app')],
            id="input_form"
        ),
    ])


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

    # tax_settings
    # self.income_tax_brackets = tax_parameters['income_tax']['brackets']
    # self.income_tax_rates = tax_parameters['income_tax']['rates']
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
                        html.Tr(children=[html.Td(f'Belasting schijf {ii + 1} '),
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
