from urllib2 import URLError
from IMDbNormalMovie import IMDbNormalMovie
from IMDbNormalPerson import IMDbNormalPerson
from IMDbProMovie import IMDbProMovie
import time
import urllib2 as request
from multiprocessing import Process, Lock, Manager
from os.path import expanduser

"""
Subclass of Process to retrieve data from IMDb.
Each movie is indetify by an id on the website.
This id is used to download iteratively every movies.
"""

lockGoodMovie = Lock()
lockGoodMovieWithout = Lock()
lockWrongMovie = Lock()
lockGoodPerson = Lock()
lockWrongPerson = Lock()

lockActorsDico = Lock()


actorsDico = Manager().dict()

home = expanduser("~")
personsPath = home + "/persons.txt"
wPersonsPath = home + "/wPersons.txt"

try:
    with open(personsPath, 'r') as p:
        for person in p.readlines():
            item = person[:-1].split("\t")
            with lockActorsDico:
                actorsDico[int(item[0])] = 1
except:
    pass

try:
    with open(wPersonsPath, 'r') as p:
        for person in p.readlines():
            item = person[:-1].split("\t")
            with lockActorsDico:
                actorsDico[int(item[0])] = 2
except:
    pass

class IMDbThread(Process):
    def __init__(self, number, threadNumber,
                 startFrom, numberOfMovies,
                 movies, moviesWithoutBudget,
                 persons, wMovies, wPersons):
        Process.__init__(self)
        self.number = number
        self.threadNumber = threadNumber
        self.numberOfMovies = numberOfMovies
        self.moviesWithoutBudget = moviesWithoutBudget
        self.startFrom = startFrom

        self.urlMovieNorm = "http://www.imdb.com/title/tt"
        self.urlMoviePro = "https://pro-labs.imdb.com/title/tt"
        self.urlActorNorm = "http://www.imdb.com/name/nm"
        self.urlActorPro = "https://pro-labs.imdb.com/name/nm"
        self.movies = movies
        self.persons = persons
        self.wMovies = wMovies
        self.wPersons = wPersons


    def run(self):

        begin = time.time()
        thread = self.number

        for i in range(self.startFrom, self.startFrom + self.numberOfMovies):
            if i == (self.startFrom + self.number):
                self.getMovie(i)
                self.number += self.threadNumber

        print("thread number : " + str(thread))
        print("take : " + str(time.time() - begin) + " seconds")
        print("finish")


    def printMovie(self, movieNor, moviePro, id):

        with lockGoodMovie:
            try:
                file = open(self.movies, "a+")
                file.write(
                    str(id) + "\t" + str(moviePro.awards) + "\t"
                    + str(moviePro.budget) + "\t" + str(movieNor.numberOfRatingUser) + "\t"
                    + str(movieNor.numberOfReviews) + "\t"
                    + str(movieNor.actor1) + "\t" + str(movieNor.actor2) + "\t"
                    + str(movieNor.actor3) + "\t" + str(movieNor.director) + "\t"
                    + str(movieNor.numberOfCritics) + "\t" + str(movieNor.numberOfMetascore) + "\t"
                    + str(movieNor.year) + "\t" + str(movieNor.writer) + "\t"
                    + str(movieNor.ratingUser) + "\t" + str(movieNor.metascore) + "\t"
                    + str(moviePro.gross) + "\n"
                )
                file.close()
            except:
                print("error writing for movie id : " + id)


    def printMovieWithoutBudget(self, movieNor, moviePro, id):

        with lockGoodMovieWithout:
            try:
                file = open(self.moviesWithoutBudget, "a+")
                file.write(
                    str(id) + "\t" + str(moviePro.awards) + "\t"
                    + str(movieNor.numberOfRatingUser) + "\t"
                    + str(movieNor.numberOfReviews) + "\t"
                    + str(movieNor.actor1) + "\t" + str(movieNor.actor2) + "\t"
                    + str(movieNor.actor3) + "\t" + str(movieNor.director) + "\t"
                    + str(movieNor.numberOfCritics) + "\t" + str(movieNor.numberOfMetascore) + "\t"
                    + str(movieNor.year) + "\t" + str(movieNor.writer) + "\t"
                    + str(movieNor.ratingUser) + "\t" + str(movieNor.metascore) + "\n"
                )
                file.close()
            except:
                print("error writing for movieWithoutBudget id : " + id)

    def printPerson(self, person, id):
        with lockGoodPerson:
            try:
                file = open(self.persons, "a+")
                file.write(
                    str(id) + "\t" + str(person.numberActor) + "\t"
                    + str(person.numberProducer) + "\t" + str(person.numberDirector) + "\t"
                    + str(person.awards) + "\t" + str(person.birth) + "\t"
                    + str(person.numberWriter) + "\t" + str(person.nominations) + "\n"
                )
                file.close()
            except:
                print("error writing for person id : " + id)

    def printWrongMovie(self, movieNor, moviePro, id):
        with lockWrongMovie:
            try:
                file = open(self.wMovies, "a+")
                file.write(
                    str(id) + "\t" + str(moviePro.awards) + "\t"
                    + str(moviePro.budget) + "\t" + str(movieNor.numberOfRatingUser) + "\t"
                    + str(movieNor.numberOfReviews) + "\t"
                    + str(movieNor.actor1) + "\t" + str(movieNor.actor2) + "\t"
                    + str(movieNor.actor3) + "\t" + str(movieNor.director) + "\t"
                    + str(movieNor.numberOfCritics) + "\t" + str(movieNor.numberOfMetascore) + "\t"
                    + str(movieNor.year) + "\t" + str(movieNor.writer) + "\t"
                    + str(movieNor.ratingUser) + "\t" + str(movieNor.metascore) + "\t"
                    + str(moviePro.gross) + "\n"
                )
                file.close()
            except:
                print("error writing for wrongMovie id : " + id)

    def printWrongPerson(self, person, id):
        with lockWrongPerson:
            try:
                file = open(self.wPersons, "a+")
                file.write(
                    str(id) + "\t" + str(person.numberActor) + "\t"
                    + str(person.numberProducer) + "\t" + str(person.numberDirector) + "\t"
                    + str(person.awards) + "\t" + str(person.birth) + "\t"
                    + str(person.numberWriter) + "\t" + str(person.nominations) + "\n"
                )
                file.close()
            except:
                print("error writing for person id : " + id)


    def verificationMovie(self, movieNorm, moviePro):
        if (movieNorm.actor1 == -1 or
                    movieNorm.actor2 == -1 or
                    movieNorm.actor3 == -1 or
                    movieNorm.director == -1 or
                    movieNorm.writer == -1 or
                    movieNorm.ratingUser == -1 or
                    movieNorm.year == -1):
            return -1

        if movieNorm.metascore == -1:
            movieNorm.metascore = int((movieNorm.ratingUser * 10))

        return 0

    def verificaitonPerson(self, person):
        if (person.birth == -1 or
                    (person.numberProducer + person.numberActor
                         + person.numberDirector
                         + person.numberWriter) == 0):
            return -1

        return 0



    def getMovie(self, i):
        print(str(i))
        result = self.tryGettingMovie(i)

        if result[0] == 0:
            self.printToGoodFile(result[1])
        elif result[0] == 2:
            self.printToGoodWithoutBudgetFile(result[1])
        else:
            self.printToWrongFile(result[1])


    def printToGoodWithoutBudgetFile(self, result):
        for (index, item) in enumerate(result):
            if (index == 0):
                self.printMovieWithoutBudget(*item)
            else:
                self.printPerson(*item)

    def printToWrongFile(self, result):
        for (index, item) in enumerate(result):
            if (index == 0):
                self.printWrongMovie(*item)
            else:
                self.printWrongPerson(*item)

    def printToGoodFile(self, result):
        for (index, item) in enumerate(result):
            if (index == 0):
                self.printMovie(*item)
            else:
                self.printPerson(*item)


    def actorAlreadyHave(self, id):
        """
        :param id:
        :return: 0 if has not the person
                1 if has a good person
                2 if has a wrong person
        """
        with lockActorsDico:
            result = actorsDico.get(id)
            if (result == None):
                return 0
        return result


    def needToLoadActor(self, id):
        """
        :param id:
        :return: -1 if already load
                -2 if already load but bad movie
                else load the movie and return 0
        """
        error = 0
        source = None
        result = self.actorAlreadyHave(id)

        if result == 1:
            error = -1
        elif result == 2:
            error = -2
        else:
            source = request.urlopen(self.urlActorNorm + str(id), timeout=10).read()
        return (error, source)

    def addEntryToActorDico(self, id):
        with lockActorsDico:
            actorsDico[id] = 1

    def addEntryToActorDicoWrong(self, id):
        with lockActorsDico:
            actorsDico[id] = 2

    def tryGettingMovie(self, i):
        resultTab = []
        try:
            sourceCodeA = request.urlopen(self.urlMovieNorm + str(i), timeout=10).read()
            sourceCodeB = request.urlopen(self.urlMoviePro + str(i), timeout=10).read()

            infoMovieNorm = IMDbNormalMovie(sourceCodeA)
            infoMovieNorm.getAll()

            infoMoviePro = IMDbProMovie(sourceCodeB)
            infoMoviePro.getAll()

            resultTab.append((infoMovieNorm, infoMoviePro, i))

            if (self.verificationMovie(infoMovieNorm, infoMoviePro) == -1):
                return (1, resultTab)

            if self.loadActor(infoMovieNorm.actor1) == -1:
                return (1, resultTab)

            if self.loadActor(infoMovieNorm.actor2) == -1:
                return (1, resultTab)

            if self.loadActor(infoMovieNorm.actor3) == -1:
                return (1, resultTab)

            if self.loadActor(infoMovieNorm.director) == -1:
                return (1, resultTab)

            if self.loadActor(infoMovieNorm.writer) == -1:
                return (1, resultTab)

        except URLError as e:
            print(str(e) + " for id : " + str(i))
            return (1, resultTab)

        except Exception as e:
            print(str(e) + " for id : " + str(i))
            return (1, resultTab)

        if (infoMoviePro.budget == -1 or
                infoMoviePro.gross == -1):
            return (2, resultTab)

        return (0, resultTab)


    def loadActor(self, id):
        error, sourceCode = self.needToLoadActor(id)
        if error == -2:
            return -1
        if (error == 0):
            info = IMDbNormalPerson(sourceCode)
            info.getAll()

            if self.verificaitonPerson(info) == -1:
                self.printWrongPerson(info, id)
                self.addEntryToActorDicoWrong(id)
                return -1
            else:
                self.printPerson(info, id)
                self.addEntryToActorDico(id)

