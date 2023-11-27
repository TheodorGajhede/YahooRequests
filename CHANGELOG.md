
## YahooRequests Changelog

### Version 1.11 (November 27, 2023)

- Added ability to find historical data for any company.
- Added method to calculate average price of a company in a given time range using new history tool.
- Fixed docstring and documentation errors for history feature.
- Added docs.md file with more detailed explanations of parameters and formatting.
- Added apikeys.csv file to allow users to use their own API keys (developer-provided keys will be used - if file is not edited).
- Updated all docstrings to follow new formatting with parameters, raises, and returns.
- Updated workflow file with caching and better dependencies.
- Updated News method to use the NewsApi Python API instead of requests.
- Updated News to use new search method for new articles.
- Slight changes to README file.

### Version 1.1 (September 12, 2023)

- Added feature to display comprehensive table of essential information.
- Added ability to convert stock data to alternative currencies using .price method.
- Added "remove suffix" function to eliminate common company suffixes such as Co. or Inc.
- Enhanced unit testing for improved code reliability.
- Organized code into separate YAML files to improve readability of codebase.
- Improved handling and reporting of exceptions, particularly the ConvertError.
- Resolved error-handling issues across multiple methods.
- Rectified typographical errors in README file.
- Added .gitignore for version control.
- Added poetry.lock for dependency management.
- Beta: Added News feature to generate articles related to selected companies, though its reliability may vary.

### Version 1.0 Rewrite (August 01, 2023)

- Updated project structure to adhere to a more modern setup type.
- Significantly reduced code duplication to improve codebase efficiency.
- Streamlined the process of updating the codebase.
- Introduced a new YAML configuration file for improved configuration management.
- Eliminated erroneous global variables.
- Removed duplicate licenses to improve code clarity.
- Special thanks to u/Diapolo10 for valuable technical support.

#### Please note that versions 0.1.5.X, 0.1.4, 0.1.3, 0.1.2, and 0.1.1 are either outdated, broken, or test versions, and are not recommended for use.