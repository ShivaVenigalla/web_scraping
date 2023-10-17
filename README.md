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

Once you have met all the prerequisites, you can run the Web Scraper application with the following command:

```shell
python scraper.py <base url>
```

Replace `<base url>` with the URL you want to use as the starting point for your scraping task.

## Examples

Here are a few example commands for running the Web Scraper application:

```shell
python scraper.py https://example.com
python scraper.py https://anotherwebsite.com
```