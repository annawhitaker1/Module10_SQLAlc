# Module10_SQLAlc

Started the Module by working through the climate starter code in Jupyter notebook. As a reference, I used ChatGPT for help in both the Jupyter notebook section and the app.py section.
The dependencies were entered in the starter code. 
I created the engine to hawaii sqlite file and brought the database into the new model in this jupyter notebook.
Printed the classes that the automap found. Then, saved the references to each of the station and measurement tables. 
I printed out the colume names for each table, which wasn't prompted by the starter code, but it helped me familiarize myself with the data.
Then, I created the session. 

First in the precipitation analysis, I calculated the recent date. From the recent date, I converted to the Year-month-date format. 
The conversion allowed for me to calculate the date of one year ago that was the basis of my logic for the next step in getting the data from the last 12 months. 
Once we saved the data from the last 12 months in the variable "results", we converted it to a dataframe to plot.

First in the station analysis, I calculated the count of unique stations and the count of each unq stations in the measurements table. 
I gathered the most active station min max and avg temperature data. From there, I saved the last 12 months of temperature data in the variable "temp_data". Converted the results into a list of temperatures to plot the histogram. 
At the end, I closed my session. 


For the app.py file, I brought in the dependencies. I set up the database, set up Flask, then created all routes that were required in the module 10 outline.
At the end, I closed my session.
