import pandas as pd
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/alexmagno6m/render/main/BD_SECUNDARIA_2026.csv')
df = pd.read_csv(r, sep=';')
#Para convertir la columna cedula de numero a string
df['Cedula']=df['Cedula'].astype(str)
df = df[['Cedula', 'Profesor_o_curso', 'DIA','FRANJA', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']]
app = Dash(__name__)
app.index_string = """
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Horario Secundaria 2026</title>
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""

server = app.server

''' For input field
                     id='professor_drop',
                     type="text",
                     autoComplete=False,
                     placeholder="Seleccione un curso o profesor"
'''
app.layout = html.Div([
    html.Div([
        html.H2('Horario General Secundaria 2026'),
        html.H2('Colegio Antonio Baraya IED'),
        
        html.Div([
            # Left Card: Cedula Input
            html.Div([
                html.Label("Consulte su horario individual. Digite su número de cédula sin puntos ni comas:", className="input-label"),
                dcc.Input(
                    id='professor_drop',
                    type="text",
                    autoComplete='off', 
                    placeholder="Cédula",
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '4px', 'border': '1px solid #ced4da'} # Inline style for immediate fix, or move to CSS
                ),
                html.Span("Si no visualiza su horario, verifique que no tiene ningún curso seleccionado en la lista desplegable de cursos", className="input-helper")
            ], className="input-card"),

            # Right Card: Course Dropdown
            html.Div([
                html.Label("Para consultar horario de un curso selecciónelo de la lista desplegable:", className="input-label"),
                html.Span("Importante: El campo cédula debe estar vacío", style={'color': '#e03131', 'fontSize': '0.85rem', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    ['601', '602', '603',
                     '701', '702', '703',
                     '801', '802', '803',
                     '901', '902', '903',
                     '1001', '1002', '1003',
                     '1101', '1102', '1103'],
                    id='dia_drop',
                    searchable=False,
                    placeholder="Seleccionar Curso"
                )
            ], className="input-card")
        ], className="input-row"),

        html.Div(
            ["Las franjas mayoritarias A y B, no son aplicables en ciclo V"], # Adjusted text slightly to make sense or keep original? User said "no afectar logica". Keeping original text but in new container.
            className="warning-banner"
        ),

        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=18,
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_data_conditional=(
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} is blank'.format(col),
                                'column_id': col
                            },
                            'backgroundColor': 'gray',
                            'color': 'white'
                        } for col in df.columns
                    ]
                    +
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} contains "TP"'.format(col),
                                'column_id': col
                            },
                            'backgroundColor': '#b8e0d2',
                            'color': 'black'
                        } for col in df.columns
                    ]
                    +
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} = "RA"'.format(col),
                                'column_id': col
                            },
                            'backgroundColor': '#c1fba4',
                            'color': 'black'
                        } for col in df.columns
                    ]
                    +
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} = "RC"'.format(col),
                                'column_id': col
                            },
                            'backgroundColor': '#c1fba4',
                            'color': 'black'
                        } for col in df.columns
                    ]
            ),
            style_cell_conditional=[
                {'if': {'column_id': 'PROFESOR_O_CURSO'},
                 'width': '15%'},
                {'if': {'column_id': 'DIA'},
                 'width': '10%'},

            ],
            id='my_table'
        ),

        # Footer
        html.Div([
            html.A([
                html.Img(src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", className="footer-logo", title="Python")
            ], href="https://www.python.org/", target="_blank"),
            
            html.A([
                html.Img(src="https://upload.wikimedia.org/wikipedia/commons/2/23/OR-Tools_Logo.png", className="footer-logo", title="Google OR-Tools")
            ], href="https://developers.google.com/optimization", target="_blank"),
            
            html.A([
                html.Img(src=app.get_asset_url('bitsmart_logo.svg'), className="footer-logo bitsmart-logo", title="BitSmart")
            ], href="#", target="_blank"),
        ], className="footer"),

        html.Div([
            "Powered by Python - Created by BitSmart | Alexander Acevedo (2016-2026)"
        ], className="credits")

    ], className="main-container")
])


@callback(
    Output('my_table', 'data'),
    Input('professor_drop', 'value'),
    Input('dia_drop', 'value')
)
def update_dropdown(proff_v, day_v):
    dff = df.copy()
    if proff_v:
        dff = dff[dff.Cedula == proff_v]
        return dff.to_dict('records')
    if day_v:
        dff = dff[dff.Cedula == day_v]
        return dff.to_dict('records')


# un solo return al mismo nivel del if muestra toda la tabla
if __name__ == '__main__':
    app.run(debug=False)