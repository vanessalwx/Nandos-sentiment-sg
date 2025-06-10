import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = "Nando's SG Social Intelligence Dashboard"

# --- Updated Data with Google Reviews ---
data = pd.DataFrame({
    "Month": [
        "Feb", "Feb", "Feb", "Mar", "Mar", "Mar", "Apr", "Apr", "Apr", "May", "May", "May",
        "May", "May", "May", "May", "May", "May"
    ],
    "Platform": [
        "TikTok", "Instagram", "Reddit", "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit", "TikTok", "Instagram", "Reddit",
        "Google Reviews", "Google Reviews", "Google Reviews",
        "Google Reviews", "Google Reviews", "Google Reviews"
    ],
    "Sentiment": [
        "Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative",
        "Positive", "Positive", "Negative", "Neutral", "Negative", "Positive"
    ],
    "Mentions": [
        60, 30, 10, 80, 20, 15, 70, 25, 20, 90, 15, 10,
        6, 6, 6, 6, 6, 6
    ]
})

# Top themes (including Google Reviews)
top_themes = pd.DataFrame({
    "Theme": [
        "Service issues", "Dry chicken", "Quick Lunch Meal Campaign",
        "Spicy not spicy", "Pricing and value perception",
        "Queue times", "Inconsistent portions", "Grill quality", "Staff attentiveness"
    ],
    "Mentions": [45, 30, 50, 25, 35, 20, 15, 18, 22],
    "Sentiment": [
        "Negative", "Negative", "Positive", "Neutral", "Negative",
        "Neutral", "Negative", "Positive", "Positive"
    ]
})

# Top quotes including Google Reviews
# Note: These are paraphrased and shortened for clarity

top_quotes = pd.DataFrame({
    "Platform": ["Reddit", "Instagram", "TikTok", "Google Reviews", "Google Reviews"],
    "Quote": [
        "The SG outlet doesn’t taste like KL’s version…",
        "Friend-zone your chicken is hilarious 🤣",
        "Best spice kick in town.",
        "Chicken juicy but sour, not smoky like AU.",
        "Queued 10 min, card-only payment, good food though."
    ],
    "Sentiment": ["Negative", "Positive", "Positive", "Neutral", "Positive"],
    "Campaign": ["N/A", "Quick Lunch Meal", "People’s Griller", "N/A", "N/A"]
})

# --- Layout ---
app.layout = html.Div([
    html.Div([
        html.Img(src='/assets/nandos_logo.png', style={
            'height': '80px', 'margin': '0 auto', 'display': 'block'})
    ]),

    html.H1("Nando’s SG Social Intelligence Dashboard", style={"textAlign": "center", "color": "#d71f26"}),

    html.Div([
        html.Label("Select Month(s):", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            options=[{"label": m, "value": m} for m in data["Month"].unique()],
            value=["Feb", "Mar", "Apr", "May"],
            multi=True,
            id="month-selector"
        ),
        html.Br(),
        html.Label("Select Platform(s):", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            options=[{"label": p, "value": p} for p in data["Platform"].unique()],
            value=data["Platform"].unique().tolist(),
            multi=True,
            id="platform-selector"
        )
    ], style={"width": "60%", "margin": "auto", "backgroundColor": "#f9f9f9", "padding": "20px", "borderRadius": "10px"}),

    html.H2("Mentions Over Time by Sentiment", style={"color": "#d71f26"}),
    dcc.Graph(id="mentions-line"),

    html.H2("Sentiment Breakdown by Platform", style={"color": "#d71f26"}),
    dcc.Graph(id="sentiment-platform-bar"),

    html.H2("Top Discussed Themes", style={"color": "#d71f26"}),
    dcc.Graph(
        figure=px.bar(top_themes, x="Mentions", y="Theme", color="Sentiment", orientation="h",
                     color_discrete_map={"Positive": "#d71f26", "Neutral": "#333333", "Negative": "#999999"},
                     title="Top Themes by Mentions")
    ),

    html.H2("Top Social Quotes", style={"color": "#d71f26"}),
    html.Table([
        html.Thead([
            html.Tr([html.Th(col, style={"backgroundColor": "#d71f26", "color": "white"}) for col in ["Quote", "Sentiment"]])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(
                    html.Span(top_quotes.iloc[i]["Quote"],
                              title=f"Source: {top_quotes.iloc[i]['Platform']} | Campaign: {top_quotes.iloc[i]['Campaign']}"),
                    style={"padding": "8px", "border": "1px solid #ccc"}
                ),
                html.Td(top_quotes.iloc[i]["Sentiment"], style={"padding": "8px", "border": "1px solid #ccc"})
            ]) for i in range(len(top_quotes))
        ])
    ], style={"width": "80%", "margin": "auto", "border": "1px solid #ccc", "borderCollapse": "collapse", "backgroundColor": "#fff"})
], style={"backgroundColor": "#ffffff", "fontFamily": "Arial, sans-serif", "padding": "20px"})

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
        markers=True,
        color_discrete_map={"Positive": "#d71f26", "Neutral": "#333333", "Negative": "#999999"}
    )

    # Sentiment by platform
    bar = px.bar(
        filtered.groupby(["Platform", "Sentiment"]).sum(numeric_only=True).reset_index(),
        x="Platform", y="Mentions", color="Sentiment", barmode="group",
        color_discrete_map={"Positive": "#d71f26", "Neutral": "#333333", "Negative": "#999999"}
    )

    return line, bar

server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
