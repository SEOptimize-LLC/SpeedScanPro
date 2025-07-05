import trafilatura
from typing import Dict, Any
import streamlit as st

from .advanced_seo import AdvancedSEOAnalyzer

class SEOAnalyzer:
    def __init__(self):
        self.advanced = AdvancedSEOAnalyzer()

    @st.cache_data(ttl=3600)
    def analyze_content(self, url: str) -> Dict[str, Any]:
        """Analyze on-page SEO elements"""
        try:
            downloaded = trafilatura.fetch_url(url)
            text_content = trafilatura.extract(downloaded)
            html_content = downloaded
            
            # Basic content analysis
            word_count = len(text_content.split()) if text_content else 0
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(downloaded)
            
            # Advanced analysis
            keyword_density = self.advanced.analyze_keyword_density(text_content) if text_content else {}
            headings = self.advanced.analyze_headings(html_content) if html_content else {}
            images = self.advanced.check_images(html_content) if html_content else []
            schemas = self.advanced.validate_schema(html_content) if html_content else {}
            links = self.advanced.analyze_links(html_content, url) if html_content else {'internal': [], 'external': []}
            
            return {
                'word_count': word_count,
                'title': metadata.title if metadata else None,
                'description': metadata.description if metadata else None,
                'language': metadata.language if metadata else None,
                'text_content': text_content,
                'keyword_density': keyword_density,
                'headings': headings,
                'images': images,
                'schemas': schemas,
                'links': links
            }
        except Exception as e:
            raise Exception(f"Content analysis failed: {str(e)}")
