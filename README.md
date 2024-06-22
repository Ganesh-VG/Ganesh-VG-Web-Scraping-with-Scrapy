# Web Scraping With Scrapy

### Overview

This project aims to extract information from a news website using web scraping techniques with Python and Scrapy. The extracted data is then stored in a JSON format for further analysis or processing.

### Features

- **Web Scraping**: Utilizes Scrapy, a powerful web crawling and scraping framework in Python, to extract structured data from the news website.
- **Data Extraction**: Extracts various pieces of information such as article titles, authors, publication dates, and article content from the website.
- **JSON Output**: Stores the extracted data into a JSON file format, making it easy to parse and analyze the information later.

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Ganesh-VG/Web-Scraping-with-Scrapy.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Web-Scraping-with-Scrapy
   ```

3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the Scrapy spider to start scraping the news website:

   ```bash
   scrapy crawl news_scraper
   ```

2. Or you can just run the main.py file present in the repository

3. Once the scraping is complete, the extracted data will be stored in a file named `livemint_articles.json` in the project directory.

### Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this explanation to fit the specifics of your project!
