import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = "Nando's SG Social Intelligence Dashboard"

# --- Fixed Length Data ---
data = pd.DataFrame({
    "Month": [
        "Feb", "Feb", "Feb",
        "Mar", "Mar", "Mar",
        "Apr", "Apr", "Apr",
        "May", "May", "May",
        "Feb", "Feb", "Feb",
        "Mar", "Mar", "Mar",
        "Apr", "Apr", "Apr",
        "May", "May", "May",
    ],
    "Platform": [
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "TikTok", "Instagram", "Reddit",
        "Google Reviews", "Google Reviews", "Google Reviews",
    ],
    "Sentiment": [
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Neutral", "Negative",
        "Positive", "Positive", "Negative"
    ],
    "Mentions": [
    60, 30, 10,
    80, 20, 15,
    70, 25, 20,
    90, 15, 10,
    40, 50, 20,
    50, 30, 10,
    6, 6, 6,
    6, 6, 6
]

})

# Top social quotes (cleaned, aligned, and current)
top_quotes = pd.DataFrame({
    "Platform": [
        "Instagram", "Facebook", "Google Reviews", "Reddit", "X (Twitter)"
    ],
    "Quote": [
        "Quick lunch meals are such a smart campaign. Got my chicken cheque today!",
        "Chicken was juicy and the staff checked on us twice — love the service!",
        "Exceptional service by Essa at Nando’s Jurong Point! Found my retainer in the trash. Hero.",
        "Bit overpriced for what they’re offering. Portion size just not worth it.",
        "Nando’s Singapore is my go-to post-gym meal. The pita combos slap."
    ],
    "Sentiment": [
        "Positive", "Positive", "Positive", "Negative", "Positive"
    ],
    "Campaign": [
        "Quick Lunch Meal", "N/A", "N/A", "N/A", "People's Griller"
    ],
    "Theme": [
        "Campaign Engagement", "Service Experience", "Service Experience", "Portion & Value", "Post-Meal Preference"
    ]
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

    html.H2("Top Social Quotes", style={"color": "#d71f26"}),
    html.Table([
        html.Thead([
            html.Tr([html.Th(col, style={"backgroundColor": "#d71f26", "color": "white"}) for col in ["Quote", "Sentiment"]])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(
                    html.Span(top_quotes.iloc[i]["Quote"],
                              title=f"Source: {top_quotes.iloc[i]['Platform']} | Theme: {top_quotes.iloc[i]['Theme']}",
                              style={"padding": "8px", "border": "1px solid #ccc"})
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
