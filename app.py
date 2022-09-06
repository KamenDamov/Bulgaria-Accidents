#Imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ALL, State

for_bar = pd.read_csv('for_bar')
for_geo = pd.read_csv('for_geo')
#print(for_bar.columns)
for_bar.rename({
    'Statistical Significance Occurences': 'Statistical Significance Occurrences',
    'Injured': 'Injuries',
    'Occurences': 'Occurrences',
    'sig_star_inj': 'sig_star_injuries',
    'sig_star_occ': 'sig_star_occurrences'
    }, axis = 1, inplace = True)
#print(for_bar.columns)
print(for_geo.columns)
for_geo.rename({
    'Statistical Significance Occurences': 'Statistical Significance Occurrences',
    'sig_star_inj': 'sig_star_injuries',
    'sig_star_occ': 'sig_star_occurrences'
    }, axis = 1, inplace = True)

fig = px.scatter_geo(for_geo, lon='long',\
     lat='lat',\
          hover_name='Области',\
               color = 'Statistical Significance Occurrences',\
                    color_discrete_sequence = ['grey', 'green', 'red'],\
                        scope='europe',\
                            center=dict(lat=42.733883, lon=25.48583),\
                                title = 'Occurrences - Difference between years')
fig.update_layout(
    autosize=True,
    height=600,
    geo=dict(
        center=dict(
            lat=42.733883,
            lon=25.48583
        ),
        scope='europe',
        projection_scale=15
    )
)
fig.update_traces(marker=dict(size=25))

texts = for_bar['sig_star_deaths'].replace(np.nan, '', regex=True).to_numpy().tolist()
print(texts)
fig2 = go.Figure(
    data=[
    go.Bar(name='2020', x=for_bar[for_bar['Year']==2020]['Region'], y=for_bar[for_bar['Year']==2020]['Deaths']),
    go.Bar(name='2021', x=for_bar[for_bar['Year']==2021]['Region'], y=for_bar[for_bar['Year']==2021]['Deaths'])
])
fig2.update_layout(barmode='group',  title = 'Year differences - with statistical significance (p < 0.05)')
fig2.update_traces(texttemplate = texts, hovertext=['Total death difference', 'Percentage death difference'])

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[html.Div(
            style={
                'backgroundColor':'#303030',
                'color':'white',
                'fontFamily': '"Lucida Console", "Courier New"'
            },
            children=[
                #Title
                html.H1(
                    style = {
                        'textAlign': 'center',
                    },
                    children="Car accidents in Bulgaria",
                    className="header-title" 
                ), 
                #Description 
                html.H2(
                    style = {
                        'textAlign': 'center',
                    },
                    children="See the most affected regions for car accidents occurrences, deaths, and injuries",
                    className="header-description", 
                ),
            ],
            className="header",
    ),     

    #Category filter
    html.Div(
            children=[
                html.Div(children = 'Category', 
                        style={'paddingTop':'5px',
                                'fontSize': "20px",
                                'fontFamily': '"Lucida Console", "Courier New"'
                                },
                        className = 'menu-title'),
                dcc.Dropdown(
                    id = 'category-filter',
                    options = [
                        {'label': Category, 'value': Category}
                      for Category in ['Occurrences', 'Deaths', 'Injuries']
                    ], #'Category' is the filter
                    value = "Occurrences",
                    className = 'dropdown', 
                    style={'fontSize': "20px",
                           'textAlign': 'center',
                           'fontFamily': '"Lucida Console", "Courier New", monospace'},
                ),
            ],
            className = 'menu',
    ),
#Adding the world visual
html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'world_chart',
                    figure = fig,
                ),
                style={'width': '100%', 'display': 'inline-block'},
            ),
            html.Div(
            children=dcc.Graph(
                id = 'bar_graph',
                figure = fig2,
            ),
            style={'width': '100%', 'display': 'inline-block'},
        )])      

])

#Callback to activate filters
@app.callback(
    dash.dependencies.Output("world_chart", "figure"),
    dash.dependencies.Output('bar_graph', 'figure'),
    dash.dependencies.Input("category-filter", "value")
)

def update_charts(Category):
    if Category == 'Injuries': 
        fig = px.scatter_geo(for_geo, lon='long',\
        lat='lat',\
            hover_name='Области',\
                color = 'Statistical Significance '+Category, \
                        color_discrete_sequence = ['grey', 'red', 'green'],\
                            scope='europe',\
                                center=dict(lat=42.733883, lon=25.48583),\
                                    title = Category + ' - Difference between years')
        fig.update_layout(
            autosize=True,
            height=600,
            geo=dict(
                center=dict(
                    lat=42.733883,
                    lon=25.48583
                ),
                scope='europe',
                projection_scale=15
            )
        )
        fig.update_traces(marker=dict(size=25))
    else: 
        fig = px.scatter_geo(for_geo, lon='long',\
        lat='lat',\
            hover_name='Области',\
                color = 'Statistical Significance '+Category, \
                        color_discrete_sequence = ['grey', 'green', 'red'],\
                            scope='europe',\
                                center=dict(lat=42.733883, lon=25.48583),\
                                    title = Category + ' - Difference between years')
        fig.update_layout(
            autosize=True,
            height=600,
            geo=dict(
                center=dict(
                    lat=42.733883,
                    lon=25.48583
                ),
                scope='europe',
                projection_scale=15
            )
        )
        fig.update_traces(marker=dict(size=25))

    texts = for_bar['sig_star_'+Category.lower()].replace(np.nan, '', regex=True).to_numpy().tolist()
    print(texts)
    fig2 = go.Figure(
        data=[
        go.Bar(name='2020', x=for_bar[for_bar['Year']==2020]['Region'], y=for_bar[for_bar['Year']==2020][Category]),
        go.Bar(name='2021', x=for_bar[for_bar['Year']==2021]['Region'], y=for_bar[for_bar['Year']==2021][Category])
    ])
    fig2.update_layout(barmode='group',  title = 'Year differences - with statistical significance (p < 0.05)')
    fig2.update_traces(texttemplate = texts)

    return fig, fig2

#Running dashboard
if __name__ == '__main__':
    app.run_server()