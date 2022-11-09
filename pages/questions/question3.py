import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/question3")
layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How much global temperatures are predicted to rise within the next 2 decades?",
                    className="question",
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
                html.H1("You are right", className="solution"),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    className="stuff next_button",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("Incorrect", className="solution"),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    className="stuff next_button",
                ),
            ]
        )
