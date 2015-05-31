"""
If the main program had to stop and we want
to run it again. It is useful to run the parser
by this script. it will look at the last valid movie
and continue the parser processing.

"""

from IMDbThread import IMDbThread
from os.path import expanduser

home = expanduser("~")

movies = home + "/movies.txt"
recovery = home + "/recovery.txt"
moviesWithoutBudget = home + "/moviesWithoutBudget.txt"
persons = home + "/persons.txt"
wrongMovie = home + "/wMovies.txt"
wrongPersons = home + "/wPersons.txt"


array = []

try:
    with open(movies, 'r') as p:
        for movie in p.readlines():
            item = movie[:-1].split("\t")
            array.append(int(item[0]))
except:
    pass

for i in array:
    fork = IMDbThread(0, 1, i, 1, recovery, moviesWithoutBudget, persons, wrongMovie, wrongPersons)
    fork.start()
    fork.join()
