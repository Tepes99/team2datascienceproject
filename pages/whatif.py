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
        html.Div(
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
                        {"label": "Limit warming to 1.5°C (>50%) with no or limited overshoot", "value": "1"},
                    ],
                    value="7",
                    id="projectionVal",
                ),
                dcc.Graph(id="projection"),
            ],
        ),
        html.Div(
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
            ]
        ),
    ],
)


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
        autosize=False,
        margin=dict(
            autoexpand=False,
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
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor="white",
    )
    return fig
