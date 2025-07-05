import streamlit as st
import pandas as pd
from typing import List
import io

def parse_text_urls(content: str) -> List[str]:
    """Parse URLs from text content"""
    return [url.strip() for url in content.split('\n') if url.strip()]

def parse_uploaded_file(uploaded_file) -> List[str]:
    """Parse URLs from uploaded file based on file type"""
    if uploaded_file is None:
        return []

    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == 'txt':
            content = uploaded_file.getvalue().decode()
            return parse_text_urls(content)
        elif file_type == 'csv':
            df = pd.read_csv(uploaded_file)
            return df.iloc[:, 0].tolist()  # Assume URLs are in the first column
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
            return df.iloc[:, 0].tolist()  # Assume URLs are in the first column
        else:
            st.error(f"Unsupported file type: {file_type}")
            return []
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
        return []

def show_url_preview(urls: List[str], max_preview: int = 5) -> None:
    """Show preview of URLs to be analyzed"""
    if not urls:
        st.warning("No URLs found in the uploaded file.")
        return

    st.subheader("URL Preview")
    preview_df = pd.DataFrame({"URLs": urls})

    with st.expander(f"Preview ({len(urls)} URLs found)"):
        st.dataframe(
            preview_df.head(max_preview),
            use_container_width=True
        )
        if len(urls) > max_preview:
            st.info(f"Showing first {max_preview} of {len(urls)} URLs")

def render_upload_section():
    """Render the bulk upload section"""
    st.markdown("""
    <h2 class="section-title">Bulk URL Analysis</h2>
    <div style='background: rgba(30, 35, 41, 0.75); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.1);'>
        <p style='color: white; text-align: center;'>Upload a file containing URLs to analyze multiple websites at once.</p>
        <div class="feature-grid">
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <span class="feature-text">CSV file (URLs in first column)</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📑</span>
                <span class="feature-text">Excel file (URLs in first column)</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📝</span>
                <span class="feature-text">Text file (one URL per line)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload file containing URLs",
        type=['csv', 'xlsx', 'xls', 'txt'],
        help="Upload a file containing URLs to analyze"
    )

    # Manual URL input
    manual_urls = st.text_area(
        "Or enter URLs manually (one per line)",
        height=100,
        help="Enter URLs manually, one URL per line"
    )

    urls = []
    if uploaded_file:
        urls = parse_uploaded_file(uploaded_file)
    elif manual_urls:
        urls = parse_text_urls(manual_urls)

    if urls:
        show_url_preview(urls)

    return urls