# Stock Price Prediction Web App

## Introduction

This project aimed at creating machine learning models to predict whether the stock price for a given company would increase or decrease on a particular day. It is built on two random forest models and provides an interactive interface via a Flask web application for users to explore the predictions alongside valuable financial data.

## Features

- **Stock Price Prediction**: Predictions on whether the stock price will increase or decrease.
- **Stock Selection**: Option to choose from one of 17 stock tickers that the models were trained on.
- **Financial Information Display**: Retrieves and displays financial data of the selected company from the Alpha Vantage API, including ratio and technical analyses.
- **Stock Historical Data**: Graphs and displays stock information from the past 6 months using the Yahoo Finance API.
- **News Feed**: Scraped news articles related to the selected stock from the Finviz website.

## Installation/Setup

Installation and Setup are simple, as one only needs to download all of the relevant code and run the app.py file, after adding the necessary packages, which a list of can be found below. The one issue that might arise when trying to download the necessary files is the two machine learning models, which are quite large currently, but I am in the testing phase trying to decrease the file size without harming the model's accuracy. 

## Usage

1. Navigate to the Flask web application (Currently only Locally Hosted).
2. From the dropdown, select one of the 17 stock tickers.
3. The application will display the prediction for the day.
4. View the comprehensive financial data, 6-month stock history graph, and related news articles for informed decision-making.

## Technologies/APIs Used

- **Machine Learning**: Random Forest models.
- **Web Framework**: Flask.
- **APIs**: 
  - Alpha Vantage for financial information.
  - Yahoo Finance for historical stock data.
- **Web Scraping**: Finviz for news articles.

## Packages Used

- 

## Warnings/Disclaimers

1. **Twitter API Limitation**: Initially, this project was designed to incorporate tweets into the machine learning models and the web application. However, due to the termination of free services on the Twitter API, this feature is unavailable.
2. **Educational Purpose Only**: This project was designed and developed as a learning experience. The predictions and data provided should **not** be used for actual financial decision-making.
