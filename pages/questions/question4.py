import dash
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/question4")

layout = html.Div(
    [
        dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Quiz", href="#")),
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
                    className="answer_4",
                ),
            ],
            id="question4",
        ),
        dcc.Markdown(""" 
        ### Quizz inspired by [GapMinder's climate action quizz](https://upgrader.gapminder.org/t/sdg-world-13/)
        """, style={"margin-top":"5%", 'textAlign': 'center',}
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
                html.H1("Excellent", className="solution"),
                dcc.Link(
                    "Next question",
                    href="/question5",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("Incorrect", className="solution"),
                dcc.Link(
                    "Next question",
                    href="/question5",
                    className="stuff next_button",
                    style= {"width": "25%", "justify-content":"center"},
                ),
            ]
        )
