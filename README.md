# README.md

## Project Title

Web Scraper

## Introduction

This README provides essential information for setting up and running the Web Scraper application. Before you begin, make sure you have the necessary prerequisites in place.

## Prerequisites

Before you can run the Web Scraper application, you need to ensure you have the following prerequisites installed on your system:

- Python (3.10 or higher)
- pip (Python package manager)

To install the required Python packages, navigate to the project directory and run the following command:

```shell
pip install -r requirements.txt
```

Additionally, Web Scraper relies on the `wkhtmltopdf` tool for generating PDFs. If you are using Ubuntu, you can install it using the following command:

```shell
sudo apt-get install wkhtmltopdf
```

## Usage

Before running the Web Scraper application, ensure you have the necessary prerequisites installed on your system. Refer to the "Prerequisites" section for details.

### Scraping and Saving URLs as PDFs

To start scraping and recursively saving URLs as PDFs, use the following command:

```shell
python scraper.py <base url>
```

Replace `<base url>` with the URL you want to use as the root for your scraping task. The application will start from the provided URL and recursively follow links on the pages to save them as PDFs.

### Scraping URLs from a File

You can also scrape URLs from a file and save them as PDFs. To do this, use the following command:

```shell
python scraper.py --urls-to-dump <file_name>
```

Replace `<file_name>` with the name of the file containing the list of URLs to be saved as PDFs.

### Scraping and Saving URLs from a File as PDFs

To scrape and save URLs from a file as PDFs, use the following command:

```shell
python scraper.py --urls-to-dump <file_name>
```

Replace `<file_name>` with the name of the file containing a list of URLs to save as PDFs. The application will process each URL in the file and save them as PDFs without scraping additional reference links.

## Examples

Here are a few example commands for running the Web Scraper application:

### Scraping and Saving URLs as PDFs

```shell
python scraper.py https://example.com
python scraper.py https://anotherwebsite.com
```

### Scraping and Saving URLs from a File as PDFs

Here is an example command for running the Web Scraper application to save URLs from a file as PDFs:

```shell
python scraper.py --urls-to-dump=my_urls.txt
```

In this example, the `my_urls.txt` file should contain a list of URLs you want to save as PDFs. The application will process each URL in the file and save them as PDFs.

Please adjust the command and file name to match your specific use case. Ensure you have installed the required Python packages and the `wkhtmltopdf` tool as mentioned in the "Prerequisites" section before running the application.