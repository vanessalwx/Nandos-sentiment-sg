import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = "Nando's SG Social Intelligence Dashboard"

# --- Sample Simulated Data ---
data = pd.DataFrame({
    "Month": ["Feb", "Feb", "Feb", "Mar", "Mar", "Mar", "Apr", "Apr", "Apr", "May", "May", "May"] * 2,
    "Platform": ["TikTok", "Instagram", "Reddit"] * 8,
    "Sentiment": ["Positive", "Neutral", "Negative"] * 8,
    "Mentions": [60, 30, 10, 80, 20, 15, 70, 25, 20, 90, 15, 10,
                 40, 50, 20, 50, 30, 10, 60, 20, 15, 75, 20, 5]
})

# Top themes (simulated)
top_themes = pd.DataFrame({
    "Theme": ["Service issues", "Dry chicken", "Great campaigns", "Spicy not spicy", "Sauce missing"],
    "Mentions": [45, 30, 50, 25, 35],
    "Sentiment": ["Negative", "Negative", "Positive", "Neutral", "Negative"]
})

# Top quotes (dummy)
top_quotes = pd.DataFrame({
    "Platform": ["Reddit", "Instagram", "TikTok"],
    "Quote": [
        "I wish SG Nando's tasted more like the one in KL…",
        "Friend-zone your chicken is hilarious 🤣",
        "Honestly? Best spice kick in town."
    ],
    "Sentiment": ["Negative", "Positive", "Positive"]
})

# --- Layout ---
app.layout = html.Div([
    html.H1("Nando’s SG Social Intelligence Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Month(s):"),
        dcc.Dropdown(
            options=[{"label": m, "value": m} for m in data["Month"].unique()],
            value=["Feb", "Mar", "Apr", "May"],
            multi=True,
            id="month-selector"
        ),
        html.Label("Select Platform(s):"),
        dcc.Dropdown(
            options=[{"label": p, "value": p} for p in data["Platform"].unique()],
            value=["TikTok", "Instagram", "Reddit"],
            multi=True,
            id="platform-selector"
        )
    ], style={"width": "60%", "margin": "auto"}),

    html.H2("Mentions Over Time by Sentiment"),
    dcc.Graph(id="mentions-line"),

    html.H2("Sentiment Breakdown by Platform"),
    dcc.Graph(id="sentiment-platform-bar"),

    html.H2("Top Discussed Themes"),
    dcc.Graph(
        figure=px.bar(top_themes, x="Mentions", y="Theme", color="Sentiment", orientation="h",
                     title="Top Themes by Mentions")
    ),

    html.H2("Top Social Quotes"),
    html.Table([
        html.Thead([
            html.Tr([html.Th(col) for col in top_quotes.columns])
        ]),
        html.Tbody([
            html.Tr([html.Td(top_quotes.iloc[i][col]) for col in top_quotes.columns])
            for i in range(len(top_quotes))
        ])
    ], style={"width": "80%", "margin": "auto", "border": "1px solid #ccc"})
])

# --- Callbacks ---
@app.callback(
    Output("mentions-line", "figure"),
    Output("sentiment-platform-bar", "figure"),
    Input("month-selector", "value"),
    Input("platform-selector", "value")
)
def update_graphs(selected_months, selected_platforms):
    filtered = data[data["Month"].isin(selected_months) & data["Platform"].isin(selected_platforms)]

    # Mentions over time
    line = px.line(
        filtered.groupby(["Month", "Sentiment"]).sum(numeric_only=True).reset_index(),
        x="Month", y="Mentions", color="Sentiment",
        markers=True
    )

    # Sentiment by platform
    bar = px.bar(
        filtered.groupby(["Platform", "Sentiment"]).sum(numeric_only=True).reset_index(),
        x="Platform", y="Mentions", color="Sentiment", barmode="group"
    )

    return line, bar

server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
