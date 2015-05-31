# MoviesPredictions
Analysis of Success Factors of Movies Based on Internet Movie Database


This repository contains the programs developed for the master thesis "Analysis of Success Factors of Movies Based on Internet Movie Database".

The first program parses the IMDb website to collect the data of movies required to apply the machine learning methods.

The second program implements the different technique used in the thesis in order to predict the movie ratings.

These programs have been tested on Python 2.7.

To test the programs, go to the current directory IMDBParser and run the Python script:

$ python IMDbParser.py

To launch a batch test to predict movie ratings, go to the current directory Predictions and run:

$ python FullTest.py Test

The files db21.txt and dbRating.txt contains respectively all the dataset with 21 features and 37 features about the movies.
The prediction program works with another program called R (open source and available on repo for linux). 
After installing R, run it and launch this command to install some packages :

$ install.packages("psych")
$ install.packages("clue")

Also, the package numpy is required for python 2.7.

Codes are commented if you want to modify it.

© Hervé Eerebout & Nicolas Pirotte (nrv team)