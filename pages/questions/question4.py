import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/question4")

layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How many million tonnes of plastic is leaked to the ocean?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "2 million",
                            className="stuff",
                            id="first_button_ques4",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "6 million",
                            className="stuff",
                            id="second_button_ques4",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "10 million",
                            className="stuff",
                            id="third_button_ques4",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "13 million",
                            className="stuff",
                            id="fourth_button_ques4",
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
            id="question4",
        ),
    ]
)


@callback(
    Output("question4", "children"),
    Input("first_button_ques4", "n_clicks"),
    Input("second_button_ques4", "n_clicks"),
    Input("third_button_ques4", "n_clicks"),
    Input("fourth_button_ques4", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3, b4):
    triggered_id = ctx.triggered_id
    if triggered_id == "second_button_ques4":
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
                    "To Knowledge",
                    href="/question5",
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
                    "To Knowledge",
                    href="/question5",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
