import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/question2")
layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How many people in the world live in areas that are 5 meters or less above sea level?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "Around 11%",
                            className="stuff",
                            id="ques2_first_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 31%",
                            className="stuff",
                            id="ques2_second_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 51%",
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
                html.H1(" Far to the beach ", className="solution"),
                html.H2(
                    "Most people overestimate the population at risk from rising sea levels. When you overestimate how many homes can be reached by rising sea levels, you may think it’s impossible for so many people to find new places to live.",
                    className="fact",
                ),
                dcc.Link(
                    "Next question",
                    href="/question3",
                    className="stuff next_button",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("You are right", className="solution"),
                html.H2(
                    "But 77% of people answer wrongly. Most people overestimate the population at risk from rising sea levels. When they overestimate how many homes can be reached by rising sea levels, they may think it’s impossible for so many people to find new places to live.",
                    className="fact",
                ),
                dcc.Link(
                    "Next question",
                    href="/question3",
                    className="stuff next_button",
                ),
            ]
        )
