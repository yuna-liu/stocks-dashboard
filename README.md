# stocks - Dashboard

---
Stocks: Apple(AAPL), IBM(IBM), Nvidia(NVDA), and Tesla(TSLA) 

Created dashboard with main functionality in place: 

- choose stock 
- filter time 
- filter OHLC options - open, high, low, close

Note that we use local csv-files for this example and not API calls. 

## Intermediate storage

In this update we use the client-side storage, i.e. the user's browser for storing JSON data after filtering. After filtering this intermediate storage is then used for multiple callbacks such as updating the graph and updating highest and lowest values. We use the **dcc.Store** component for doing this.

## Styling dash app

For styling this app we mostly used dash bootstrap components, but also some minor css-styling. TODO: fix minor responsiveness with mobile version.

## Deployment

Deploy dashboard on Heroku app: 
[https://stocky-dashboard.herokuapp.com/](https://stocky-dashboard.herokuapp.com/)