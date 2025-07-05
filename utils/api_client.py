import requests
import streamlit as st
import os

class PageSpeedInsightsAPI:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.api_key = os.environ.get("PAGESPEED_API_KEY")
        if not self.api_key:
            raise Exception("PageSpeed API key not found. Please set the PAGESPEED_API_KEY environment variable.")

        # Define a legitimate browser user agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    @staticmethod
    @st.cache_data(ttl=3600, show_spinner=False)
    def _fetch_metrics(base_url: str, api_key: str, url: str, strategy: str = "desktop", headers: dict = None):
        """
        Cached function to fetch PageSpeed Insights metrics
        """
        params = {
            'url': url,
            'strategy': strategy,
            'category': ['performance', 'accessibility', 'best-practices', 'seo'],
            'key': api_key
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Check if we have the lighthouse results
            if 'lighthouseResult' not in data:
                raise Exception("Invalid API response: No lighthouse results found")

            # Get categories with proper error handling
            categories = data['lighthouseResult']['categories']

            # Standardize the response format
            result = {
                'lighthouse_result': {
                    'categories': {},
                    'audits': {}
                }
            }

            # Process categories with flexible key matching
            category_keys = {
                'performance': ['performance'],
                'accessibility': ['accessibility'],
                'best-practices': ['best-practices', 'bestPractices'],
                'seo': ['seo']
            }

            for our_key, possible_keys in category_keys.items():
                found = False
                for api_key in possible_keys:
                    if api_key in categories:
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': categories[api_key]['score']
                        }
                        found = True
                        break
                if not found:
                    # Try alternative key formats
                    kebab_key = our_key.replace('_', '-')
                    camel_key = ''.join(word.capitalize() if i > 0 else word 
                                      for i, word in enumerate(our_key.split('-')))
                    if kebab_key in categories:
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': categories[kebab_key]['score']
                        }
                    elif camel_key in categories:
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': categories[camel_key]['score']
                        }
                    else:
                        available_keys = ', '.join(categories.keys())
                        raise Exception(f"Missing category in API response. Looking for '{our_key}' but found: {available_keys}")

            # Process audits
            audits = data['lighthouseResult'].get('audits', {})
            required_audits = [
                'first-contentful-paint',
                'interactive',
                'largest-contentful-paint',
                'cumulative-layout-shift',
                'total-blocking-time',
                'server-response-time',
                'interaction-to-next-paint'
            ]

            for audit_key in required_audits:
                if audit_key in audits:
                    result['lighthouse_result']['audits'][audit_key] = {
                        'displayValue': audits[audit_key].get('displayValue', 'N/A')
                    }

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch metrics: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def get_metrics(self, url: str, strategy: str = "desktop"):
        """
        Public method to get PageSpeed Insights metrics
        """
        return self._fetch_metrics(self.base_url, self.api_key, url, strategy, self.headers)