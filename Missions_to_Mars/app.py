from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo=PyMongo(app)

#Identify the collection
data=mongo.db.data


# Render the index.html page with any craigslist listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    result=data.find_one()
    return render_template("index.html", result=result)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():

    # scrape_craigslist.scrape() is a custom function that we've defined in the scrape_craigslist.py file within this directory
    marsdata=scrape_mars.scrape()
    data.replace_one({},marsdata,upsert=True)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)