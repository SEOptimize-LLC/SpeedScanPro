
import streamlit as st
import pandas as pd
from utils.visualization import create_score_gauge, create_comparison_chart

def display_metrics(desktop_results: dict, mobile_results: dict):
    """Display the analysis metrics with visualizations"""
    
    # Create tabs for overview and detailed metrics
    tab1, tab2, tab3 = st.tabs(["Overview", "Desktop Metrics", "Mobile Metrics"])

    with tab1:
        st.markdown("""
        <style>
        .metric-container {
            background: rgba(17, 25, 40, 0.75);
            backdrop-filter: blur(16px);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.125);
        }
        .metric-table {
            width: 100%;
            background: rgba(30, 35, 41, 0.75);
            border-radius: 8px;
            margin: 10px 0;
        }
        .metric-table th, .metric-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Performance Overview")
        comparison_chart = create_comparison_chart(desktop_results, mobile_results)
        st.plotly_chart(comparison_chart, use_container_width=True)

    def display_detailed_metrics(results, device_type):
        performance = results['lighthouse_result']['categories']['performance']['score']
        metrics = results['lighthouse_result']['audits']
        categories = results['lighthouse_result']['categories']
        
        col1, col2 = st.columns([1, 1])
        with col1:
            fig = create_score_gauge(performance, f"{device_type} Performance Score")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Performance Metrics")
        metrics_df = pd.DataFrame({
            "Metric": [
                "First Contentful Paint (FCP)",
                "Largest Contentful Paint (LCP)",
                "Time to First Byte (TTFB)",
                "Time to Interactive (TTI)",
                "Total Blocking Time (TBT)",
                "Interaction to Next Paint (INP)",
                "Cumulative Layout Shift (CLS)"
            ],
            "Value": [
                metrics['first-contentful-paint']['displayValue'],
                metrics['largest-contentful-paint']['displayValue'],
                metrics['server-response-time']['displayValue'],
                metrics['interactive']['displayValue'],
                metrics['total-blocking-time']['displayValue'],
                metrics.get('interaction-to-next-paint', {}).get('displayValue', 'N/A'),
                metrics['cumulative-layout-shift']['displayValue']
            ],
            "Score": [
                f"{int(metrics['first-contentful-paint']['score'] * 100)}%",
                f"{int(metrics['largest-contentful-paint']['score'] * 100)}%",
                f"{int(metrics['server-response-time']['score'] * 100)}%",
                f"{int(metrics['interactive']['score'] * 100)}%",
                f"{int(metrics['total-blocking-time']['score'] * 100)}%",
                "N/A",
                f"{int(metrics['cumulative-layout-shift']['score'] * 100)}%"
            ]
        })
        st.table(metrics_df.style
                .set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                    'padding': '12px',
                    'background-color': 'transparent'
                })
                .set_table_styles([{
                    'selector': 'td, th',
                    'props': [
                        ('background-color', 'transparent'),
                        ('color', 'white'),
                        ('border-bottom', '1px solid rgba(255, 255, 255, 0.1)')
                    ]
                }]))

        st.markdown("### Overall Scores")
        scores_df = pd.DataFrame({
            "Category": ["Performance", "SEO", "Accessibility", "Best Practices"],
            "Score": [
                f"{int(categories['performance']['score'] * 100)}%",
                f"{int(categories['seo']['score'] * 100)}%",
                f"{int(categories['accessibility']['score'] * 100)}%",
                f"{int(categories['best-practices']['score'] * 100)}%"
            ]
        })
        st.table(scores_df.style
                .set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                    'padding': '12px',
                    'background-color': 'transparent'
                })
                .set_table_styles([{
                    'selector': 'td, th',
                    'props': [
                        ('background-color', 'transparent'),
                        ('color', 'white'),
                        ('border-bottom', '1px solid rgba(255, 255, 255, 0.1)')
                    ]
                }]))

    with tab2:
        display_detailed_metrics(desktop_results, "Desktop")

    with tab3:
        display_detailed_metrics(mobile_results, "Mobile")
