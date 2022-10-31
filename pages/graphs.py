import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pycountry
import numpy as np
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
from dash import Input, Output, callback, dcc, html

pd.options.mode.chained_assignment = None  # default='warn'
import os

mainDirectory = os.path.dirname(os.path.abspath(__file__))
dataPath = f"{mainDirectory[0:-5]}/data/"

dash.register_page(__name__, path="/graphs")
path = f"{dataPath}/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"
# Daniel graph
df_co2_by_sector = pd.read_csv(f"{dataPath}CO2_by_sector_and_country.csv")
daniel_scope = sorted([*set(df_co2_by_sector["Country"])])
daniel_scope.append("Global emissions")  # selectable countries + GLOBAL VIEW
df_co2_by_sector.fillna(0, inplace=True)  # replace unreported emissions with 0

#  Hieu graph

df_CO2_country = pd.read_excel(io='data/CO2_by_capita.xlsx', sheet_name="fossil_CO2_per_capita_by_countr")
##remove EU27 and global emission
df_CO2_country = df_CO2_country.drop([210, 211, 212])
nordic_countries = [
    "Denmark",
    "Finland",
    "Iceland",
    "Norway",
    "Sweden",
    "Greenland",
    "Faroes",
]

# Convert country name into continent name


def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(
            country_continent_code
        )
    except:
        return "Unspecified"
    return country_continent_name


df_CO2_country["Continent"] = df_CO2_country["Country"].apply(
    lambda x: country_to_continent(x)
)

region = [
    {"label": c, "value": c}
    for c in [
        "World",
        "Asia",
        "Africa",
        "Europe",
        "North America",
        "Nordic",
        "Oceania",
        "South America",
    ]
]


# Linh graph
df_co2_change = pd.read_csv(f"{dataPath}co2_by_country.csv")
scope = list(df_co2_change["Country"].unique())


df_GDP = pd.read_csv(
    f"{dataPath}/GDP_by_country_current_international_dollar.csv",
)


# Selins graph

# Preprocessing
df_PaM = pd.read_csv(f"{dataPath}/PaM_number.csv")

# Teemus graph
teemusData = pd.read_excel(
    io=f"{dataPath}/teemusData.xls", sheet_name="Total Greenhouse Gas Emission"
).T
teemusData.columns = teemusData.iloc[0]
teemusData = teemusData[1:]


projectionData = pd.read_csv(f"{dataPath}/GHG_projection.csv")
projectionData.columns = projectionData.columns.str.strip()

#############################
#     Start of the page     #
#############################

layout = html.Div(
    children=[
        dbc.Row(
            [
                html.Div(
                    children="""
        This is our Home page content.
    """
                ),
                html.Div(
                    [
                        "How many friends do you have: ",
                        dcc.Input(id="my-input", value="", type="number"),
                    ]
                ),
                html.Div(
                    [
                        "What you can do:",
                        dcc.Checklist(
                            [
                                "Walk/cycle to work",
                                "Use better energy home appliance",
                                "Cook more at home to reduce food waste",
                            ],
                            [],
                            id="activities",
                        ),
                    ]
                ),
                html.Br(),
                html.Div(id="my-output"),
            ],
            style={"textAlign": "center", "fontSize": 30},
        ),
        dbc.Row(
            [
                dbc.Row(
                    [
                        html.H1(
                            "CO2 emissions by sector", style={"text-align": "center"}
                        ),
                        html.Div(
                            children=[
                                html.H3("Select scope:"),
                                dcc.Dropdown(
                                    id="daniel_scope",
                                    options=daniel_scope,
                                    multi=False,
                                    value="Global emissions",
                                ),
                            ]
                        ),
                        html.Br(),
                        dcc.Graph(id="sector_emissions_graph", style={}),
                        html.Br(),
                    ],
                    style={"order": 2},
                ),
                dbc.Row(
                    [
                        html.H1('CO2 emission per capita', style = {'text-align':'center'}),

                        html.Div(
                            children = [
                            html.H3('Choose a region:'),
                            ],
                            style={'width': '100%'}
                        ),
                        dcc.RadioItems(id = 'region',
                                        options=region,
                                        value = 'World',
                                        inline=False, 
                                        # style={'margin-left':'50px'},
                                        labelStyle={'display': 'inline-block', 'margin-right':'15px'}, # block for column, inline-block for line
                                        ),
                        html.Br(),
                        dcc.Graph(id = 'co2_graph', figure = {}, style = {'margin-left':'10px'}),
                        html.Br(),
                        html.Div(
                            children = 
                                [dcc.Slider(min = 1970, 
                                            max = 2021, 
                                            step = 1, 
                                            value = 2021, 
                                            marks=None,
                                            tooltip={"placement": "bottom", "always_visible": False}, 
                                            id = 'year_slider')],
                            style = {'width': '50%', 'margin-left':'440px'}
                        ),
                        html.Div(id = 'output_container', children = [], style={'text-align':'center', 'font-size':'25px'})
                                    ],
                    style={
                        "order": 1,
                    },
                ),
                dbc.Row(
                    [
                        html.H1(
                            "Changes in CO2 emissions and GDP",
                            style={"text-align": "center"},
                        ),
                        html.Div(
                            children=[
                                html.H3("Select scope:"),
                                dcc.Dropdown(
                                    id="scope",
                                    options=scope,
                                    multi=False,
                                    value="Finland",
                                ),
                            ],
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="C02_change_emissions_graph",
                            style={},
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                html.H3("Select year:"),
                                dcc.RangeSlider(
                                    min=1990,
                                    max=2021,
                                    step=1,
                                    value=[2000, 2021],
                                    marks={
                                        1990: "1990",
                                        1995: "1995",
                                        2000: "2000",
                                        2005: "2005",
                                        2010: "2010",
                                        2015: "2015",
                                        2021: "2021",
                                    },
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                    id="my-range-slider",
                                ),
                            ]
                        ),
                    ],
                    style={"order": 3},
                ),
                dbc.Row(
                    [
                        html.H1(
                            "Number of Policies and measurements by Sector",
                            style={"text-align": "center"},
                        ),
                        html.P("Select the Sector"),
                        dcc.Dropdown(
                            id="sector",
                            options=[
                                "Total",
                                "Energy",
                                "Waste",
                                "Transportation",
                                "Industry",
                                "Agriculture & Land",
                                "Other",
                            ],
                            multi=False,
                            value="Total",
                        ),
                        dcc.Graph(id="selinsGraph"),
                    ],
                    style={"order": 4},
                ),
                dbc.Row(
                    [
                        html.H1("Emissions by country", style={"text-align": "center"}),
                        dbc.Label(
                            "Choose between total emissions, per capita and per GDP"
                        ),
                        dbc.RadioItems(
                            options=[
                                {
                                    "label": "Total CO2 Emission",
                                    "value": "Total CO2 Emission",
                                },
                                {
                                    "label": "CO2 Emissions Per Capita",
                                    "value": "CO2 Emissions Per Capita",
                                },
                                {
                                    "label": "CO2 Emissions Per GDP",
                                    "value": "CO2 Emissions Per GDP",
                                },
                                {
                                    "label": "Total Greenhouse Gas Emission",
                                    "value": "Total Greenhouse Gas Emission",
                                },
                                {
                                    "label": "Greenhouse Gas Emissions Per Capita",
                                    "value": "Greenhouse Emissions Per Capita",
                                },
                                {
                                    "label": "Greenhouse Gas Emissions Per GDP",
                                    "value": "Greenhouse Emissions Per GDP",
                                },
                            ],
                            value="Total Greenhouse Gas Emission",
                            id="sheet",
                        ),
                        html.P("Select country:"),
                        dcc.Dropdown(
                            id="y-axis",
                            options=list(teemusData.columns.values),
                            value="Afghanistan",
                        ),
                        dcc.Graph(id="teemusGraph"),
                    ],
                    style={"order": 4},
                ),
            ],
            style={"display": "flex", "flex-direction": "column"},
        ),
         
        html.Div(
            [
                html.H1("Global GHG emissions by scenario", 
                style={"text-align": "center"}),
                
                dbc.Label("Choose between total emissions, per capita and per GDP"),
                dbc.RadioItems(
                    options=[
                        {"label": "Trend from implemented policies","value": "7"},
                        {"label": "Limit warming to 2°C (>67%) or return warming to 1.5°C (>50%) after a high overshoot, NDCs until 2030","value": "4"},
                        {"label": "Limit warming to 2°C (>67%)", "value": "2"},
                        {"label": "Limit warming to 2°C (>67%)","value": "1"},
                    ],
                        value="7",
                        id="projectionVal",
                ),
                dcc.Graph(id="projection")

            ]
        ),
    ],
)


@callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="my-input", component_property="value"),
    Input("activities", "value"),
    prevent_initial_call=True,
)
def update_output_div(input_value, activities):
    if len(activities) == 0 or input_value is None:
        ans = 0
        return ""
    else:
        ans = input_value * len(activities)
        return html.H1(
            "You can reduce {} tons carbon emission by 2050".format(ans),
            style={"margin-left": "35%", "margin-right": "30%", "color": "red"},
        )


@callback(Output("sector_emissions_graph", "figure"), Input("daniel_scope", "value"))
def update_graph_co2_by_sector(selection):
    data = df_co2_by_sector.copy()
    if selection == "Global emissions":
        data.drop(columns=["Country"], inplace=True)  # not needed on global scope
        data = data.groupby(
            "Sector", as_index=False
        ).sum()  # group by sector, aggregate by summing yearly emissions
        data.columns = data.columns.astype(
            str
        )  # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(
            data,
            id_vars="Sector",
            value_vars=data.columns,
            var_name="Year",
            value_name="CO2 emissions",
            ignore_index=True,
        )
        fig = px.area(
            data, x="Year", y="CO2 emissions", color="Sector", template="none"
        )
    else:
        # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
        # produces a series when it produces a dataframe. Works when running so no problem
        data = data[data["Country"] == selection]  # select country data
        data.drop(columns=["Country"], inplace=True)
        data.columns = data.columns.astype(
            str
        )  # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(
            data,
            id_vars="Sector",
            value_vars=data.columns[1:],
            var_name="Year",
            value_name="CO2 emissions",
            ignore_index=True,
        )
        fig = px.area(
            data, x="Year", y="CO2 emissions", color="Sector", template="none"
        )
    fig.update_layout(legend={"orientation": "h", "y": -0.4})
    return fig


@callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="co2_graph", component_property="figure"),
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year_slider", component_property="value"),
    ],
)
def update_graph_co2_by_region(
    region_slctd, year_slctd
):  # number of arguments is the same as the number of inputs

    container = " CO2 emission per capita in {}".format(year_slctd)

    if region_slctd == "World":
        df_CO2 = df_CO2_country.copy()

    elif region_slctd == "Nordic":
        df_CO2 = df_CO2_country[df_CO2_country["Country"].isin(nordic_countries)]

    else:
        df_CO2 = df_CO2_country[df_CO2_country["Continent"] == region_slctd]

    df_CO2 = df_CO2[["Country", year_slctd]]
    df_CO2[year_slctd] = np.round(df_CO2[year_slctd], 3)

    fig = px.choropleth(
        data_frame=df_CO2,
        locationmode='country names',
        locations= 'Country',
        color= year_slctd,
        range_color=[0, 20],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        hover_data={'Country': False},
        labels={str(year_slctd): 'CO2 emission per capita'},
        hover_name='Country',
        basemap_visible=True,
        # center = center_dict[region_slctd]
    )
    fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True),
        #     height=400,
    )
    fig.update_coloraxes(colorbar_orientation="h", colorbar_y=1)
    return container, fig


@callback(
    Output("C02_change_emissions_graph", "figure"),
    Input("scope", "value"),
    [Input("my-range-slider", "value")],
)
def update_graph_co2_vs_gdp_change(scope_selected, years_selected):
    data = df_co2_change.copy()
    data1 = df_GDP.copy()
    ###
    data = data[data["Country"] == scope_selected]
    data.columns = data.columns.astype(str)
    data = pd.melt(
        data,
        id_vars="Country",
        value_vars=data.columns[1:],
        var_name="Year",
        value_name="Change",
        ignore_index=True,
    )
    data["Year"] = data["Year"].astype("int")
    data = data[
        (data["Year"] >= years_selected[0]) & (data["Year"] <= years_selected[1])
    ]
    data.drop(columns=["Country"], inplace=True)
    data.iloc[:, 1] = data.iloc[:, 1].apply(
        lambda row: (((row - data.iloc[0, 1]) / data.iloc[0, 1]))
    )
    data["Metric"] = "CO2"

    ###
    data1 = data1[data1["Country Name"] == scope_selected]
    data1.columns = data1.columns.astype(str)
    data1 = pd.melt(
        data1,
        id_vars="Country Name",
        value_vars=data1.columns[1:],
        var_name="Year",
        value_name="Change",
        ignore_index=True,
    )
    data1["Year"] = data1["Year"].astype("int")
    data1 = data1[
        (data1["Year"] >= years_selected[0]) & (data1["Year"] <= years_selected[1])
    ]
    data1.drop(columns=["Country Name"], inplace=True)
    data1.iloc[:, 1] = data1.iloc[:, 1].apply(
        lambda row: (((row - data1.iloc[0, 1]) / data1.iloc[0, 1]))
    )
    data1["Metric"] = "GDP"

    df = pd.concat([data, data1.loc[:]]).reset_index(drop=True)
    fig = px.line(df, x="Year", y="Change", color="Metric", template="none")
    fig.layout.yaxis.tickformat = ",.1%"

    return fig


@callback(Output("selinsGraph", "figure"), Input("sector", "value"))
def display_choropleth(sector):
    df_use = df_PaM  # replace with your own data source
    fig = px.choropleth(
        df_use,
        color=sector,
        locations="code",
        projection="mercator",
        scope="europe",
        hover_name="Country",
        color_continuous_scale="Viridis",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(colorbar_orientation="h", colorbar_y=1)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@callback(
    Output("teemusGraph", "figure"), Input("sheet", "value"), Input("y-axis", "value")
)
def display_area(sheet, y):
    df = pd.read_excel(io=f"{dataPath}/teemusData.xls", sheet_name=sheet).T
    df.columns = df.iloc[0]
    df = df[1:]
    fig = px.area(df, x=df.index, y=y)
    return fig


@callback(
    Output("projection", "figure"),
    Input("projectionVal", "value"))
def display_projeciton(proj):
    proMean = projectionData[f"{proj}m"]
    confidenceIntervalLow = projectionData[f"{proj}l"]
    confidenceIntervalHigh = projectionData[f"{proj}h"]
    x = list(projectionData["Year"])
    x_rev = x[::-1]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x= x+x_rev,
        y=list(confidenceIntervalLow)+list(proMean)[::-1],
        fill='toself',
        fillcolor='rgba(100,0,0,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name= '95% Confidence level',
    ))

    fig.add_trace(go.Scatter(
        x= x+x_rev,
        y=list(confidenceIntervalHigh)+list(proMean)[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name= '95% Confidence level',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=proMean,
        line_color='rgb(0,100,80)',
        name='Mean',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=confidenceIntervalLow,
        line_color='rgb(200,0,0)',
        name='Lower bound',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=confidenceIntervalHigh,
        line_color='rgb(0,200,160)',
        name='Upper bound',
    ))

    fig.update_traces(mode='lines')
    return fig
    