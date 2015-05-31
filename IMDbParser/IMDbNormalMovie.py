import bs4 as bs

"""
Class to download data about a movie
(year of the movie, ...)
"""

class IMDbNormalMovie:

    def __init__(self, sourceCode):
        self.parse = bs.BeautifulSoup(sourceCode)
        self.year = -1
        self.director = -1
        self.writer = -1
        self.actor1 = -1
        self.actor2 = -1
        self.actor3 = -1
        self.ratingUser = -1
        self.numberOfRatingUser = 0
        self.metascore = -1
        self.numberOfMetascore = 0
        self.numberOfReviews = 0
        self.numberOfCritics = 0

    def getAll(self):
        self.getCasts()
        self.getFilmMaker()
        self.getRatingAndComments()
        self.getYear()

    def getYear(self):
        #--------------------
        # year
        #--------------------

        yearBalise = self.parse.find("span", attrs={"class": "nobr"})

        self.year = self.testYear(yearBalise)

        #print("year : " + str(self.year))
        #--------------------

    def getFilmMaker(self):
        #--------------------
        # FilmMaker
        #--------------------

        directorBalise = self.parse.find("div", attrs={"itemprop":"director"})
        if directorBalise and directorBalise != -1:
            directorBalise = directorBalise.a

        self.director = self.testPersonID(directorBalise)

        creatorBalise = self.parse.find("div", attrs={"itemprop":"creator"})
        if creatorBalise and creatorBalise != -1:
            creatorBalise = creatorBalise.a

        self.writer = self.testPersonID(creatorBalise)

        #print("director : " + str(self.director))
        #print("writer : " + str(self.writer))

        #--------------------


    def getCasts(self):
        #--------------------
        # Cast
        #--------------------

        actorBalise = self.parse.find("div", attrs={"itemprop":"actors"})

        if actorBalise and actorBalise != -1:
            baliseA = actorBalise.findAll("a")
            if baliseA and baliseA != -1:
                for (index, actor) in enumerate(baliseA):
                    if index > 2:
                        break
                    if (index == 0):
                        self.actor1 = self.testPersonID(actor)
                    if (index == 1):
                        self.actor2 = self.testPersonID(actor)
                    if (index == 2):
                        self.actor3 = self.testPersonID(actor)

        #print("actor1 : " + str(self.actor1))
        #print("actor2 : " + str(self.actor2))
        #print("actor3 : " + str(self.actor3))

        #--------------------


    def getRatingAndComments(self):
        #--------------------
        # rating and comments
        #--------------------

        frameBalise = self.parse.find("div", attrs={"class":"star-box giga-star"})
        if frameBalise and frameBalise != -1:

            #ratingUser
            ratingUserBalise = frameBalise.find("span", attrs={"itemprop":"ratingValue"})
            if ratingUserBalise and ratingUserBalise != -1:
                try:
                    self.ratingUser = float(str(ratingUserBalise.string))
                except Exception:
                    self.ratingUser = -1

            #numberOfRatingUser
            numberOfRatingUserBalise = frameBalise.find("span", attrs={"itemprop":"ratingCount"})
            if numberOfRatingUserBalise and numberOfRatingUserBalise != -1:
                if (numberOfRatingUserBalise.string.replace(",","").isdigit()):
                    self.numberOfRatingUser = int(numberOfRatingUserBalise.string.replace(",",""))


            framecritics = frameBalise.findAll("a", attrs={"href":"criticreviews?ref_=tt_ov_rt"}, limit=2)
            if framecritics and framecritics != -1 and len(framecritics) > 1:

                #metascore
                metascoreTest = framecritics[0].string.strip().split("/")[0]
                if str(metascoreTest).isdigit():
                    self.metascore = int(str(metascoreTest))

                #numberOfMetascore
                numberOfMetascoreTest = framecritics[1].string.strip()
                if str(numberOfMetascoreTest).isdigit():
                    self.numberOfMetascore = int(str(numberOfMetascoreTest))


            frameNumbers = frameBalise.findAll("span", attrs={"itemprop":"reviewCount"}, limit=2)
            if frameNumbers and frameNumbers != -1 and len(frameNumbers) > 1:

                #numberOfReviews
                numberOfReviewsTest = frameNumbers[0].string.replace("user","").replace(",","").strip()
                if str(numberOfReviewsTest).isdigit():
                    self.numberOfReviews = int(str(numberOfReviewsTest))

                #numberOfCritics
                numberOfCriticsTest = frameNumbers[1].string.replace("critic","").replace(",","").strip()
                if str(numberOfCriticsTest).isdigit():
                    self.numberOfCritics = int(str(numberOfCriticsTest))

        #print("ratingUser : " + str(self.ratingUser))
        #print("numberOfRatingUser : " + str(self.numberOfRatingUser))
        #print("metascore : " + str(self.metascore))
        #print("numberOfMetascore : " + str(self.numberOfMetascore))
        #print("numberOfReviews : " + str(self.numberOfReviews))
        #print("numberOfCritics : " + str(self.numberOfCritics))

        #--------------------


    def testYear(self, year):
        if (year and year != -1):
            try:
                return int(self.parse.find("span", attrs={"class": "nobr"}).getText().strip()[1:-1])
            except:
                return -1
        return -1


    def testPersonID(self, maker):
        nameBalise = "/name/nm"
        if (maker and maker != -1 and maker["href"]):
            temp = str(maker["href"]).replace(nameBalise, "").split("/")[0]
            try:
                return int(temp)
            except:
                return -1
        return -1

#------------------------------------