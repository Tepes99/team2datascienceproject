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

dash.register_page(__name__, path="/graphs")
path = f"{dataPath}/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"


### Daniel graph

# PREPROCESSING ETC => Rather not do this every update so perform here
sector_data = pd.read_excel(io=f"{path}", sheet_name="fossil_CO2_by_sector_and_countr")
sector_data.drop(columns=["Substance"], inplace=True)  # drop unnecessary columns
choices = sorted([*set(sector_data["Country"])])
choices.append("Global emissions")  # selectable countries + GLOBAL VIEW

pop_data = pd.read_csv(
    f"{dataPath}API_SP.POP.TOTL_DS2_en_csv_v2_4685015.csv", skiprows=4
)

drop_years = [str(y) for y in range(1960, 1970)]  # more than necessary population data
drop_cols = drop_years + [
    "Country Name",
    "Indicator Name",
    "Indicator Code",
    "Unnamed: 66",
]
pop_data.drop(columns=drop_cols, inplace=True)  # drop unnecessary cols

# computing total populations per year (from our underlying data rather than external source to
# maintain consistancy with ratios)
pop_totals = pop_data.copy()
pop_totals = pop_totals[
    pop_totals["Country Code"].isin([*set(sector_data["EDGAR Country Code"])])
]
pop_totals.drop(columns=["Country Code"], inplace=True)
pop_totals = pop_totals.sum()  # series of total populations per year

sector_per_capita = sector_data.copy()  # we build the emissions/sector/capita into this

# The global scope
global_sector_per_capita = sector_data.copy()
global_sector_per_capita.drop(
    columns=["Country", "EDGAR Country Code"], inplace=True
)  # not needed on global scope
global_sector_per_capita = global_sector_per_capita.groupby(
    "Sector", as_index=False
).sum()  # group by sector, aggregate by summing yearly emissions
global_sector_per_capita.columns = global_sector_per_capita.columns.astype(
    str
)  # change names to string to ensure sound processing

years = range(1970, 2022)

# dividing the earlier aggregated total co2 by population
for row in global_sector_per_capita.itertuples():
    for year in years:
        pop = pop_totals[str(year)]
        co2 = global_sector_per_capita.at[row.Index, str(year)]
        global_sector_per_capita.at[row.Index, str(year)] = (
            10**6 * co2 / pop
        )  # convert from Mt => t

# same as above but country specific
for row in sector_per_capita.itertuples():
    country = row._2
    pop_ts = pop_data[pop_data["Country Code"] == country]
    if not pop_ts.empty:
        pop_ts.reset_index(drop=True, inplace=True)
        for year in years:
            pop = pop_ts.at[0, str(year)]
            co2 = sector_per_capita.at[row.Index, year]
            sector_per_capita.at[row.Index, year] = (
                10**6 * co2 / pop
            )  # convert from Mt => t


###  Hieu graph

df_CO2_country = pd.read_excel(
    io="data/CO2_by_capita.xlsx", sheet_name="fossil_CO2_per_capita_by_countr"
)
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

# Hard code spain
df_CO2_country.loc[df_CO2_country['EDGAR Country Code'] == 'ESP', 'Country'] = 'Spain'

df_CO2_country["Continent"] = df_CO2_country["Country"].apply(
    lambda x: country_to_continent(x)
)

# Hard code france
df_CO2_country.loc[df_CO2_country['EDGAR Country Code'] == 'FRA', 'Continent'] = 'Europe'


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


##### Linh graph

# CO2 per capita
df_CO2_capita = pd.read_excel(f"{dataPath}CO2_by_capita.xlsx")
df_CO2_capita = df_CO2_capita.drop(columns=["Substance", "EDGAR Country Code"])
scope = list(df_CO2_capita["Country"].unique())
df_CO2_capita = pd.melt(
    df_CO2_capita,
    id_vars="Country",
    value_vars=df_CO2_capita.columns[1:],
    var_name="Year",
    value_name="CO2_per_capita",
)
df_CO2_capita["Year"] = df_CO2_capita["Year"].astype("int")
df_CO2_capita["Country"] = df_CO2_capita["Country"].astype("string")

# GDP per capita
df_GDP_capita = pd.read_excel(f"{dataPath}GDP_per_capita.xlsx", skiprows=3)
df_GDP_capita = df_GDP_capita.drop(columns=df_GDP_capita.columns[1:34])
df_GDP_capita = df_GDP_capita.rename(columns={"Country Name": "Country"})
df_GDP_capita = pd.melt(
    df_GDP_capita,
    id_vars="Country",
    value_vars=df_GDP_capita.columns[1:],
    var_name="Year",
    value_name="GDP_per_capita",
)
df_GDP_capita["Year"] = df_GDP_capita["Year"].astype("int")
df_GDP_capita["Country"] = df_GDP_capita["Country"].astype("string")

# Population
df_population = pd.read_csv(f"{dataPath}population.csv", skiprows=4)
df_population = df_population.drop(columns=df_population.columns[1:4])
df_population = df_population.drop(columns=df_population.columns[-1])
df_population = df_population.rename(columns={"Country Name": "Country"})
df_population = pd.melt(
    df_population,
    id_vars="Country",
    value_vars=df_population.columns[1:],
    var_name="Year",
    value_name="Population",
)
df_population["Year"] = df_population["Year"].astype("int")
df_population["Country"] = df_population["Country"].astype("string")
df_population = df_population.dropna()

# Final dataset
df = pd.merge(df_CO2_capita, df_GDP_capita, on=["Country", "Year"], how="inner")
df = pd.merge(df, df_population, on=["Country", "Year"], how="inner")
df["Continent"] = df["Country"].apply(lambda x: country_to_continent(x))

# Add Nordics into data sets
df_nordics = df[df["Country"].isin(nordic_countries)]
df_nordics["Continent"] = "Nordics"
df = pd.concat([df, df_nordics])
df = df[df["Continent"] != "Unspecified"]


# Selins graph

# Preprocessing
df_PaM = pd.read_csv(f"{dataPath}/PaM_number.csv")

# Teemus graph
teemusData = pd.read_excel(
    io=f"{dataPath}/teemusData.xls", sheet_name="Total Greenhouse Gas Emission"
).T
teemusData.columns = teemusData.iloc[0]
teemusData = teemusData[1:]


#############################
#     Start of the page     #
#############################

layout = html.Div(
    children=[
        dbc.Row(
            [   
                dbc.NavbarSimple(
                            children=[
                                dbc.NavItem(dbc.NavLink("Questionnaire", href="/..")),
                                dbc.NavItem(dbc.NavLink("Home", href="#")),
                                dbc.NavItem(dbc.NavLink("Future", href="whatif")),
                                dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master")),
                            ],
                            brand="Home",
                            brand_href="graphs",
                            color="primary",
                            dark=True,
                        ),
                        html.H1(
                            "Introduction", style={"margin-top":"5%","text-align": "center"}
                        ),
                        dcc.Markdown('''
                            Climate change is one of the most significant challenges that humanity is currently facing. 
                            Economic and population growth comes with more emissions. 
                            The emissions are distributed globally and over a wide range of societal activities, and are likely to cause widespread social, economic, and ecosystem damage if not limited.  
                            Therefore, it is important that all countries in the world try to tackle these global issues together. 
                            This website is created to communicate the emission reduction momentum to more audiences. 
                        ''',style={"margin":"2%"}),
                dbc.Row(
                    [
                        
                        html.H1(
                            "CO2 emissions per sector", style={"text-align": "center"}
                        ),
                        html.Div(
                            children=[
                                html.H3("Select scope:"),
                                dcc.Dropdown(
                                    id="scope",
                                    options=choices,
                                    multi=False,
                                    value="Global emissions",
                                    style={"width": "60%"},
                                ),
                                html.Br(),
                                dcc.RadioItems(
                                    id="scale",
                                    options=["Total CO2", "CO2 / capita"],
                                    value="CO2 / capita",
                                ),
                            ],
                            style={"width": "50%", "margin-left": "50px"},
                        ),
                        html.Br(),
                        dcc.Graph(id="sector_emissions_graph", style={'marggin':"2%","height":"45vh"}),


                        dcc.Markdown('''
                            Which sectors are the main contributors to CO2 emissions?
                            CO2 emitted into the atmosphere comes from different types of activities. Some sectors produce far more carbon emissions than others.
                            With the issue of climate change far from resolved, understanding the determinants behind the emission levels can help us prioritize appropriate actions and improve guide policy making.
                            This chart shows the breakdown of CO2 emissions across sectors (power industry, buildings, transport, other industrial combustion, and other sectors). 
                            The data used in the graph is adopted from [EDGAR - Emissions Database for Global Atmospheric Research](https://edgar.jrc.ec.europa.eu/emissions_data_and_maps).
                        ''',style={"margin":"2%"}),    
                    ],
                    style={"order": 2},
                ),
                dbc.Row(
                    [
                        html.H1(
                            "CO2 emission per capita", style={"text-align": "center"}
                        ),
                        html.Div(
                            children=[
                                html.H3("Choose a region:",style={"margin":"2%"}),
                            ],
                            style={"width": "100%"},
                        ),
                        dcc.RadioItems(
                            id="region",
                            options=region,
                            value="World",
                            inline=False,
                            labelStyle={
                                "display": "inline-block",
                            }
                            ,style={"margin":"2%"} 
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="co2_graph", figure={}, style={"margin": "2%","height":"50vh"}
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                dcc.Slider(
                                    min=1970,
                                    max=2021,
                                    step=1,
                                    value=2021,
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": False,
                                    },
                                    id="year_slider",
                                )
                            ],
                            style={"width": "50%", "margin-left": "440px"},
                        ),
                        html.Div(
                            id="output_container",
                            children=[],
                            style={"text-align": "center", "font-size": "25px"},
                        ),
                        html.Br(),
                        dcc.Markdown('''
                            What are the average emissions per person? Where in the world does the average person emit the most CO2 each year?


                            Different metrics capture different stories.  A per capita view offers an important perspective on the 
                            global CO2 challenge and gives a clear point of how much each person can reduce emissions 
                            to together tackle this climate change.  In this interactive map, you can explore the differences in CO2
                            per capita emissions, which is the average amount of CO2 emitted by each  citizen of each country, across the world and over time. 
                            In general, there are very large inequalities in per capita emissions across the world.                            
                        ''',style={"margin":"2%"}),
                    ],
                    style={
                        "order": 1,
                    },
                ),
                dbc.Row(
                    [
                        html.H1(
                            "GDP per capita and CO2 emissions per capita by region and by country",
                            style={"text-align": "center"},
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.Br(),
                                        dcc.RadioItems(
                                            ["Linear", "Log"],
                                            "Log",
                                            id="crossfilter-type",
                                            # labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                                        ),
                                    ],
                                    style={"width": "49%", "display": "inline-block"},
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="scatterplot-percapita",
                                    hoverData={"points": [{"id": "Finland"}]},
                                )
                            ],
                            style={
                                "width": "55%",
                                "display": "inline-block",
                                "padding": "0 20",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="x-time-series"),
                                dcc.Graph(id="y-time-series"),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),
                        
                        dcc.Markdown('''

                    '''),
                    html.Br(),
                    dcc.Markdown('''
                        What explains the variation in CO2 emissions per capita?
                        Since the industrial revolution, economic activities has significantly increased. However, eonomic growth comes with a cost. 
                        According to [National Oceanic and Atmostpheric Administration], humans have generated an estimated 1.5 trillion tons of CO2 pollution since then,
                        much of which will continue to warm the atmosphere for thousands of years.

                        The health of a country's economy and welfare is measured by Gross Dosmetic Product (GDP). It represents the value of all goods and services produced 
                        over a specific time period within a country's borders. This graph shows the correlation between gross domestic product (GDP) per capita and CO2 per capita.
                        In general, there is a strong link between the amount of CO2 emitted and the standards of living. A brief look at the graph shows that emissions are rising as the economy grows. 
                        However, Nordic countries are examples of opposite trend which illustrates that we together can make effort to reduce the CO2 emissiond while 
                        keeping the GDP per capita high.                          
                    ''',style={"margin":"0%"}),
                    ],
                    style={"order": 3,"margin":"2%"},
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
                        dcc.Graph(id="selinsGraph",style={"height":"70vh"}),
                        dcc.Markdown('''
                            According to [Statista](https://www.statista.com/topics/4958/emissions-in-the-european-union/#dossierKeyfigures), countries of European Union (EU-27) emits
                            more than 240 billion metric tons of CO2 equivalent (GtCO2e) into the atmosphere since the industrial evolution, which makes up approximately 18% of total historical global
                            greenhouse gases emissions. 

                            Current policies to reduce, or at least slow down growth, in CO2 and other greenhouse gas emissions will have some impact on tackling this global issues.
                            The European Council has adopted the European climate law in 2021. With it, EU countries are legally oblidged to 
                            cut at least 55% emissions by 2030 and achieve climate-neutrality to reach a net-zero emissions balance by 2050. In order to meet this agreement, different EU countries in Europe have adopted policies for different sectors. 
                            In this graph, we can explore the number of  policies adopted in different countries in Europe by sector. 
                        '''),
                    ],
                    style={"order": 4,"margin":"2%"},
                ),
                dbc.Row(
                    [
                        html.H1(
                            "Resources for the Future: Carbon pricing calculator",
                            style={"text-align": "center"},
                        ),
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
                                {
                                    "label": "Consumer Prices % Change in 2030 Compared to Business as Usual",
                                    "value": "RFF_Consumer_Prices.csv",
                                },
                            ],
                            value="RFF_Annual_EmissionsL.csv",
                            id="RFF_calc_file",
                            style={"margin": "0%"},
                        ),
                        dcc.Graph(id="RFF_calc", style={"height": "45vh"}),
                        dcc.Markdown(
                            """
                            Resources for the Future (RFF) describes themselves as an independent, non-profit research institution situated in Washington, DC. 
                            Their goal is to improve the decision-making process around environmental policy, via research and policy action. 
                            [Their Carbon Pricing Calculator](https://www.rff.org/publications/data-tools/carbon-pricing-calculator/) is a great way to illustrate how different policies can have an impact on the environment. 
                                                       
                            The RFF utilizes the Goulder-Hafstead Energy-Environment-Economy E3 CGE Model, an economy-wide model of the United States with international trade to evaluate the impact of the policies. 
                            Its focus is on tax system and its interaction with pre existing environmental and economic policies.
                            As of 17.11.2022 all of the Acts are at the "Introduced" stage, and need to pass the Senate, the House and the President to become law.
                            Follow legislation process on [congress.gov](https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%7D).
                                                 
                            Although RFF is focused on the United States, it considers policy actions that are reproducible in the Nordics too. 
                            These include flat and incremental carbon taxes, with revenue recycling. You can learn more from their website [here](https://www.rff.org/).
                        """
                        ),
                    ],style={"order": 5,"margin":"2%"}

                ),
                dbc.Row(
                    [
                        html.H1("Emissions by country", style={"text-align": "center"}),
                        dbc.Label(
                            "Choose between total emissions (Million metric tons), or ratio by per capita or per GDP"
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
                        dcc.Graph(id="teemusGraph", style={"height":"45vh"}),
                        dcc.Markdown('''
                            European Comission has a great database called [EDGAR - Emissions Database for Global Atmospheric Research.](https://edgar.jrc.ec.europa.eu/emissions_data_and_maps)
                            It allows us to see how the fight against climate change is developing in different regions.
                            However, the raw emission data can be misleading, as it does not account for changes in population or the changes in GDP. 
                            It is also quite common to focus only on the CO2 emissions, although other greenhouse gases also contribute significantly to the problem. 
                            A good example is methane that contributes 25% to global warming. 
                            Finally, the country specific data does not account for emissions resulting from imported or exported goods and services. 
                            Thus, it has a bias towards economies that have outsourced polluting industries.
                        ''',style={"margin":"0%"}),
                        dcc.Markdown("""
                        ## [What can you do?](/whatif)
                        """,style={"height":"5vh"}),
                        dbc.NavbarSimple(
                            children=[
                                dbc.NavItem(dbc.NavLink("Questionnaire", href="/..")),
                                dbc.NavItem(dbc.NavLink("Home", href="#")),
                                dbc.NavItem(dbc.NavLink("Future", href="whatif")),
                                dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master")),
                            ],
                            brand="Up",
                            brand_href="#",
                            color="primary",
                            dark=True,
                        )  
                    ],
                    style={"order": 6,"margin":"2%"},
                ),
                
            ],
            style={"display": "flex", "flex-direction": "column"},
        ),
    ],
)


@callback(
    Output("sector_emissions_graph", "figure"),
    Input("scope", "value"),
    Input("scale", "value"),
)
def update_graph_co2_by_sector(select, scale):
    if scale == "CO2 / capita":
        if select == "Global emissions":
            data = global_sector_per_capita.copy()
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(
                data,
                id_vars="Sector",
                value_vars=data.columns,
                var_name="Year",
                value_name="CO2 emissions [Tonnes/person]",
                ignore_index=True,
            )
            fig = px.area(
                data,
                x="Year",
                y="CO2 emissions [Tonnes/person]",
                color="Sector",
                template="none",
            )
        else:
            # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
            # produces a series when it produces a dataframe. Works when running so no problem
            data = sector_per_capita.copy()
            data = data[data["Country"] == select]  # select country data
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
                value_name="CO2 emissions [Tonnes/person]",
                ignore_index=True,
            )
            fig = px.area(
                data,
                x="Year",
                y="CO2 emissions [Tonnes/person]",
                color="Sector",
                template="none",
            )
        return fig
    else:
        if select == "Global emissions":
            data = sector_data.copy()
            data.drop(
                columns=["Country", "EDGAR Country Code"], inplace=True
            )  # not needed on global scope
            data = data.groupby(
                "Sector", as_index=False
            ).sum()  # group by sector, aggregate by summing yearly emissions
            data.columns = data.columns.astype(str)
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(
                data,
                id_vars="Sector",
                value_vars=data.columns,
                var_name="Year",
                value_name="CO2 emissions [Megatonnes]",
                ignore_index=True,
            )
            fig = px.area(
                data,
                x="Year",
                y="CO2 emissions [Megatonnes]",
                color="Sector",
                template="none",
            )
        else:
            # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
            # produces a series when it produces a dataframe. Works when running so no problem
            data = sector_data.copy()
            data = data[data["Country"] == select]  # select country data
            data.drop(columns=["Country", "EDGAR Country Code"], inplace=True)
            data.columns = data.columns.astype(
                str
            )  # change names to string to ensure sound processing
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(
                data,
                id_vars="Sector",
                value_vars=data.columns[1:],
                var_name="Year",
                value_name="CO2 emissions [Megatonnes]",
                ignore_index=True,
            )
            fig = px.area(
                data,
                x="Year",
                y="CO2 emissions [Megatonnes]",
                color="Sector",
                template="none",
            )
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
        locationmode="country names",
        locations="Country",
        color=year_slctd,
        range_color=[0, 20],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        hover_data={"Country": False},
        labels={str(year_slctd): ",    CO2 emission/capita"},
        hover_name="Country",
        basemap_visible=True,
        # center = center_dict[region_slctd]
    )
    fig.update_geos(fitbounds="locations")

    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True),
        #     height=400,
    )
    fig.update_coloraxes(colorbar_orientation="h", colorbar_y=1)
    return container, fig


@callback(Output("scatterplot-percapita", "figure"), Input("crossfilter-type", "value"))
def update_graph_co2_and_gdp_per_capita(type):

    fig = px.scatter(
        df,
        x="GDP_per_capita",
        y="CO2_per_capita",
        size="Population",
        color="Continent",
        hover_name="Country",
        animation_frame="Year",
        animation_group="Country",
        size_max=55,
    )

    fig.update_traces(customdata=df["Country"])

    fig.update_xaxes(
        title="GDP per capita (current US$)",
        type="linear" if type == "Linear" else "log",
    )

    fig.update_yaxes(
        title="CO2 per capita (Tonnes/person)",
        type="linear" if type == "Linear" else "log",
    )

    fig.update_layout(
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
        height=500,
        transition_duration=500,
    )
    return fig


def create_time_series(filtered_df, axis_type, title, y_axis):
    fig = px.scatter(filtered_df, x="Year", y=y_axis)
    fig.update_traces(mode="lines+markers")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        type="linear" if axis_type == "Linear" else "log",
        title="CO2/capita (tonnes/person)"
        if y_axis == "CO2_per_capita"
        else "GDP/capita (current US$)",
    )
    fig.add_annotation(
        x=0,
        y=0.85,
        xanchor="left",
        yanchor="bottom",
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
        text=title,
    )
    fig.update_layout(height=255, margin={"l": 20, "b": 30, "r": 10, "t": 10})

    return fig


@callback(
    Output("x-time-series", "figure"),
    Input("scatterplot-percapita", "hoverData"),
    Input("crossfilter-type", "value"),
)
def update_y_timeseries(hoverData, axis_type):
    country_name = hoverData["points"][0]["id"]
    if country_name in nordic_countries:
        filtered_df = df_nordics[df_nordics["Country"] == country_name]
    else:
        filtered_df = df[df["Country"] == country_name]
    title = country_name
    return create_time_series(filtered_df, axis_type, title, "GDP_per_capita")


@callback(
    Output("y-time-series", "figure"),
    Input("scatterplot-percapita", "hoverData"),
    Input("crossfilter-type", "value"),
)
def update_x_timeseries(hoverData, axis_type):
    country_name = hoverData["points"][0]["id"]
    if country_name in nordic_countries:
        filtered_df = df_nordics[df_nordics["Country"] == country_name]
    else:
        filtered_df = df[df["Country"] == country_name]
    title = country_name
    return create_time_series(filtered_df, axis_type, title, "CO2_per_capita")


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
    #fig.update_coloraxes(colorbar_orientation="h", colorbar_y=1)
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

@callback(Output("RFF_calc", "figure"), Input("RFF_calc_file", "value"))
def display_area(calc_file):
    df = pd.read_csv(f"{dataPath}/{calc_file}")
    omitted_policies = [
            "America Wins Act (Larson)",
            "American Opportunity Carbon Fee Act (Whitehouse-Schatz)",
            "Consumers REBATE Act (McNerney)",
            "Healthy Climate and Family Security Act (Van Hollen-Beyer)",
            "MARKET CHOICE Act (Fitzpatrick)",
            "Raise Wages Cut Carbon Act (Lipinski)"
            ]
    if calc_file == "RFF_Consumer_Prices.csv":
        fig = go.Figure()
        df = df.drop(columns = omitted_policies)
        for colName in df.columns[1:]:
            fig.add_trace(go.Bar(y=df[colName], x=df["Category"], name=colName))
    else:
        df = df[~df["Policy"].isin(omitted_policies)]
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
        legend_orientation="h",
        legend_borderwidth=0,
        legend_y=-0.2,
        plot_bgcolor="white",
    )
    return fig