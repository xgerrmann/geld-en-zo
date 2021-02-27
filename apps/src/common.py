import dash

default_salary = 24000

app = dash.Dash(__name__, suppress_callback_exceptions = True)
server = app.server

