import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import pycountry_convert as pc
from dash import Input, Output, callback, dcc, html

pd.options.mode.chained_assignment = None  # default='warn'
import os

# define scope population
nordic_population = 27.36e6
europe_population = 746.4e6
africa_population = 1.215e9
asia_population = 4.561e9
na_population = 579e6
sa_population = 422.5e6
world_population = 7.387e9
mainDirectory = os.path.dirname(os.path.abspath(__file__))
dataPath = f"{mainDirectory[0:-5]}/data/"
dash.register_page(__name__, path="/whatif")

teemusData = pd.read_excel(
    io=f"{dataPath}/teemusData.xls", sheet_name="Total Greenhouse Gas Emission"
).T
teemusData.columns = teemusData.iloc[0]
teemusData = teemusData[1:]


projectionData = pd.read_csv(f"{dataPath}/GHG_projection.csv")
projectionData.columns = projectionData.columns.str.strip()
layout = html.Div(
    children=[
        dbc.Row(
            [
                html.H1(
                    "Global GHG emissions by scenario", style={"text-align": "center"}
                ),
                dbc.Label("Choose between total emissions, per capita and per GDP"),
                dbc.RadioItems(
                    options=[
                        {"label": "Trend from implemented policies", "value": "7"},
                        {
                            "label": "Limit warming to 2°C (>67%) or return warming to 1.5°C (>50%) after a high overshoot, NDCs until 2030",
                            "value": "4",
                        },
                        {"label": "Limit warming to 2°C (>67%)", "value": "2"},
                        {
                            "label": "Limit warming to 1.5°C (>50%) with no or limited overshoot",
                            "value": "1",
                        },
                    ],
                    value="7",
                    id="projectionVal",
                ),
                dcc.Graph(id="projection"),
                html.Br(),
                dbc.Row(
                [
                dbc.Col(
                            width=0.5, 
                            ),
                dbc.Col(
                    dcc.Markdown(
                                        """
                                        The United Nations has many sub-organizations, and one of them is [The Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch/). 
                                        IPCC is the scientific hub for evaluating climate change and it has many working groups focused on different aspects of climate change. 
                                        Here is the graph by [Working Group III](https://www.ipcc.ch/working-group/wg3/), that illustrates the paths emissions should take to limit global warming to different levels. 
                                        The ultimate goal is to limit global warming to 1.5°C, but according to IPCC this is unlikely with the current policies.
                                """
                                ),
                            ),
                        ],
       
                ),
            ],
        ),
        
 
        dbc.Row(
            [
                html.H1(
                    "Resources for the Future: Carbon pricing calculator",
                    style={"text-align": "center"},
                ),
                dbc.Label("RFF Carbon Pricing Calculator"),
                dbc.RadioItems(
                    options=[
                        {
                            "label": "Annual Emissions",
                            "value": "RFF_Annual_EmissionsL.csv",
                        },
                        {
                            "label": "Cumulative Emissions",
                            "value": "RFF_Cumulative_EmissionsL.csv",
                        },
                        {"label": "Carbon Price", "value": "RFF_Carbon_Price.csv"},
                        {
                            "label": "Annual Revenues",
                            "value": "RFF_Annual_RevenuesL.csv",
                        },
                    ],
                    value="RFF_Annual_EmissionsL.csv",
                    id="RFF_calc_file",
                ),
                dcc.Graph(id="RFF_calc"),
                html.Br(),
                dbc.Row(
                [
                dbc.Col(
                            width=0.5, 
                            ),
                dbc.Col(
                    dcc.Markdown(
                        """
                        Resources for the Future describes themselves as an independent, non-profit research institution situated in Washington, DC. 
                        Their goal is to improve the decision-making process around environmental policy, via research and policy action. 
                        Their Carbon Pricing Calculator is a great way to illustrate how different policies can have an impact on the environment. 
                        Although it is focused on the United States, it considers policy actions that are reproducible in the Nordics too. 
                        These include flat and incremental carbon taxes, with revenue recycling. You can learn more from their website [here](https://www.rff.org/publications/data-tools/carbon-pricing-calculator/).
                        """
                                ),
                            ),
                        ],
       
                ),
            ]
        ),
        
 
        html.Div(
            [
                html.Div(
                    [
                        "What you can do:",
                        dcc.Checklist(
                            [
                                "Decrease car usage by x%",
                            ],
                            id="car_check",
                        ),
                        dcc.Input(type="hidden", id="car_usage", min=0, max=100),
                        dcc.Checklist(
                            [
                                "Cutting down the usage of lights by x%",
                            ],
                            id="lights_check",
                        ),
                        dcc.Input(type="hidden", id="lights_usage", min=0, max=100),
                        dcc.Checklist(
                            [
                                "Take less time in the shower",
                            ],
                            id="shower_check",
                        ),
                        dcc.Input(type="hidden", id="shower_usage", min=0, max=100),
                    ]
                ),
                html.Div(
                    [
                        dcc.RadioItems(
                            [
                                "Just you",
                                "You and your friends",
                                "Nordics",
                                "Europe",
                                "Africa",
                                "Asia",
                                "North America",
                                "South America",
                                "World",
                            ],
                            style={"margin": "6px"},
                            id="reduce_scope",
                        ),
                        html.Div(
                            [
                                html.Div(id="what_scope"),
                                dcc.Input(
                                    type="hidden", id="percentage_of_scope", min=0
                                ),
                            ]
                        ),
                        html.Div(id="my-output"),
                    ]
                ),
            ],
            style={"font-size": "30px", "margin-left": "30%"},
        ),
    ],
)


@callback(Output("car_usage", "type"), Input("car_check", "value"))
def show_input_car(car_check):
    if car_check == None:
        return "hidden"
    elif len(car_check) == 0:
        return "hidden"
    else:
        return "number"


@callback(Output("lights_usage", "type"), Input("lights_check", "value"))
def show_input_lights(lights_check):
    if lights_check == None:
        return "hidden"
    elif len(lights_check) == 0:
        return "hidden"
    else:
        return "number"


@callback(Output("shower_usage", "type"), Input("shower_check", "value"))
def show_input_shower(shower_check):
    if shower_check == None:
        return "hidden"
    elif len(shower_check) == 0:
        return "hidden"
    else:
        return "number"


@callback(
    Output("what_scope", "children"),
    Output("percentage_of_scope", "type"),
    Output("percentage_of_scope", "max"),
    Input("reduce_scope", "value"),
)
def choose_reduce_amount(scope):
    if scope == None or scope == "Just you":
        return None, "hidden", None
    elif scope == "You and your friends":
        return ["How many friends do you have"], "number", None
    else:
        return ["How many percentage of {} will do it ".format(scope)], "number", 100


@callback(
    Output("my-output", "children"),
    Input("car_check", "value"),
    Input("lights_check", "value"),
    Input("shower_check", "value"),
    Input("car_usage", "value"),
    Input("lights_usage", "value"),
    Input("shower_usage", "value"),
    Input("reduce_scope", "value"),
    Input("percentage_of_scope", "value"),
)
def compute_reduced_carbon(c1, c2, c3, u1, u2, u3, scope, percent):
    ans1 = 0
    ans2 = 0
    ans3 = 0
    if c1 != None and len(c1) != 0:
        if u1 != None:
            ans1 = u1 / 100
    if c2 != None and len(c2) != 0:
        if u2 != None:
            ans2 = u2 / 100
    if c3 != None and len(c3) != 0:
        if u3 != None:
            ans3 = u3 / 100
    reduce1 = 0
    reduce2 = 0
    reduce3 = 0
    if scope == "Just you":
        reduce1 = 4.6 * 1e3
        reduce2 = 2529 / 1000
        reduce3 = 2.6 / 1000
    elif scope == "You and your friends":
        if percent != None:
            reduce1 = 4.6 * 1e3 * (percent + 1)
            reduce2 = 2529 / 1000 * (percent + 1)
            reduce3 = 2.6 / 1000 * (percent + 1)
    elif scope == "Nordics":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * nordic_population
            reduce2 = 2529 / 1000 * percent / 100 * nordic_population
            reduce3 = 2.6 / 1000 * percent / 100 * nordic_population
    elif scope == "Europe":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * europe_population
            reduce2 = 2529 / 1000 * percent / 100 * europe_population
            reduce3 = 2.6 / 1000 * percent / 100 * europe_population
    elif scope == "Africa":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * africa_population
            reduce2 = 2529 / 1000 * percent / 100 * africa_population
            reduce3 = 2.6 / 1000 * percent / 100 * africa_population
    elif scope == "Asia":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * asia_population
            reduce2 = 2529 / 1000 * percent / 100 * asia_population
            reduce3 = 2.6 / 1000 * percent / 100 * asia_population
    elif scope == "North America":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * na_population
            reduce2 = 2529 / 1000 * percent / 100 * na_population
            reduce3 = 2.6 / 1000 * percent / 100 * na_population
    elif scope == "South America":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * sa_population
            reduce2 = 2529 / 1000 * percent / 100 * sa_population
            reduce3 = 2.6 / 1000 * percent / 100 * sa_population
    elif scope == "World":
        if percent != None:
            reduce1 = 4.6 * 1e3 * percent / 100 * world_population
            reduce2 = 2529 / 1000 * percent / 100 * world_population
            reduce3 = 2.6 / 1000 * percent / 100 * world_population
    if scope != None:
        return [
            "We can reduce {:,.0f} tonnes of carbon dioxide per year".format(
                reduce1 * ans1 + reduce2 * ans2 + reduce3 * ans3
            )
        ]
    else:
        return []


@callback(Output("projection", "figure"), Input("projectionVal", "value"))
def display_projeciton(proj):
    proMean = projectionData[f"{proj}m"]
    confidenceIntervalLow = projectionData[f"{proj}l"]
    confidenceIntervalHigh = projectionData[f"{proj}h"]
    x = list(projectionData["Year"])
    x_rev = x[::-1]
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x + x_rev,
            y=list(confidenceIntervalLow) + list(proMean)[::-1],
            fill="toself",
            fillcolor="rgba(100,0,0,0.2)",
            line_color="rgba(255,255,255,0)",
            showlegend=False,
            name="95% Confidence level",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x + x_rev,
            y=list(confidenceIntervalHigh) + list(proMean)[::-1],
            fill="toself",
            fillcolor="rgba(0,100,80,0.2)",
            line_color="rgba(255,255,255,0)",
            showlegend=False,
            name="95% Confidence level",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=proMean,
            line_color="rgb(0,100,80)",
            name="Mean",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=confidenceIntervalLow,
            line_color="rgb(200,0,0)",
            name="Lower bound",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=confidenceIntervalHigh,
            line_color="rgb(0,200,160)",
            name="Upper bound",
        )
    )

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor="white",
    )

    fig.update_traces(mode="lines")
    return fig


@callback(Output("RFF_calc", "figure"), Input("RFF_calc_file", "value"))
def display_area(calc_file):
    df = pd.read_csv(f"{dataPath}/{calc_file}")
    fig = px.line(df, x=df["Year"], y=df.columns[2], color=df["Policy"])

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor="white",
    )
    return fig
