bitcoin-pos
===========

Point-of-sale system for bitcoin.  

Hardware:
raspberri pi,
thermal printer,
2.8" touch screen

Code:
The software is designed to be used in a restaurant/bar.  Transactions will ask for tip.  
Program asks for two input addresses (primary account and tip account).
Transactions stored in sqlite db.
Coinbase backend.  Bitcoin price pulled every 60 sec.

Need to add: 
-GUI
-way to easily input btc addresses in Setup function
-ability to query confirmations
-invoice reports
-button functionality (waiting on parts from adafruit)
-custom qr codes based on price


