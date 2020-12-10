# stock-web-application

## Part One.  General Introduction

This is a Python project to create your own stock dashboard and have a prediction on tomorrows stock price.
In this project I created two dashboard to interactively analyse and visualize specific stock data.
#### 1. Stock Price Visualization
The first dashboard is about stock prices. In this Dashboard, three tabs are shown to present 1-day candlestick plot, 1-week candlestick plot and 1-month candlestick plot. Moving average lines are also provided here. You can choose moving average of 5, 10, 20 or 30. Mulitple lines can be applied at the same time.

#### 2. Stock Prediction
The second dashboard is about a prediction model of this stock. An Auto ARIMA model from pmdarima package is used here to have a real-time prediction of tomorrow's stock price. 

#### 3.  The Layout of This Web Application
Here is a quick gif to show the layout of the whole application.
![img](https://github.com/cathyzjc/stock-application/blob/main/image/layout.gif)

The [wireframe](https://github.com/cathyzjc/stock-application/blob/main/Wireframe%20of%20Stock%20Application%20.pdf) and [a png format layout](https://github.com/cathyzjc/stock-application/blob/main/stock%20-%20layout.PNG) of this application is also included in Github. 
 
 
## Part Two.   Real-time Data 

[Baostock Python API](http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5) is used here to get the real-time securities data in this application.

Baostock is a free and open source securities data platform (no registration required). It provides a large amount of accurate and complete securities historical market data, listed company financial data, etc. of Chinese stock market. 
Users can obtain securities data information through python API, which meets the data needs of quantitative trading investors, quantitative finance enthusiasts, and econometrics practitioners.

Because we use an Python API here, the connection is not so stable all the time. So **please be patient and refresh your browser a few times when an error occurs.**

## Part Three.   Code Explanation

1. [app.py](https://github.com/cathyzjc/stock-application/blob/main/app.py) : The main python file of this whole application. Contains layout and callbacks.

2. [controls.py](https://github.com/cathyzjc/stock-application/blob/main/controls.py) : Define most of the functions used in app.py.

3. [prediction.py](https://github.com/cathyzjc/stock-application/blob/main/prediction.py) : Define ARIMA related functions in this python file.

4. [Test_controls.py](https://github.com/cathyzjc/stock-application/blob/main/Test_controls.py): This project is a test-driven project. 

## Part Four. How To Use It?
[![Watch the video](https://github.com/cathyzjc/stock-application/blob/main/image/Stock%20Predicting%20Application.png)](https://youtu.be/EaD8qFEvQPU)
