import dash
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/question2")
layout = html.Div(
    [
        dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Quiz", href="#")),
                        dbc.NavItem(dbc.NavLink("Home", href="graphs")),
                        dbc.NavItem(dbc.NavLink("Future", href="whatif")),
                        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master")),
                        dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("Developer Team", header=True),
                                    dbc.DropdownMenuItem("Daniel Aaltonen", href="https://github.com/Daalton3n"),
                                    dbc.DropdownMenuItem("Dung Nguyen Anh", href="https://github.com/nguu0123"),
                                    dbc.DropdownMenuItem("Hieu Pham", href="https://github.com/HieuPhamNgoc"),
                                    dbc.DropdownMenuItem("Linh Ngo", href="https://github.com/linhlngo"),
                                    dbc.DropdownMenuItem("Selin Taskin", href="https://github.com/selintaskin"),
                                    dbc.DropdownMenuItem("Teemu Saha", href="https://github.com/Tepes99"),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="Team",
                        ),
                    ],
                    brand="Home",
                    brand_href="graphs",
                    color="primary",
                    dark=True,
                ),
        html.Div(
            [
                html.H1(
                    "Which of the following is a widely used policy to reduce global carbon emissions?",
                    className="question",
                    style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}
                ),
                html.Div(
                    [
                        html.Button(
                            "Mix and match",
                            className="stuff",
                            id="ques2_first_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Catch and tax",
                            className="stuff",
                            id="ques2_second_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Cap and trade",
                            className="stuff",
                            id="ques2_third_button",
                            style={"margin": "6px"},
                        ),
                    ],
                    className="answer_3",
                ),
            ],
            id="question2",
        ),
        dcc.Markdown(""" 
        ### Quizz inspired by [GapMinder's climate action quizz](https://upgrader.gapminder.org/t/sdg-world-13/)
        """, style={"margin-top":"5%", 'textAlign': 'center',}
        ),
    ]
)


@callback(
    Output("question2", "children"),
    Input("ques2_first_button", "n_clicks"),
    Input("ques2_second_button", "n_clicks"),
    Input("ques2_third_button", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3):
    triggered_id = ctx.triggered_id
    if triggered_id == "ques2_first_button" or triggered_id == "ques2_second_button":
        return html.Div(
            [
                html.H1("Not quite right", className="solution",style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}),
                html.H2(
                    "The first two certainly sound catchy, but neither is correct. Cap and trade is used to set maximum amount of emissions and permits are distributed for companies to trade or use",
                    className="fact",
                    style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}
                ),
                dcc.Link(
                    "Next question",
                    href="/question3",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("You are right", className="solution",style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}),
                html.H2(
                    "The first two certainly sound catchy, but neither is correct. Cap and trade is used to set maximum amount of emissions and permits are distributed for companies to trade or use",
                    className="fact",
                    style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}
                ),
                dcc.Link(
                    "Next question",
                    href="/question3",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
