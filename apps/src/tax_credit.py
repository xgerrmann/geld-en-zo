import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pfinsim.taxes import Taxes

import pfinsim
from common import app, default_salary


input_salary = default_salary

def plot_tax_credits(taxes, selected_year):
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
      'text': f"Heffingskortingen vs inkomen {selected_year}",
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
      'range': [0, 7000]
    },
    font=dict(
      size=16,
    )
  )
  fig.update_yaxes(title="Hoogte korting [€]")
  fig.update_xaxes(title="Inkomen [€]")
  return dcc.Graph(figure=fig, id='tax_credit_graph',
            config={'displayModeBar': False})

def tax_credit_app(pathname):
    available_years = list(pfinsim.common.load_settings()['taxes'].keys())
    available_years.sort(reverse=True)
    selected_year = available_years[0]

    tax_settings = pfinsim.common.load_settings()['taxes'][selected_year]
    taxes = Taxes(tax_settings)

    return html.Div(children=[
      html.Div(children=[plot_tax_credits(taxes, selected_year)], id='tax_credit_plot_div'),
      dcc.Dropdown(
        id='tax_credit_year_selection',
        options=[{'label': year, 'value': year} for year in available_years],
        value=selected_year
      ),
        html.Div(
            [html.H1('Bereken eigen situatie'),
             html.Div([
                 html.Label(children=['Bruto jaarinkomen'], className='input_label'),
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

@app.callback(Output(component_id='tax_credit_plot_div', component_property='children'),
               Input(component_id='tax_credit_year_selection', component_property='value'))
def update_tax_credit_plot(selected_year):
    taxes = Taxes(pfinsim.common.load_settings()['taxes'][selected_year])
    return plot_tax_credits(taxes, selected_year)

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='salary_input', component_property='value'),
     Input(component_id='tax_credit_year_selection', component_property='value')],
)
def determine_taxable_income(salary, selected_year):
    taxes = Taxes(pfinsim.common.load_settings()['taxes'][selected_year])

    if salary is None:
        salary = 0

    global input_salary
    if input_salary != salary:
        input_salary = salary

    work_tax_credit = taxes.calc_work_tax_discount(input_salary)
    general_tax_credit = taxes.calc_general_tax_discount(input_salary)
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
                                      html.Td(f'{total_tax_credit:.2f} €', className="align_right bottom_row")]),
                ])
            ]
        )
    )

