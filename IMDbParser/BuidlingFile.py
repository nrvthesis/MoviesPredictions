"""
Script used to compact all the data together.
First, a person was a reference to another file.
At the end, every details of the person were output.
Prepare the data to be exploited by the other script (knn, ...)

"""

from os.path import expanduser

home = expanduser("~")

moviesWithoutBudget = home + "/Desktop/moviesWithoutBudget.txt"
movies = home + "/Desktop/movies.txt"
personsPath = home + "/Desktop/persons.txt"
finalMoviesWithoutBudget = home + "/Desktop/finalMoviesWithoutBudget.txt"
finalMoviesWithBudget = home + "/Desktop/finalMoviesWithBudget.txt"

personsHash = {}

def loadPersonsInMemory():
    with open(personsPath, 'r') as p:
        for person in p.readlines():
            item = person[:-1].split("\t")
            personsHash[item[0]] = item[1:]

def searchPerson(id):
    persons = []

    for person in id:
        search = personsHash.get(person)
        if search:
            persons.extend(search)
        else:
            return None

    return persons

def builderWithBudget(m, f):
    count = 0
    for lineM in m.readlines():
        tabM = lineM[:-1].split("\t")

        arg = tabM[5:9]
        arg.append(tabM[12])
        persons = searchPerson(arg)

        if persons == None :
            print("Can't find all persons for the id : " + str(tabM[0]))
            continue
        tabM.__delitem__(12)
        tabM[5:9] = []

        saveLast = tabM[-3:]
        tabM = tabM[:-3]
        tabM.extend(persons)
        tabM.extend(saveLast)

        count +=1
        if count%1000 == 0:
            print(tabM[0])

        for (index, item) in enumerate(tabM[1:]):
                if index == (len(tabM)-2):
                    f.write(str(item) + "\n")
                else:
                    f.write(str(item) + "\t")


def builderWithoutBudget(m, f):
    count = 0
    for lineM in m.readlines():
        tabM = lineM[:-1].split("\t")

        arg = tabM[4:8]
        arg.append(tabM[11])
        persons = searchPerson(arg)

        if persons == None :
            print("Can't find all persons for the id : " + str(tabM[0]))
            continue
        tabM.__delitem__(11)
        tabM[4:8] = []

        saveLast = tabM[-2:]
        tabM = tabM[:-2]
        tabM.extend(persons)
        tabM.extend(saveLast)

        count +=1
        if count%1000 == 0:
            print(tabM[0])

        for (index, item) in enumerate(tabM[1:]):
                if index == (len(tabM)-2):
                    f.write(str(item) + "\n")
                else:
                    f.write(str(item) + "\t")

if __name__ == '__main__':

    loadPersonsInMemory()
    try:
        with open(movies, 'r') as m:
            with open(finalMoviesWithBudget, 'a+') as f:
                builderWithBudget(m, f)
    except:
        pass
    try:
        with open(moviesWithoutBudget, 'r') as m:
                with open(finalMoviesWithoutBudget, 'a+') as f:
                    builderWithoutBudget(m, f)
    except:
        pass

