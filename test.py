import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
from tensorflow import keras
import csv

app = dash.Dash()

walls = {'Masonry': 229 , 'Concrete': 224, 'Stucco': 222, 'Metal': 226 , 'Tile': 225, 'Fiber Cement': 227, 'Asphalt': 228 , 'Vinyl': 221, 'Wood': 223}
roofs = {'Solar Tiles': 235 , 'Architectural Shingles': 236, 'Slate': 230, 'Plastic Polymer': 232 , 'Clay Tile': 234, 'Wood': 237, 'Concrete Tile': 231 , 'Metal': 233, 'Asphalt': 238}
reader = csv.reader(open('Parcel_Locations.csv', 'r'))
locations = {}
for row in reader:
    k, v = row
    locations[k] = int(v)

app.layout = html.Div([

    html.H1('Sterling Investments, LLC Property Value Calculator', style = { 'textAlign': 'center'}),

    html.Hr(),

    html.H2('Insert Property Features',  style = { 'textAlign': 'center'}),
    html.Hr(),
    html.Table(
        [ html.Tr([html.Td(html.Label('Square Feet')), html.Td(dcc.Input(id='input-1',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Bedrooms')), html.Td(dcc.Input(id='input-7',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Bathrooms')), html.Td(dcc.Input(id='input-5',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Stories')), html.Td(dcc.Input(id='input-6',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Garage Capacity')), html.Td(dcc.Input(id='input-3',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Number of Patios')), html.Td(dcc.Input(id='input-4',type='number', value='')) ]),
          html.Tr([html.Td(html.Label('Pool Size (Sqft, 0 if no pool)')), html.Td(dcc.Input(id='input-2',type='number', value='')) ]),


          html.Tr([html.Td(html.Label('Exterior Wall Type')), html.Td(dcc.Dropdown(
        id='dropdown-1',
        options=[{'label': wall, 'value': type} for wall, type in walls.items()], value=''))]),
          html.Tr([html.Td(html.Label('Roof Type')), html.Td(dcc.Dropdown(
        id='dropdown-2',
        options=[{'label': roof, 'value': type} for roof, type in roofs.items()], value=''))]),
          html.Tr([html.Td(html.Label('Location')), html.Td(dcc.Dropdown(
        id='dropdown-3',
        options=[{'label': location, 'value': index} for location, index in locations.items()], value=''))])

          ],


        style = { 'marginLeft': '40%', 'marginRight': '25%'} ),



    html.Hr(),
    html.Button('Submit', id='button-2',  style = { 'marginLeft': '48%', 'marginRight': '25%'}),
    html.Hr(),
    html.Table([html.Tr([html.Td(html.Label(' House Price:')), html.Td(html.Div(id='output'))])], style={ 'marginLeft': '45%', 'marginRight': '25%'}),

])





@app.callback(
    Output('output', 'children'),
    [Input('button-2', 'n_clicks')],
    state=[State('input-1', 'value'),
     State('input-2', 'value'),
     State('input-3', 'value'),
     State('input-4', 'value'),
     State('input-5', 'value'),
     State('input-6', 'value'),
     State('input-7', 'value'),
     State('dropdown-1', 'value'),
     State('dropdown-2', 'value'),
     State('dropdown-3', 'value'),
           ])


def compute(n_clicks, input1, input2, input3, input4, input5, input6, input7, walls, roofs, location):
    model = keras.models.load_model('keras_model')
    test = np.zeros(239)
    test[0] = int(input1)
    test[1] = int(input2)
    test[2] = int(input3)
    test[3] = int(input4)
    test[4] = int(input5)
    test[5] = int(input6)
    test[6] = int(input7)
    test[walls] = 1
    test[roofs] = 1
    test[location] = 1
    predict = model.predict([[test]])
    return '$' + str(predict[0][0])


if __name__ == '__main__':

    app.run_server(port=80)