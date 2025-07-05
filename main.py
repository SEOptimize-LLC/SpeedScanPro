import streamlit as st
from utils.api_client import PageSpeedInsightsAPI
from utils.seo_analyzer import SEOAnalyzer
from components.metrics_display import display_metrics
from components.report_generator import generate_report
from components.bulk_upload import render_upload_section
import asyncio
import re
import traceback
import pandas as pd
import json
from typing import List, Dict
import io

# Page configuration
st.set_page_config(
    page_title="SEO Audit Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Light theme styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.2em;
        border: none;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def validate_url(url):
    """Validate URL format"""
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def analyze_url(api_client: PageSpeedInsightsAPI, url: str) -> Dict:
    """Analyze a single URL"""
    desktop_results = api_client.get_metrics(url, strategy="desktop")
    mobile_results = api_client.get_metrics(url, strategy="mobile")

    return {'url': url, 'desktop': desktop_results, 'mobile': mobile_results}


def export_results(results: List[Dict], format: str):
    """Export results in the specified format"""
    if format == 'json':
        return json.dumps(results, indent=2)

    # Flatten results for CSV/Excel with safe score handling
    flattened_data = []
    for result in results:
        def get_score(data, category):
            try:
                score = data['lighthouse_result']['categories'][category]['score']
                if score is None:
                    return 'N/A'
                return score * 100 if score > 0 else 0
            except (KeyError, TypeError):
                return 'N/A'
        
        row = {
            'URL': result['url'],
            'Desktop Performance': get_score(result['desktop'], 'performance'),
            'Desktop Accessibility': get_score(result['desktop'], 'accessibility'),
            'Desktop Best Practices': get_score(result['desktop'], 'best-practices'),
            'Desktop SEO': get_score(result['desktop'], 'seo'),
            'Mobile Performance': get_score(result['mobile'], 'performance'),
            'Mobile Accessibility': get_score(result['mobile'], 'accessibility'),
            'Mobile Best Practices': get_score(result['mobile'], 'best-practices'),
            'Mobile SEO': get_score(result['mobile'], 'seo')
        }
        flattened_data.append(row)

    df = pd.DataFrame(flattened_data)

    if format == 'csv':
        return df.to_csv(index=False)
    elif format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Analysis Results', index=False)
        return output.getvalue()


def main():
    # Simple header
    st.title("🔍 SEO Audit Tool")
    st.markdown("---")

    # API Key input
    api_key = st.text_input(
        "Enter your Google PageSpeed Insights API Key:",
        type="password",
        placeholder="Your API key here...",
        help="Get your API key from Google Cloud Console"
    )

    if not api_key:
        st.info("👆 Please enter your PageSpeed Insights API key to continue")
        st.markdown("""
        **How to get an API key:**
        1. Visit [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select existing one
        3. Enable PageSpeed Insights API
        4. Create credentials (API Key)
        5. Copy and paste the key above
        """)
        return

    # URL input section
    st.subheader("Enter URLs to Analyze")
    
    # Get URLs from bulk upload or single input
    urls = render_upload_section()
    single_url = st.text_input(
        "Or analyze a single URL:",
        placeholder="https://example.com"
    )

    if single_url:
        urls = [single_url]

    # Centered submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🚀 Analyze Websites")

    if urls and analyze_button:
        invalid_urls = [url for url in urls if not validate_url(url)]
        if invalid_urls:
            st.error(f"Invalid URLs found: {', '.join(invalid_urls)}")
            return

        with st.spinner("🔍 Analyzing websites..."):
            try:
                # Initialize API client with the provided API key
                api_client = PageSpeedInsightsAPI(api_key=api_key)
                all_results = []

                progress_bar = st.progress(0)
                for i, url in enumerate(urls):
                    with st.expander(f"Analyzing {url}", expanded=True):
                        try:
                            result = analyze_url(api_client, url)
                            all_results.append(result)
                            # Show individual results
                            display_metrics(result['desktop'], result['mobile'])
                        except Exception as e:
                            st.error(f"Error analyzing {url}: {str(e)}")
                    progress_bar.progress((i + 1) / len(urls))

                if all_results:
                    st.success(f"✅ Analysis completed for {len(all_results)} URLs")

                    # Export options
                    st.subheader("Export Results")
                    export_format = st.selectbox(
                        "Choose export format:",
                        ['json', 'csv', 'excel']
                    )

                    export_data = export_results(all_results, export_format)

                    if export_format == 'json':
                        st.download_button(
                            "📥 Download JSON Report",
                            export_data,
                            file_name="seo_audit_results.json",
                            mime="application/json"
                        )
                    elif export_format == 'csv':
                        st.download_button(
                            "📥 Download CSV Report",
                            export_data,
                            file_name="seo_audit_results.csv",
                            mime="text/csv"
                        )
                    else:  # excel
                        st.download_button(
                            "📥 Download Excel Report",
                            export_data,
                            file_name="seo_audit_results.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

            except Exception as e:
                error_msg = str(e)
                if "API key not found" in error_msg or "Invalid API key" in error_msg:
                    st.error("⚠️ Invalid API Key: Please check your PageSpeed Insights API key and try again.")
                elif "Failed to fetch metrics" in error_msg:
                    st.error("🌐 Network Error: Unable to fetch data from Google PageSpeed Insights. Please try again later.")
                elif "Invalid API response" in error_msg:
                    st.error("🚫 API Error: Received invalid response from PageSpeed Insights. Please try again later.")
                else:
                    st.error(f"❌ An unexpected error occurred: {error_msg}")

                # Log the full error for debugging
                with st.expander("Debug information"):
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
