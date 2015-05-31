import bs4 as bs
import re

"""
Class to download data about a person
such as an actor, director, ...
"""

class IMDbNormalPerson:

    def __init__(self, sourceCode):
        self.parse = bs.BeautifulSoup(sourceCode)
        self.birth = -1
        self.awards = 0
        self.nominations = 0
        self.numberActor = 0
        self.numberWriter = 0
        self.numberProducer = 0
        self.numberDirector = 0

    def getAll(self):
        self.getAwards()
        self.getBirth()
        self.getNumberOfMovies()
        #self.getSkills()


    def getBirth(self):
        #--------------------
        # birth
        #--------------------

        birthBalise = self.parse.find("time", attrs={"itemprop":"birthDate"})
        self.birth = self.testDate(birthBalise)

        #print("birth : " + str(self.birth))

        #--------------------

    def getAwards(self):
        #--------------------
        # Awards and nominations
        #--------------------

        self.awardsBalise = self.parse.findAll("span", attrs={"itemprop":"awards"}, limit=2)
        self.awards, self.nominations = self.testAwards(self.awardsBalise)

        #print("awards : " + str(self.awards))
        #print("nominations : " + str(self.nominations))

        #--------------------

    #def getSkills(self):
        #--------------------
        # skills
        #--------------------

        #skillsBalise = self.parse.find("div", attrs={"id":"name-job-categories"})
       # self.actor, self.writer, self.producer, self.director = self.testSkills(skillsBalise)

        #print("actor : " + str(self.actor))
        #print("writer : " + str(self.writer))
        #print("producer : " + str(self.producer))
        #print("director : " + str(self.director))

        #--------------------

    def getNumberOfMovies(self):
        #--------------------
        # number of movies
        #--------------------

        baliseSkill = self.parse.find("div", attrs={"id":"filmo-head-actor"})
        if baliseSkill and baliseSkill != -1:
            self.numberActor = self.testNumber(baliseSkill)

        else:
            baliseSkill = self.parse.find("div", attrs={"id":"filmo-head-actress"})
            self.numberActor = self.testNumber(baliseSkill)

        self.numberWriter = self.testNumber(self.parse.find("div", attrs={"id":"filmo-head-writer"}))
        self.numberProducer = self.testNumber(self.parse.find("div", attrs={"id":"filmo-head-producer"}))
        self.numberDirector = self.testNumber(self.parse.find("div", attrs={"id":"filmo-head-director"}))

        #print("numberWriter : " + str(self.numberWriter))
        #print("numberProducer : " + str(self.numberProducer))
        #print("numberDirector : " + str(self.numberDirector))
        #print("numberActor : " + str(self.numberActor))
        #print("man : " + str(self.man))

        #--------------------


    def testDate(self, birthBalise):
        if (birthBalise and birthBalise != -1):
            date = birthBalise["datetime"]
            if (date and date != -1):
                try:
                    return int(date.split("-")[0])
                except Exception:
                    return -1
        return -1

    def testAwards(self, awards):
        awardsR = 0
        nominationsR = 0
        if not awards or awards == -1:
            return (0,0)

        entireText = ""
        for award in awards:
            entireText += award.getText()

        iter = re.split("\.| |\n", entireText.strip())

        for (index, alpha) in enumerate(iter):
            if alpha.isdigit():
                prev = index - 1
                next = index + 1

                if prev > -1 and str(iter[prev]).__contains__("Won"):
                    awardsR += int(alpha)

                elif next < len(iter) and str(iter[next]).__contains__("wins"):
                    awardsR += int(alpha)

                else:
                    nominationsR += int(alpha)

        return (awardsR, nominationsR)

    def testSkills(self, balise):

        actor = 0
        writer = 0
        producer = 0
        director = 0

        if (not balise or balise == -1):
            return actor, writer, producer, director

        for skill in balise .getText().replace("\n","").split("|"):
            skill = skill.strip()

            if skill == "Actor" or skill == "Actress":
                actor = 1
            elif skill == "Producer":
                producer = 1
            elif skill == "Director":
                director = 1
            elif skill == "Writer":
                writer = 1

        return actor, writer, producer, director

    def testNumber(self, balise):

        if not balise or balise == -1:
            return 0

        baliseFormat = balise.getText().split("(")

        if len(baliseFormat) > 1:
            baliseFinal = baliseFormat[1].split(" ")[0]

            if (baliseFinal.isdigit()):
                return int(baliseFinal)
        return 0

#------------------------------------