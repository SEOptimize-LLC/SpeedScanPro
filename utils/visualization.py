import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_score_gauge(score: float, title: str):
    """Create a gauge chart for performance scores"""
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': get_score_color(score)},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 90], 'color': "gray"},
                {'range': [90, 100], 'color': "darkgray"}
            ]
        }
    ))

def get_score_color(score: float) -> str:
    """Return color based on score value"""
    if score >= 0.9:
        return "green"
    elif score >= 0.5:
        return "orange"
    return "red"

def create_comparison_chart(desktop_data: dict, mobile_data: dict):
    """Create comparison chart for desktop vs mobile metrics"""
    categories = ['Performance', 'Accessibility', 'Best Practices', 'SEO']
    category_keys = ['performance', 'accessibility', 'best-practices', 'seo']

    try:
        desktop_scores = [
            desktop_data['lighthouse_result']['categories'][key]['score'] * 100 
            for key in category_keys
        ]
        mobile_scores = [
            mobile_data['lighthouse_result']['categories'][key]['score'] * 100 
            for key in category_keys
        ]

        df = pd.DataFrame({
            'Category': categories * 2,
            'Score': desktop_scores + mobile_scores,
            'Device': ['Desktop'] * 4 + ['Mobile'] * 4
        })

        fig = px.bar(
            df,
            x='Category',
            y='Score',
            color='Device',
            barmode='group',
            title='Desktop vs Mobile Comparison'
        )

        return fig
    except KeyError as e:
        st.error(f"Error creating comparison chart: Missing data for {str(e)}")
        return None