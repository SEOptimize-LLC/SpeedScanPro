import streamlit as st
from datetime import datetime

def generate_report(url: str, desktop_results: dict, mobile_results: dict) -> str:
    """Generate an HTML report from the analysis results"""
    
    report = f"""
    <html>
    <head>
        <title>SEO Audit Report - {url}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background-color: #f8f9fa; padding: 20px; }}
            .metric {{ margin: 20px 0; }}
            .score {{ font-size: 24px; font-weight: bold; }}
            .good {{ color: green; }}
            .average {{ color: orange; }}
            .poor {{ color: red; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SEO Audit Report</h1>
            <p>URL: {url}</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <h2>Desktop Performance</h2>
        <div class="metric">
            <h3>Performance Score</h3>
            <div class="score {get_score_class(desktop_results['lighthouse_result']['categories']['performance']['score'])}">
                {int(desktop_results['lighthouse_result']['categories']['performance']['score'] * 100)}%
            </div>
        </div>
        
        <h2>Mobile Performance</h2>
        <div class="metric">
            <h3>Performance Score</h3>
            <div class="score {get_score_class(mobile_results['lighthouse_result']['categories']['performance']['score'])}">
                {int(mobile_results['lighthouse_result']['categories']['performance']['score'] * 100)}%
            </div>
        </div>
    </body>
    </html>
    """
    return report

def get_score_class(score: float) -> str:
    """Return CSS class based on score"""
    if score >= 0.9:
        return "good"
    elif score >= 0.5:
        return "average"
    return "poor"
