# Stock-Web-Application

<br>

## For users, please go directly to [this tutorial](https://github.com/cathyzjc/stock-application/blob/main/README.md#part-four----how-to-use-it)

<br>     
          
<br>          

## Part One.  General Introduction

This is a Python project to create your own stock dashboard and have a prediction on tomorrow's stock price. Stocks are all traded on the Shanghai Stock Exchange and the Shenzhen Stock Exchange in China. [More Information about stock inluded](https://en.wikipedia.org/wiki/CSI_300_Index)
In this project, I created two dashboards to interactively analyze and visualize specific stock data you pick.

#### 1. Stock Price Visualization
The first dashboard is about the stock price. In this Dashboard, three tabs are shown to present a 1-day candlestick plot, 1-week candlestick plot and 1-month candlestick plot. **Moving average** lines are also provided here. You can choose a moving average of 5, 10, 20 or 30. Multiple lines can be applied at the same time.

#### 2. Stock Prediction
The second dashboard is about a prediction model of this stock. An Auto ARIMA model from **pmdarima package** is used here to have a real-time prediction of tomorrow's stock price. 

#### 3.  The Layout of This Web Application
Here is a quick gif to show the layout of the whole application.
![img](https://github.com/cathyzjc/stock-application/blob/main/image/layout.gif)

The [wireframe](https://github.com/cathyzjc/stock-application/blob/main/Wireframe%20of%20Stock%20Application%20.pdf) and [a png format layout](https://github.com/cathyzjc/stock-application/blob/main/stock%20-%20layout.PNG) of this application is also included in Github. 
 
 <br>
 
 <br>
 
## Part Two.   Real-time Data 

[Baostock Python API](http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5) is used here to get the real-time securities data in this application.

Baostock is a free and open-source securities data platform (no registration required). It provides a large amount of accurate and complete securities historical market data, listed company financial data, etc. of the Chinese stock market. 
Users can obtain securities data information through python API, which meets the data needs of quantitative trading investors, quantitative finance enthusiasts, and econometrics practitioners.

Because we use a Python API here, the connection is not so stable all the time. So **please be patient and refresh your browser a few times when an error occurs.**

<br>

<br>

## Part Three.   Code Explanation

1. [app.py](https://github.com/cathyzjc/stock-application/blob/main/app.py) : The main python file of this whole application. Contains layout and callbacks.

2. [controls.py](https://github.com/cathyzjc/stock-application/blob/main/controls.py) : Define most of the functions used in app.py.

3. [prediction.py](https://github.com/cathyzjc/stock-application/blob/main/prediction.py) : Define ARIMA related functions in this python file.

4. [Test_controls.py](https://github.com/cathyzjc/stock-application/blob/main/Test_controls.py): This project is a test-driven project. 

<br>

<br>

## Part Four.    How To Use It?

#### 1. Setup
1. Clone this repo locally.
2. Create a local python 3.8 environment and install all packages shown below.
   > - **Dash:** dash, dash_core_components, dash_bootstrap_components, dash_html_components
   > - **Time Series Data & Prediction Model:** datetime, plotly, pandas, numpy, sklearn, pmdarima
   > - **Test-Driven:** pytest
   > - **Real-time Stock Data:** baostock
3. Run python3 app.py

#### 2. Video Tutorial

Here is a short video to show how you can use this web application

[![Watch the video](https://github.com/cathyzjc/stock-application/blob/main/image/Stock%20Predicting%20Application.png)](https://youtu.be/EaD8qFEvQPU)
