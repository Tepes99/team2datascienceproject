import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/question5")
layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How many percent of the global warming we are experiencing today is caused by methane in the atmosphere?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "20%",
                            className="stuff",
                            id="first_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "25%",
                            className="stuff",
                            id="second_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "50%",
                            className="stuff",
                            id="third_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "60%",
                            className="stuff",
                            id="fourth_button_quest5",
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
            id="question5",
        ),
    ]
)


@callback(
    Output("question5", "children"),
    Input("first_button_quest5", "n_clicks"),
    Input("second_button_quest5", "n_clicks"),
    Input("third_button_quest5", "n_clicks"),
    Input("fourth_button_quest5", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3, b4):
    triggered_id = ctx.triggered_id
    if triggered_id == "second_button_quest5":
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
                    href="/graphs",
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
                    href="/graphs",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
