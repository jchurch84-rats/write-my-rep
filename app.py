from flask import Flask # tiny python webserver that turns your code into a web page - takes requests, hands back HTML

app = Flask(__name__) # This is the rat King: __name__ tells Flask hey, I'm this script, RUN ME AS A SERVER, not some Library
@app.route('/') # This is a "Decorator" binding the the HTTP GET (or POST) request to '/' to the function below-it's Flask's way of saying handle traffic 
def home():
  if request.method == 'POST':
    return 'Got It!!!'  
  return open('index.html').read()
  
