# GOAL OF THIS REPO 


To make a complete pipline for getting data from stock market and other indices via API's. Then make calculated predictions on the same .

Then use this to make informed decisions on buying and selling . We hope to apply back_testing methodologies.


Icing on the cake would be a nice WEB UI where we can easily see all this in a Human readable form.


# Related links

- https://github.com/NayakwadiS/mftool
- 
- GET_DATA , scripts for getting realtime data
- VISUALIZATION , gui for plotting the data
- BACK_TESTING

  ON THE TRADDING DAY WE PLAN TO ENTER AT 2% , WITH STOP LOSS AT CURRENT_MKT_PRICE - 2%

  - Prvious day , use filters to select the stocks
    - 1st I select stocks with market capitalisation more than 5000 crores.
    - Find the average and standard deviations of last 10 days.
    - Then 1 find the top 10 percentile of the average, 1 week change.
    - 2 WEEK AGO CHANGE , TOP 20% PERCENTILE
    - MONTH AGO CHANGE , TOP 20%
  - ARIMA
  - SARIMAX statistical model belonging to a class of models that explains a given time series based on its own past values -i.e.- its own lags and the lagged forecast errors. The SARIMAX model has complex mathematical equations that can be used to forecast future values. This model differs from other models such as ARIMA and SARIMA as it takes account of exogenous variables, or in other words, use external data in forecasting. Some real-world examples of exogenous variables include gold price, oil price, outdoor temperature, exchange rate.There are certain conditions in order before this model can be conducted. We need to understand whether the time series can be established as 'stationary'.
    - This means whether the time series has:
      - (a) constant mean,
      - (b) it should have constant variance or standard deviation, and
      - (c) auto-covariance should not depend on time.The time series needs to be stationary to allow forecasting to be computed accurately.
    - There are two ways to check for stationarity of a time series:
      - (1) rolling statistics, and
      - (2) Augmented Dickey-Fuller (ADF) test.
    - Before we establish whether the data is stationary, we need to understand the time series by decomposing into several components:
      - (1) trend
      - (2) seasonality
      - (3) random noise (residuals).
- CONFIG

  - entry
  - stop_loss
- 

### GIT COMMANDS

To commit your changes

```
git add .
git commit -m "change you are making"
git push

```

To pull the latest changes from the repo

```
git pull
```
