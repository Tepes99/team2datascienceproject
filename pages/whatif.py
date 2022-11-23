import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import pycountry_convert as pc
from dash import Input, Output, callback, dcc, html
from statsmodels.tsa.arima.model import ARIMA

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

# Daniels prediction
co2_data = pd.read_excel(
    io=f"{dataPath}/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx",
    sheet_name="fossil_CO2_totals_by_country",
)
co2_data = co2_data[co2_data["Country"] == "GLOBAL TOTAL"]
co2_data.drop(columns=["Country", "EDGAR Country Code", "Substance"], inplace=True)
co2_data.reset_index(drop=True, inplace=True)
co2_data["id"] = 0

co2_data = pd.melt(
    co2_data, id_vars="id", var_name="Year", value_name="Realized CO2 [Mt/year]"
)
co2_data.drop(columns=["id"], inplace=True)
co2_data.set_index("Year", inplace=True)

# super simple once-differenced AR model (with drift i.e., constant term c)
model = ARIMA(co2_data, order=(1, 1, 0), trend="t")
result = model.fit()
# predict 5 years out
mat_pred = result.get_prediction(start=1, end=56)
# default plots by statsmodels in matplotlib WHICH DONT FUCKING WORK WITH DASH!!!
pred_df = mat_pred.summary_frame()
pred_df.drop(columns=["mean_se"], inplace=True)
pred_df.columns = ["Predicted CO2 [Mt/year]", "Lower CI (95%)", "Higher CI (95%)"]
pred_df.loc[-1] = [None, None, None]
pred_df.index = pred_df.index + 1
pred_df = pred_df.sort_index()
pred_df["Year"] = [year for year in range(1970, 2027)]
pred_df.set_index("Year", inplace=True)
# hardcode future years into og timeseries
co2_data.loc[2022] = [None]
co2_data.loc[2023] = [None]
co2_data.loc[2024] = [None]
co2_data.loc[2025] = [None]
co2_data.loc[2026] = [None]

shitos = pd.concat([co2_data, pred_df], axis=1)
shitos = shitos.drop([year for year in range(1970, 1990)])

# print(shitos)

prediction_plot = go.Figure(
    [
        go.Scatter(
            name="Predicted",
            x=shitos.index,
            y=shitos["Predicted CO2 [Mt/year]"],
            mode="lines",
            line=dict(color="rgb(31,119,180)"),
        ),
        go.Scatter(
            name="Upper CI",
            x=shitos.index,
            y=shitos["Higher CI (95%)"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
        ),
        go.Scatter(
            name="Lower CI",
            x=shitos.index,
            y=shitos["Lower CI (95%)"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(
                width=0,
            ),
            fillcolor="rgba(68,68,68,0.3)",
            fill="tonexty",
        ),
        go.Scatter(
            name="Realized",
            x=shitos.index,
            y=shitos["Realized CO2 [Mt/year]"],
            mode="lines",
            line=dict(color="rgb(250,150,20)"),
        ),
    ]
)

prediction_plot.update_layout(
    xaxis_title="Year",
    yaxis_title="CO2 emissions [Mt CO2/year]",
    hovermode="x",
    template="none",
)


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
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Quiz", href="/..")),
                        dbc.NavItem(dbc.NavLink("Home", href="graphs")),
                        dbc.NavItem(dbc.NavLink("Future", href="#")),
                        dbc.NavItem(
                            dbc.NavLink(
                                "GitHub",
                                href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master",
                            )
                        ),
                    ],
                    brand="Home",
                    brand_href="graphs",
                    color="primary",
                    dark=True,
                ),
                dbc.Row(
                    [
                        html.H1(
                            "Global CO2 emissions 5 year forecast",
                            style={"margin-top": "5%", "text-align": "center"},
                        ),
                        dcc.Graph(
                            id="emissions_forecast",
                            figure=prediction_plot,
                            style={"margin-left": "2%"},
                        ),
                        dcc.Markdown(
                            """
                    The above graph provides a simple ARIMA(1,1,0) predictive model for global CO2 emissions timeseries. The grey area inidcates a confidence interval of 95%. As typical for a simple ARIMA forecast, the future predicted values quickly regress to the mean. The graph still provides some insight to how we can expect the trend to develop if emission remain as they have been in the past without much changes. Both the models predicted values for previous timepoints and the 5 year forecast are given to demonstrate the decent behaviour of the fitted model.
                    """,
                            style={"margin": "2%"},
                        ),
                    ],
                ),
                html.H1(
                    "Global GHG emissions by scenario",
                    style={"text-align": "center"},
                ),
                dcc.Markdown(
                    """
                    Similar to our projection, IPCC expects Global GHG emissions in 2030 associated with the implementation of Nationally Determined 
                    Contributions (NDCs) announced before 26th UN Climate Change Conference to result global warming to exceed 1.5°C """,
                    style={"margin": "2%"},
                ),
                dbc.RadioItems(
                    options=[
                        {"label": "Trend from implemented policies", "value": "7"},
                        {
                            "label": "Limit warming to 2°C (>67%) or return warming to 1.5°C (>50%) after a high overshoot in temperature, NDCs until 2030",
                            "value": "4",
                        },
                        {"label": "Limit warming to 2°C (>67%)", "value": "2"},
                        {
                            "label": "Limit warming to 1.5°C (>50%) with no or limited overshoot in temperature",
                            "value": "1",
                        },
                    ],
                    value="7",
                    id="projectionVal",
                    style={"margin": "2%"},
                ),
                dcc.Graph(id="projection"),
                dcc.Markdown(
                    """
                    The United Nations has many sub-organizations, and one of them is [The Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch/). 
                    IPCC is the scientific hub for evaluating climate change and it has many working groups focused on different aspects of climate change. 
                    Here is the graph by [Working Group III](https://www.ipcc.ch/working-group/wg3/), that illustrates the paths emissions should take to limit global warming to different levels. 
                    The ultimate goal is to limit global warming to 1.5°C, but according to IPCC this is unlikely with the current policies.
                """,
                    style={
                        "width": "100%",
                        "display": "flex",
                        "textAlign": "left",
                        "margin": "2%",
                        "justify-content": "center",
                    },
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        "What you can do:",
                        dcc.Checklist(
                            [
                                "How long will you drive daily in minutes",
                            ],
                            id="car_check",
                        ),
                        dcc.Input(id="car_usage", min=0, max=100, value=5),
                        dcc.Checklist(
                            [
                                "Cutting down electricity usage by x%",
                            ],
                            id="lights_check",
                        ),
                        dcc.Input(type="hidden", id="lights_usage", min=0, max=100),
                        dcc.Checklist(
                            [
                                "You will shower for x minutes",
                            ],
                            id="shower_check",
                        ),
                        dcc.Input(type="hidden", id="shower_usage", min=0, max=100),
                    ],
                    style={"margin": "2%"},
                ),
                dbc.Col(
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
                            style={"margin": "6px", "margin-top": "20px"},
                            id="reduce_scope",
                            value="Just you",
                        ),
                        html.Div(
                            [
                                html.Div(id="what_scope"),
                                dcc.Input(
                                    type="hidden", id="percentage_of_scope", min=0
                                ),
                            ]
                        ),
                    ],
                ),
            ],
            style={"font-size": "30px"},
        ),
        dbc.Row(
            dbc.Col(
                [html.Div(id="my-output")],
            )
        ),
        dcc.Markdown("""
        Following sources were used for calculations:

        [Countries by number of households](https://en.wikipedia.org/wiki/List_of_countries_by_number_of_households)

        [Home electricity consumption](https://www.vaasansahko.fi/en/energy-tips/electricity-consumption-at-your-home-what-does-it-consist-of/)

        [Average daily driving time](https://newsroom.aaa.com/2016/09/americans-spend-average-17600-minutes-driving-year/)
        """, style={"margin":"2%"}),
        
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Quiz", href="/..")),
                dbc.NavItem(dbc.NavLink("Home", href="graphs")),
                dbc.NavItem(dbc.NavLink("Future", href="#")),
                dbc.NavItem(
                    dbc.NavLink(
                        "GitHub",
                        href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master",
                    )
                ),
            ],
            brand="Up",
            brand_href="#",
            color="primary",
            dark=True,
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
            ans1 = 48 - u1
    if c2 != None and len(c2) != 0:
        if u2 != None:
            ans2 = u2 / 100
    if c3 != None and len(c3) != 0:
        if u3 != None:
            ans3 = 13 - u3
    reduce1 = (4.6 * 10e3) / 48
    reduce2 = 10632 * 0.527
    reduce3 = 2.6 / 13 * 365
    if scope == "You and your friends":
        if percent != None:
            reduce1 = reduce1 * (percent + 1)
            reduce2 = reduce2 * (percent + 1)
            reduce3 = reduce3 * (percent + 1)
    elif scope == "Nordics":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * nordic_population
            reduce2 = reduce2 * percent / 100 * nordic_population
            reduce3 = reduce3 * percent / 100 * nordic_population
    elif scope == "Europe":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * europe_population
            reduce2 = reduce2 * percent / 100 * europe_population
            reduce3 = reduce3 * percent / 100 * europe_population
    elif scope == "Africa":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * africa_population
            reduce2 = reduce2 * percent / 100 * africa_population
            reduce3 = reduce3 * percent / 100 * africa_population
    elif scope == "Asia":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * asia_population
            reduce2 = reduce2 * percent / 100 * asia_population
            reduce3 = reduce3 * percent / 100 * asia_population
    elif scope == "North America":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * na_population
            reduce2 = reduce2 * percent / 100 * na_population
            reduce3 = reduce3 * percent / 100 * na_population
    elif scope == "South America":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * sa_population
            reduce2 = reduce2 * percent / 100 * sa_population
            reduce3 = reduce3 * percent / 100 * sa_population
    elif scope == "World":
        if percent != None:
            reduce1 = reduce1 * percent / 100 * world_population
            reduce2 = reduce2 * percent / 100 * world_population
            reduce3 = reduce3 * percent / 100 * world_population
    if scope == "Just you" or scope == "You and your friends":
        message = "We can reduce {:,.0f} kgs  of carbon dioxide per year".format(
            reduce1 * ans1 + reduce2 * ans2 + reduce3 * ans3
        )
    else:
        if percent == None:
            message = " "
        else:
            message = "We can reduce {:,.0f} tonnes of carbon dioxide per year".format(
                reduce1 * ans1 / 1000 + reduce2 * ans2 / 1000 + reduce3 * ans3 / 1000
            )
    if scope != None:
        return dcc.Markdown(
            """ 
        ## {}
        """.format(
                message
            ),
            style={"margin": "2%", "margin-bottom": "5vh"},
        )
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
        xaxis_title="Year",
        yaxis_title="Billion metric tons",
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
        legend_orientation="h",
        plot_bgcolor="white",
    )

    fig.update_traces(mode="lines")
    return fig
