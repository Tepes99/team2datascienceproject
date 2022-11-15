import dash
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/question2")
layout = html.Div(
    [
        dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Questionnaire", href="#")),
                        dbc.NavItem(dbc.NavLink("Home", href="graphs")),
                        dbc.NavItem(dbc.NavLink("Future", href="whatif")),
                        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/HieuPhamNgoc/Data-Science-Project-Group-2/tree/master")),
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
                html.H1("Not quite right", className="solution"),
                html.H2(
                    "The first two certainly sound catchy, but neither is correct. Cap and trade is used to set maximum amount of emissions and permits are distributed for companies to trade or use",
                    className="fact",
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
                html.H1("You are right", className="solution"),
                html.H2(
                    "The first two certainly sound catchy, but neither is correct. Cap and trade is used to set maximum amount of emissions and permits are distributed for companies to trade or use",
                    className="fact",
                ),
                dcc.Link(
                    "Next question",
                    href="/question3",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
