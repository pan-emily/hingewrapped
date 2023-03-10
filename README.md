# Hinge Wrapped
## 2022 Dating Wrapped, Hinge Edition

Welcome to my Hinge Data visualizer! After seeing the trend of creating "Dating Wrapped" slideshows to recap a year of dating, I decided to leverage Hinge's "Download My Data" feature to be able to make a personalized dashboard of this year's Hinge Wrapped! 

This project contains a script to process the data that Hinge provides, and opens up a browser page to display the dashboard! I recommend using this in a more vertical aspect ratio (like a split-screen browser window), as the graphics are optimized to display on approximately that size. 

## How do I use this script? 
1. Get your data! On the Hinge app, go to your profile tab and select "Settings." Scroll all the way down in settings, and under "Legal," you should see a tab called "Download My Data." Select this and follow the steps. My dataset is compatible for most USA versions, and you want to select "Download My Data." When the data is ready, you should receive an email (or just check back in in a day or so) and you can go to the same spot in the app to download the data. Ensure that you have saved the file path of your saved data, you will need this later. 
2. Run the app.py script however you'd like. When you run it, you will be prompted for the path of the directory that you saved your downloaded data to, and you should enter it here. When it runs, you will find text that says "Dash is running on http://127.0.0.1:8050". If you are having trouble with finding this, you can just go into your browswer and type in http://127.0.0.1:8050 as the url and the dashboard should load! 

## Details for nerds
Python script (app.py):
1. Data analysis and processing
	Primarily leveraged Pandas and NumPy. The data was in JSON, so the json package was used to parse the file contents as well as subcontents. Then I loaded the data into pandas. Computations were relatively simple, so Pandas and NumPy functionality was sufficient. 

2. Plotting and visualization 
	To plot and visualize the data, I used Plotly, namely for its convenient integration with Dash. Plotly allowed me to create many different customized chart styles, such as pie, waffle, and bar charts. 

3. Dashboard creation
	I used Dash to format the figures generated by Plotly using CSS. Dash essentially creates a small Flask web app to host the website locally to view the dashboard webpage. 

## What???s to come? 
- Integration with Flask to create an interactive webpage to run the script to make the app more accessible. 
- Aesthetic improvements
