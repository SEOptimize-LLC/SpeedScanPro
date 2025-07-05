# SEO Audit Tool 🔍

A powerful web application built with Streamlit that performs comprehensive SEO analysis using Google PageSpeed Insights API. The tool analyzes websites for both desktop and mobile performance metrics.

## Features

- **Single URL Analysis**: Analyze individual websites
- **Bulk URL Processing**: Upload multiple URLs for batch analysis
- **Comprehensive Metrics**: 
  - Performance Score
  - Accessibility Score
  - Best Practices Score
  - SEO Score
- **Multi-Platform Analysis**:
  - Desktop metrics
  - Mobile metrics
- **Export Options**:
  - JSON format
  - CSV format
  - Excel format

## Requirements
python
streamlit
pandas
xlsxwriter

## Setup

1. Clone the repository
2. Install the required dependencies:
3. Set up your Google PageSpeed Insights API key in the environment variables

## Usage

1. Run the application:
2. Access the tool through your web browser (typically http://localhost:8501)

3. You can analyze websites in two ways:
   - Enter a single URL in the text input field
   - Upload a file containing multiple URLs for bulk analysis

4. Click the "🚀 Analyze Websites" button to start the analysis

5. View the results and export them in your preferred format (JSON/CSV/Excel)

## Features in Detail

### URL Validation
- Automatically validates URLs before processing
- Supports both HTTP and HTTPS protocols
- Handles localhost and IP addresses

### Analysis Results
- Real-time progress tracking
- Expandable results view for each URL
- Comprehensive metrics display
- Error handling with detailed feedback

### Export Functionality
- JSON export with detailed metrics
- CSV export with flattened data structure
- Excel export with formatted spreadsheet

## Error Handling

The application handles various types of errors:
- API configuration issues
- Network connectivity problems
- Invalid API responses
- General runtime errors

## UI Features

- Modern gradient background
- Responsive design
- Interactive buttons with hover effects
- Collapsible sidebar
- Progress indicators
- Clean, organized data presentation

## Technical Notes

- Uses caching for improved performance
- Asynchronous processing for better response times
- Modular component structure
- Comprehensive error logging for debugging

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license information here]

## Support

For API key setup and other configuration support, please contact the support team.
