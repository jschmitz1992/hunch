# hunch – A simple stock market prediction app
This Django project provides a simple interface for historic stock price data. Furthermore, it allows the user to predict the future performance of the stock using regression algorithms.

The interface has been implemented on the app "tripous", which can be accessed via the subdirectory with the same name. 

![Screenshot of the prediction app](https://github.com/jschmitz1992/hunch/blob/main/tripous-social-screenshot.jpg?raw=true)

## Installation
1. Clone this repository with `git clone https://github.com/jschmitz1992/hunch.git`
2. Access project directory with `cd hunch` 
3. Automatically install dependencies with `pip install -r requirements.txt` 

---
**Technical note**

We generally advise you to create a new virtual  environment for installing and running this app to prevent discrepancies with already existing libraries.

---


## How to run
1. Make sure you are in the top project-directory called "hunch"
2. Run `python manage.py runserver`
3. Access the app via the link provided in the shell (e.g. [http://127.0.0.1:8000/tripous](http://127.0.0.1:8000/tripous))