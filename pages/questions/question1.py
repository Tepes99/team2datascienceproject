import dash
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")
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
        html.Div([]),
        html.Div(
            [
                html.H1(
                    "What is the United Nations body for assessing the science related to climate change?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "IPPD",
                            className="stuff",
                            id="first_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Y.M.C.A.",
                            className="stuff",
                            id="second_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "IPCC",
                            className="stuff",
                            id="third_button",
                            style={"margin": "6px"},
                        ),
                    ],
                    className="answer_3",
                ),
            ],
            id="hook_question",
        ),
        dcc.Markdown(""" 
        ### Questionnaire inspired by [GapMinder's climate action questionnaire](https://upgrader.gapminder.org/t/sdg-world-13/)
        """, style={"margin-top":"5%", 'textAlign': 'center',}
        ),
    ]
)


@callback(
    Output("hook_question", "children"),
    Input("first_button", "n_clicks"),
    Input("second_button", "n_clicks"),
    Input("third_button", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3):
    triggered_id = ctx.triggered_id
    if triggered_id == "first_button" or triggered_id == "second_button":
        return html.Div(
            [
                html.H1(
                    "IPPD is used to make the rubber in tires and Y.M.C.A. is a song by American disco group Village People",
                    className="solution",
                ),
                dcc.Link(
                    "Next question",
                    href="/question2",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("You are right", className="solution"),
                html.P(
                    "The Intergovernmental Panel on Climate Change (IPCC) is the United Nations body for assessing the science related to climate change.",
                    className="fact",
                ),
                dcc.Link(
                    "Next question",
                    href="/question2",
                    className="stuff next_button",
                    style={"width": "25%", "justify-content":"center"},
                ),
            ]
            
        )
