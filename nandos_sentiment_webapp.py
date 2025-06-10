import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

# Sample data
monthly_sentiments = pd.DataFrame({
    "Month": ["Feb 2025", "Mar 2025", "Apr 2025", "May 2025"],
    "Mentions": [120, 180, 160, 220]
})

sentiment_topics = {
    "Positive": ["Good food, Clean ambience", "Fun campaign, Friend-zone chicken", "Interactive rating feature", "Kiss your chicken trend"],
    "Neutral": ["Standard posts", "Queue reports", "Mixed reviews on spice", "Promo posts"],
    "Negative": ["Service inconsistency", "No sauce left", "Overcooked chicken", "Table service complaints"]
}

app = Dash(__name__)

pie_labels = ['Positive', 'Neutral', 'Negative']
pie_values = [65, 25, 10]

customdata = sentiment_topics['Positive'] + sentiment_topics['Neutral'] + sentiment_topics['Negative']

pie_chart = go.Figure(data=[
    go.Pie(
        labels=pie_labels * 1,
        values=pie_values,
        hoverinfo="label+percent",
        textinfo="label+percent",
        customdata=customdata,
        hovertemplate="%{label}: %{percent} <br>Topic: %{customdata}<extra></extra>"
    )
])

line_chart = px.line(monthly_sentiments, x="Month", y="Mentions", title="Monthly Mentions Trend")

app.layout = html.Div([
    html.H1("Nando's Singapore Sentiment Dashboard (Feb–May 2025)"),
    html.Div([
        html.Div([
            dcc.Graph(figure=pie_chart)
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(figure=line_chart)
        ], style={'width': '48%', 'display': 'inline-block'})
    ])
])

server = app.server

if __name__ == '__main__':
    app.run()
