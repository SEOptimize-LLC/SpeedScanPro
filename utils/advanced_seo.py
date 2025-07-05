
import bs4
from bs4 import BeautifulSoup
from collections import Counter
from typing import Dict, List, Tuple
import re
import requests
from urllib.parse import urljoin, urlparse

class AdvancedSEOAnalyzer:
    def analyze_keyword_density(self, text: str) -> Dict[str, float]:
        """Calculate keyword density for 1-3 word phrases"""
        words = re.findall(r'\w+', text.lower())
        total_words = len(words)
        
        # Single word density
        singles = Counter(words)
        
        # 2-3 word phrases
        phrases = []
        for i in range(len(words)-1):
            phrases.append(' '.join(words[i:i+2]))
            if i < len(words)-2:
                phrases.append(' '.join(words[i:i+3]))
        
        phrase_density = Counter(phrases)
        
        # Calculate percentages
        density = {}
        for word, count in singles.most_common(10):
            density[word] = (count / total_words) * 100
            
        for phrase, count in phrase_density.most_common(10):
            density[phrase] = (count / (total_words - len(phrase.split()) + 1)) * 100
            
        return density

    def analyze_headings(self, html: str) -> Dict[str, List[str]]:
        """Analyze heading structure"""
        soup = BeautifulSoup(html, 'html.parser')
        headings = {}
        
        for i in range(1, 7):
            tag = f'h{i}'
            headings[tag] = [h.text.strip() for h in soup.find_all(tag)]
            
        return headings

    def check_images(self, html: str) -> List[Dict[str, str]]:
        """Check image alt texts"""
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt', '').strip())
            })
            
        return images

    def validate_schema(self, html: str) -> Dict[str, List[str]]:
        """Validate schema markup"""
        soup = BeautifulSoup(html, 'html.parser')
        schemas = {
            'json-ld': [],
            'microdata': [],
            'rdfa': []
        }
        
        # Check JSON-LD
        scripts = soup.find_all('script', type='application/ld+json')
        schemas['json-ld'] = [s.string for s in scripts if s.string]
        
        # Check microdata
        microdata = soup.find_all(itemscope=True)
        schemas['microdata'] = [str(m) for m in microdata]
        
        # Check RDFa
        rdfa = soup.find_all(property=True)
        schemas['rdfa'] = [str(r) for r in rdfa]
        
        return schemas

    def analyze_links(self, html: str, base_url: str) -> Dict[str, List[Dict[str, str]]]:
        """Analyze internal and external links"""
        soup = BeautifulSoup(html, 'html.parser')
        base_domain = urlparse(base_url).netloc
        
        internal_links = []
        external_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            absolute_url = urljoin(base_url, href)
            domain = urlparse(absolute_url).netloc
            
            link_info = {
                'url': absolute_url,
                'text': link.text.strip(),
                'nofollow': 'nofollow' in link.get('rel', [])
            }
            
            if domain == base_domain:
                internal_links.append(link_info)
            else:
                external_links.append(link_info)
                
        return {
            'internal': internal_links,
            'external': external_links
        }
