import random

import dash
from dash import Input, Output, callback, ctx, dcc, html


##num = random.randint(1, 5)
num = 2
if num == 1:
    layout = html.Div(
        [
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
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "margin-left": "30%",
                            "margin-right": "30%",
                        },
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
                        "You are right",
                        style={
                            "margin-left": "30%",
                            "margin-right": "30%",
                            "font-size": "70px",
                        },
                    ),
                    html.P(
                        "But 90%% of people answer wrongly. Most people are unaware that most global warming is hiding in the seas. As long as they think global warming is all about air temperature, they won’t realize the size of the problem.",
                        style={
                            "margin-left": "30%",
                            "margin-right": "30%",
                            "font-size": "30px",
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

elif num == 2:
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
                                        id="first_button",
                                        style={"margin": "6px"},
                                    )
                                ],
                                className="column",
                            ),
                            html.Button(
                                "5 Celcious",
                                className="stuff",
                                id="second_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "7 Celsious",
                                className="stuff",
                                id="third_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "20 Celsious",
                                className="stuff",
                                id="fourth_button",
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
                id="hook_question",
            ),
        ]
    )

    @callback(
        Output("hook_question", "children"),
        Input("first_button", "n_clicks"),
        Input("second_button", "n_clicks"),
        Input("third_button", "n_clicks"),
        Input("fourth_button", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_log(b1, b2, b3, b4):
        triggered_id = ctx.triggered_id
        if triggered_id == "first_button":
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

elif num == 3:
    layout = html.Div(
        [
            html.Div(
                [
                    html.H1(
                        "How many billion tonnes of ice Antarctica is losing every year?",
                        className="question",
                    ),
                    html.Div(
                        [
                            html.Button(
                                "5 billion",
                                className="stuff",
                                id="first_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "50 billion",
                                className="stuff",
                                id="second_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "100 billion",
                                className="stuff",
                                id="third_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "150 billion",
                                className="stuff",
                                id="fourth_button",
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
                id="hook_question",
            ),
        ]
    )

    @callback(
        Output("hook_question", "children"),
        Input("first_button", "n_clicks"),
        Input("second_button", "n_clicks"),
        Input("third_button", "n_clicks"),
        Input("fourth_button", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_log(b1, b2, b3, b4):
        triggered_id = ctx.triggered_id
        if triggered_id == "fourth_button":
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

elif num == 4:
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
                                id="first_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "6 million",
                                className="stuff",
                                id="second_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "10 million",
                                className="stuff",
                                id="third_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "13 million",
                                className="stuff",
                                id="fourth_button",
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
                id="hook_question",
            ),
        ]
    )

    @callback(
        Output("hook_question", "children"),
        Input("first_button", "n_clicks"),
        Input("second_button", "n_clicks"),
        Input("third_button", "n_clicks"),
        Input("fourth_button", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_log(b1, b2, b3, b4):
        triggered_id = ctx.triggered_id
        if triggered_id == "second_button":
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

else:
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
                                id="first_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "25%",
                                className="stuff",
                                id="second_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "50%",
                                className="stuff",
                                id="third_button",
                                style={"margin": "6px"},
                            ),
                            html.Button(
                                "60%",
                                className="stuff",
                                id="fourth_button",
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
                id="hook_question",
            ),
        ]
    )

    @callback(
        Output("hook_question", "children"),
        Input("first_button", "n_clicks"),
        Input("second_button", "n_clicks"),
        Input("third_button", "n_clicks"),
        Input("fourth_button", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_log(b1, b2, b3, b4):
        triggered_id = ctx.triggered_id
        if triggered_id == "second_button":
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
