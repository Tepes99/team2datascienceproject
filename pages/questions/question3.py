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
                        html.Div(
                            [
                                html.Button(
                                    "1.5 Celcious",
                                    className="stuff",
                                    id="first_button_ques3",
                                    style={"margin": "6px"},
                                )
                            ],
                            className="column",
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
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "margin-left": "30%",
                        "margin-right": "30%",
                    },
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
                html.H1(
                    "Correct",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "70px",
                    },
                ),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1(
                    "Incorrect",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "70px",
                    },
                ),
                dcc.Link(
                    "Next question",
                    href="/question4",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
