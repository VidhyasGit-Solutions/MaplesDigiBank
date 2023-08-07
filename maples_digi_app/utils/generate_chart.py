import plotly.graph_objects as go

def generate_gauge_chart(value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': "Credit Report Back Home"},
        gauge = {
            'axis': {'range': [300, 900]},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [300, 599], 'color': "red"},
                {'range': [600, 649], 'color': "orange"},
                {'range': [650, 699], 'color': "yellow"},
                {'range': [700, 749], 'color': "lightgreen"},
                {'range': [750, 900], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 900
            }
        }
    ))
    return fig