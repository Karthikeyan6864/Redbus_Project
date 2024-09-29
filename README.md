# RedBus Data Scraper and Visualization

## Project Overview
This project is an automated data scraping solution that extracts bus-related information from the RedBus website using the Selenium library. The scraped data is stored in a MySQL database. We then use this database to create an interactive website built with Streamlit, which provides filtered datasets and visualizations, helping users make informed decisions in a user-friendly environment.

## Features

### Automated Data Scraping:
- Uses Selenium to extract real-time data from RedBus, including bus routes, prices, durations, bus types, and more.
- Handles dynamic web elements and multi-page data scraping.

### Database Storage:
- Data is stored in a MySQL database for efficient retrieval and analysis.
- Ensures scalability and persistence of data.

### Interactive Web Application:
- Built with Streamlit to visualize bus-related information.
- Allows users to filter data by bus type, route, price, and other attributes.
- Provides detailed visualizations such as bar charts, scatter plots, pie charts, and histograms to enhance decision-making.

## Technologies Used
- **Selenium**: For web scraping from RedBus.
- **MySQL**: For storing the scraped data.
- **Pandas**: For data manipulation and filtering.
- **Plotly**: For creating interactive and dynamic visualizations.
- **Streamlit**: For building the user-friendly web application interface.
- **Python**: Core language used for automation, scraping, and data handling.

## How It Works

### Data Scraping:
- The project uses Selenium to automate browsing on the RedBus website, scrape relevant information like bus name, price, star rating, bus type, etc.
- The scraped data is processed and converted into a structured format.

### Database Setup:
- The processed data is stored in a MySQL database with appropriate schema design.
- The database can be queried for data retrieval and analysis.

### Web Application:
- The Streamlit-based web app provides a clean interface for users to interact with the data.
- Users can filter results based on multiple criteria such as route, bus type, rating, and duration.
- Visualizations such as scatter plots, bar charts, and pie charts help users analyze trends and pricing.

## Usage
- The web application provides various options to filter data, visualize bus types, prices, and star ratings.
- Users can explore the price distribution, seat availability, and other important metrics before choosing the right bus for their journey.

## Future Improvements
- **Automation**: Schedule the scraping script to run at regular intervals to keep the data updated.
- **Advanced Filtering**: Add more granular filtering options based on user feedback.
- **Additional Visualizations**: Introduce more complex visualizations, such as geographic mapping of routes.

## Acknowledgments
- Thanks to RedBus for providing the platform to gather bus data.
- Special thanks to the maintainers of Selenium, Streamlit, and other libraries used in this project.

