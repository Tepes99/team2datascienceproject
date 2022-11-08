import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/")
layout = html.Div(
    [
        html.Div([]),
        html.Div(
            [
                html.H1(
                    "How much of the excess heat from global warming is captured in the oceans?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "Around 10%",
                            className="stuff",
                            id="first_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 50%",
                            className="stuff",
                            id="second_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 90%",
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
                    "Don’t look for global warming outside your window",
                    className="solution",
                ),
                dcc.Link(
                    "To Knowledge",
                    href="/question2",
                    className="stuff next_button",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("You are right", className="solution"),
                html.P(
                    "But 90%% of people answer wrongly. Most people are unaware that most global warming is hiding in the seas. As long as they think global warming is all about air temperature, they won’t realize the size of the problem.",
                    className="fact",
                ),
                dcc.Link(
                    "Next question",
                    href="/question2",
                    className="stuff next_button",
                ),
            ]
        )
