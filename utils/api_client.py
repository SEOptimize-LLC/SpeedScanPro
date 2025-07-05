import requests
import streamlit as st
import os

class PageSpeedInsightsAPI:
    def __init__(self, api_key=None):
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.api_key = api_key
        if not self.api_key:
            raise Exception("API key not provided. Please provide a valid PageSpeed Insights API key.")

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

        response = None
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

            # Process categories with flexible key matching and safe score handling
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
                        # Safe score extraction
                        category_data = categories[api_key]
                        if category_data is None:
                            score = None
                        elif isinstance(category_data, dict) and 'score' in category_data:
                            score = category_data['score']
                        else:
                            score = None
                            
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': score if score is not None else 0
                        }
                        found = True
                        break
                        
                if not found:
                    # Try alternative key formats
                    kebab_key = our_key.replace('_', '-')
                    camel_key = ''.join(word.capitalize() if i > 0 else word 
                                      for i, word in enumerate(our_key.split('-')))
                    
                    if kebab_key in categories:
                        category_data = categories[kebab_key]
                        score = category_data.get('score', 0) if isinstance(category_data, dict) else 0
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': score if score is not None else 0
                        }
                    elif camel_key in categories:
                        category_data = categories[camel_key]
                        score = category_data.get('score', 0) if isinstance(category_data, dict) else 0
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': score if score is not None else 0
                        }
                    else:
                        # Set default score if category is missing
                        result['lighthouse_result']['categories'][our_key] = {
                            'score': 0
                        }
                        print(f"Warning: Category '{our_key}' not found. Available: {', '.join(categories.keys())}")

            # Process audits with safe handling
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
                if audit_key in audits and audits[audit_key] is not None:
                    audit_data = audits[audit_key]
                    result['lighthouse_result']['audits'][audit_key] = {
                        'displayValue': audit_data.get('displayValue', 'N/A'),
                        'score': audit_data.get('score', 0) if audit_data.get('score') is not None else 0
                    }
                else:
                    result['lighthouse_result']['audits'][audit_key] = {
                        'displayValue': 'N/A',
                        'score': 0
                    }

            return result

        except requests.exceptions.RequestException as e:
            # Check for common API key errors
            if response and response.status_code == 400:
                error_detail = response.json().get('error', {}).get('message', '')
                if 'API key not valid' in error_detail:
                    raise Exception("Invalid API key. Please check your PageSpeed Insights API key.")
                else:
                    raise Exception(f"Bad request: {error_detail}")
            elif response and response.status_code == 403:
                raise Exception("API key error: Access forbidden. Please ensure your API key has the necessary permissions.")
            else:
                raise Exception(f"Failed to fetch metrics: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid API response format: {str(e)}")
        except Exception as e:
            if "score" in str(e):
                # If it's a score-related error, return a result with default values
                print(f"Score error for {url}: {str(e)}")
                return {
                    'lighthouse_result': {
                        'categories': {
                            'performance': {'score': 0},
                            'accessibility': {'score': 0},
                            'best-practices': {'score': 0},
                            'seo': {'score': 0}
                        },
                        'audits': {
                            audit: {'displayValue': 'N/A', 'score': 0}
                            for audit in required_audits
                        }
                    }
                }
            else:
                raise Exception(f"An error occurred: {str(e)}")

    def get_metrics(self, url: str, strategy: str = "desktop"):
        """
        Public method to get PageSpeed Insights metrics
        """
        return self._fetch_metrics(self.base_url, self.api_key, url, strategy, self.headers)
