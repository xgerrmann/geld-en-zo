import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes
from plotly.subplots import make_subplots

import pfinsim
from common import app, default_salary


def income_taxes_app(pathname):
    available_years = list(pfinsim.common.load_settings()['taxes'].keys())
    available_years.sort(reverse=True)
    selected_year = available_years[0]
    tax_settings = pfinsim.common.load_settings()['taxes'][selected_year]
    taxes = Taxes(tax_settings)
    return html.Div(children=[
        html.Div(children=[plot_income_taxes(taxes, selected_year)], id='income_tax_plot_div'),
        dcc.Checklist(
            options=[
                {'label': 'Inclusief heffingskortingen', 'value': True},
            ],
            value=[True],
            id='include_tax_credit_checkbox'
        ),
        dcc.Dropdown(
          id='income_taxes_year_selection',
          options=[{'label': year, 'value': year} for year in available_years],
          value=selected_year
        ),
        html.Div(
            [html.H1('Bereken eigen situatie'),
             html.Div(children=[
                 html.Label(children=['Bruto jaarinkomen'], className='input_label'),
                 dcc.Input(id="income_taxes_salary_input",
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

@app.callback(Output(component_id='income_tax_plot_div', component_property='children'),
              [Input(component_id='include_tax_credit_checkbox', component_property='value'),
               Input(component_id='income_taxes_year_selection', component_property='value')])
def update_income_tax_plot(include_tax_credit, selected_year):
    taxes = Taxes(pfinsim.common.load_settings()['taxes'][selected_year])

    if include_tax_credit and include_tax_credit[0] == True:
        return plot_income_taxes(taxes, selected_year)
    return plot_income_taxes(taxes, selected_year, include_tax_credits=False)

@app.callback(
    Output(component_id='output_income_taxes_app', component_property='children'),
    [Input(component_id='income_taxes_salary_input', component_property='value'),
     Input(component_id='income_taxes_year_selection', component_property='value')])
def determine_nett_income(gross_income, selected_year):
    gross_income = gross_income or 0
    taxes = Taxes(pfinsim.common.load_settings()['taxes'][selected_year])

    work_tax_credit = taxes.calc_work_tax_discount(gross_income)
    general_tax_credit = taxes.calc_general_tax_discount(gross_income)
    total_tax_credit = work_tax_credit + general_tax_credit

    subtotal_income_tax, income_tax_buckets = taxes.calc_income_tax(gross_income)

    total_income_tax = taxes.calc_total_income_tax(gross_income)

    nett_income = gross_income - total_income_tax

    tax_settings = pfinsim.common.load_settings()['taxes'][selected_year]
    income_tax_rates = [rate*100 for rate in tax_settings['income_tax']['rates']]
    return (
        html.Table(
            [
                html.Tbody([
                    *[
                        html.Tr(children=[html.Td(f'Belasting schijf {ii + 1} ({income_tax_rates[ii]}%) '),
                                          html.Td(f'{income_tax_bucket:.2f} €', className="align_right")], className=f"{'border_bottom' if ii +1 == len(income_tax_buckets) else ''}")
                        for ii, income_tax_bucket in enumerate(income_tax_buckets)],
                    html.Tr(children=[html.Td('Inkomstenbelasting'),
                                      html.Td(f'{subtotal_income_tax:.2f} €', className="align_right bottom_row")]),
                  html.Tr(children=[html.Td(),
                                    html.Td(' ', className="align_right")]),
                  html.Tr(children=[html.Td('Arbeidskorting'),
                                    html.Td(f'{work_tax_credit:.2f} €', className="align_right")]),
                  html.Tr(children=[html.Td('Algemene heffingskorting', className='border_bottom'),
                                    html.Td(f'{general_tax_credit:.2f} €', className="align_right border_bottom")]),
                  html.Tr(children=[html.Td('Totaal heffingskortingen'),
                                    html.Td(f'{total_tax_credit:.2f} €', className="align_right bottom_row")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    html.Tr(children=[html.Td('Inkomstenbelasting'),
                                      html.Td(f'{subtotal_income_tax:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Totaal heffingskortingen', className='border_bottom'),
                                      html.Td(f'- {total_tax_credit:.2f} €', className="align_right border_bottom")]),
                    html.Tr(children=[html.Td('Effectieve inkomstenbelasting'),
                                      html.Td(f'{total_income_tax:.2f} €', className="align_right bottom_row")]),
                    html.Tr(children=[html.Td(),
                                      html.Td(' ', className="align_right")]),
                    html.Tr(children=[html.Td('Bruto inkomen'),
                                      html.Td(f'{gross_income:.2f} €', className="align_right")]),
                    html.Tr(children=[html.Td('Effectieve inkomstenbelasting'),
                                      html.Td(f'{- total_income_tax:.2f} €', className="align_right")],
                            className="border_bottom"),
                    html.Tr(children=[html.Td('Netto jaarsalaris'),
                                      html.Td(f'{nett_income:.2f} €', className="align_right bottom_row")]),
                  # html.Tr(children=[html.Td(),
                  #                   html.Td(' ', className="align_right")]),
                  # html.Tr(children=[html.Td('Netto maandsalaris'),
                  #                   html.Td(f'{(nett_income/1.08/12):.2f} €', className="align_right")]),
                ])
            ]
        )
    )

def plot_income_taxes(taxes, selected_year, include_tax_credits=True):
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
            'text': f"Belasting vs inkomen {selected_year}",
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
