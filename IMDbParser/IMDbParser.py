"""
The heart of the parser.
run : python IMDBParser.py
to run the parser.
"""

from IMDbThread import IMDbThread
from os.path import expanduser

home = expanduser("~")

movies = home + "/movies.txt"
moviesWithoutBudget = home + "/moviesWithoutBudget.txt"
persons = home + "/persons.txt"
wrongMovie = home + "/wMovies.txt"
wrongPersons = home + "/wPersons.txt"

forkNumbers = 1

listProcess = []
for i in range(forkNumbers):

    # The first number is the IMDb id the program will start
    # the second number is the number of movie we want to downloaded
    temp = IMDbThread(i, forkNumbers, 2488496, 1,
                                  movies, moviesWithoutBudget, persons, wrongMovie, wrongPersons)
    listProcess.append(temp)
    temp.start()

for j in listProcess:
    j.join()
