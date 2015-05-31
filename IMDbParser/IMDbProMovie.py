import bs4 as bs
import re

"""
Class to download data about a movie (budget, ...)
It parse the IMDb pro webpage.
"""

class IMDbProMovie:

    def __init__(self, sourceCode):
        self.parse = bs.BeautifulSoup(sourceCode)
        self.gross = -1
#        self.openWK = -1
        self.budget = -1
        self.awards = 0

    def getAll(self):
        self.getBudget()

    def getBudget(self):
        #--------------------
        # Budget details
        #--------------------

        budgetDetails = self.parse.find("div", attrs={"id": "main_details"})
        if budgetDetails and budgetDetails != -1:
            budgetNames = budgetDetails.findAll("dt")
            budgetNumbers = budgetDetails.findAll("dd")

            if budgetNames and budgetNames != -1 \
                    and budgetNumbers and budgetNumbers != -1:

                for (name, number) in zip(budgetNames, budgetNumbers):
                    name = name.string.strip()
                    if (name == "BUDGET"):
                        self.budget = self.testBudget(number)
                    elif (name == "OPENING WKD"):
                        pass
                   #     self.openWK = self.testBudget(number)
                    elif (name == "GROSS"):
                        self.gross = self.testBudget(number)
                    elif (name == "AWARDS"):
                        self.awards = self.testAwards(number)
                    else:
                        break

        #print("gross : " + str(self.gross))
        #print("openWK : " + str(self.openWK))
        #print("budget : " + str(self.budget))
        #print("awards : " + str(self.awards))

        #--------------------

    def testBudget(self, budget):
        if (budget):
            number = str(budget.getText().strip().split("\n")[0])
            if number.__contains__("B"):
                budgetStr = number[1:-1].replace(",",".")
                budgetStr = float(budgetStr) * 1000
            elif number.__contains__("K"):
                budgetStr = number[1:-1].replace(",",".")
                budgetStr = float(budgetStr) / 1000
            else:
                budgetStr = number[1:-2].replace(",",".")
            try:
                return float(budgetStr)
            except:
                return -1
        return -1

    def testAwards(self, awards):
        result = 0
        if not awards:
            return result

        for alpha in re.split(" |\n", awards.getText().strip()):
            if alpha.isdigit():
                result += int(alpha)
        return result
