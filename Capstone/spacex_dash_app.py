# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

options = [{'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
            ]
# Create a dash application
app = dash.Dash("SpaceX Dash Application")

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 48}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=options,
                                             value = "ALL",
                                             placeholder="Select A Site",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max =10000, step=1000, 
                                                marks={0:"0", 2500:"2500", 5000:"5000", 7500:"7500", 10000:"10000"}, 
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    # filtered_df = spacex_df
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, names='Launch Site', title='Success Rate for All Launch Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df["class"] = filtered_df["class"].astype(str)
        fig = px.pie(filtered_df, names='class', title=f'Success Rate for {entered_site}', labels=['Failed', 'Successful'], color_discrete_map={"0": "#EF5350", "1": "#187bcd"}, color="class")
        return fig  
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value'))


def get_scatter_plot(entered_site, slider_values):
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= slider_values[0]) & (spacex_df["Payload Mass (kg)"] <= slider_values[1])]
    if entered_site == 'ALL':
        # filtered_df = spacex_df
        fig = px.scatter(filtered_df, title='Correlation between Payload and Mission Outcome for All Sites', x="Payload Mass (kg)", y="class",  color='Launch Site')
        fig.update_layout(yaxis=dict(range=[-0.1, 1.1], tickvals=[0, 1]))
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df["class"] = filtered_df["class"].astype(str)
        fig = px.scatter(filtered_df, title=f'Correlation between Payload and Mission Outcome for {entered_site}', x="Payload Mass (kg)", y="class", color="class", color_discrete_map={"0": "#EF5350", "1": "#187bcd"})
        fig.update_layout(yaxis=dict(range=[-0.1, 1.1] ,tickvals=[0, 1]))
        return fig  

# Run the app
if __name__ == '__main__':
    app.run_server()
