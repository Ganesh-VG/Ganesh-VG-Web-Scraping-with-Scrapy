# News Scraper

## Project Description

News Scraper is a web scraping project built using Scrapy to extract articles from various news websites. The extracted data includes article URLs, titles, publication dates, authors, and content. The data is saved in JSON files categorized by the website from which they were scraped.

## Features

- Scrapes multiple news websites sequentially.
- Extracts and saves articles in JSON format.
- Organizes scraped data by website.
- Configurable through a text file containing URLs.

## Setup Instructions

### Prerequisites

- Python 3.x
- Scrapy

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Ganesh-VG/Web-Scraping-with-Scrapy
    cd Web-Scraping-with-Scrapy
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Configuration

- **config.txt**: Add the list of URLs to be scraped in this file, one URL per line.
- **settings.py**: Adjust the Scrapy settings as needed.

### Directory Structure

```sh
Web-Scraping-with-Scrapy/
├── config.txt
├── main.py
├── news_spider.py
├── pipelines.py
├── requirements.txt
└── JSON_files/
```

## Usage

1. Add URLs to `config.txt`.

2. Run the scraper:

    ```sh
    python main.py
    ```

3. The scraped data will be saved in JSON files in the `JSON_files` directory, categorized by the website name.

4. If you want to run spider on single url:

    ```sh
    scrapy crawl getnews -a url=<Input URL>  
    ```

## Example

An example of a URL in `config.txt`:

https://www.livemint.com/
https://economictimes.indiatimes.com/

After running the scraper, JSON files will be created for each website:

JSON_files/
├── livemint_articles.json
├── economictimes_articles.json

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Submit a pull request.

