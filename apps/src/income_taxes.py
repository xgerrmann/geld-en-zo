import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from pfinsim.taxes import Taxes
from plotly.subplots import make_subplots

import pfinsim
from common import default_salary

tax_settings = pfinsim.common.load_settings()['taxes'][2021]
taxes = Taxes(tax_settings)


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
