import dash
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/question3")
layout = html.Div(
    [
        dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Quiz", href="#")),
                        dbc.NavItem(dbc.NavLink("Home", href="graphs")),
                        dbc.NavItem(dbc.NavLink("Future", href="whatif")),
                        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/Tepes99/team2datascienceproject/tree/main")),
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
                    "How much global temperatures are predicted to rise within the next 2 decades?",
                    className="question",
                    style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}
                ),
                html.Div(
                    [
                        html.Button(
                            "1.5 Celcious",
                            className="stuff",
                            id="first_button_ques3",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "5 Celcious",
                            className="stuff",
                            id="second_button_ques3",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "7 Celsious",
                            className="stuff",
                            id="third_button_ques3",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "20 Celsious",
                            className="stuff",
                            id="fourth_button_ques3",
                            style={"margin": "6px"},
                        ),
                    ],
                    className="answer_4",
                ),
            ],
            id="question3",
        ),
        dcc.Markdown(""" 
        ### Quizz inspired by [GapMinder's climate action quizz](https://upgrader.gapminder.org/t/sdg-world-13/)
        """, style={"margin-top":"5%", 'textAlign': 'center',}
        ),
    ]
)


@callback(
    Output("question3", "children"),
    Input("first_button_ques3", "n_clicks"),
    Input("second_button_ques3", "n_clicks"),
    Input("third_button_ques3", "n_clicks"),
    Input("fourth_button_ques3", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3, b4):
    triggered_id = ctx.triggered_id
    if triggered_id == "first_button_ques3":
        return html.Div(
            [
                html.H1("You are right", className="solution",style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("Incorrect", className="solution",style= {"textAlign":"center","margin-left": "37.5%", "margin-right": "37.5%"}),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
