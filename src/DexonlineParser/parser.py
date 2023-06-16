#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import copy
import sys


class DexParser:
    def __init__(self, word):
        self.word = word # word inputted
        self.url = f"https://dexonline.ro/definitie/{self.word}" # url to be parsed, information of {word}
        self.response = requests.get(self.url) # request page
        self.soup = BeautifulSoup(self.response.text, "html.parser") # start parsing

        self.information = {
            "lemma": self.word,  # word itself, i.e., "cățel"
            "definitions": [],  # definitions + examples in a tight format
            "type": "",  # word classification, substantiv [gender], adverb, etc
            "inflection": {}
        }

        self.get() # Populate information

    def isDefinition(self, tag): # function used whlie searching for definitions
        parent = tag.parent.find("span", "material-icons meaning-icon") # find if definition is a colloquial definition (not classified the same)

        if parent and parent.text == "chat_bubble": # control flow if definition is colloquial (won't be added otherwise)
            return True

        return len(tag.find_all(lambda tag: tag.name != "span")) == 0 # all non-coloquial definitions have no tags, only way to check

    def get(self):
        self.getInformation() # populate basic info 
        type = self.information["type"]

        if "substantiv" in type: # if word is a noun
            self.findSubstantivInflection() 
            return
 
        elif type == "adjectiv": # if word is an adjective
            self.findAdjectivInflection()
            return
        
        elif type == "verb": # if word is a verb
            self.findVerbInflection() 
            return
        
        else: # if type of word can't be found
            print("Error getting type, double check word is spelt correctly.")
            return sys.exit(1)
        
    def getInformation(self):
        if not self.soup: # if the page can't be found
            print("Error parsing information")
            return sys.exit(1)
        
        elif not self.soup.find("span", "tree-pos-info"): # if word type can't be parsed
            print("Error parsing text, double check word is spelt correctly.")
            return sys.exit(1)
        
        else: # if none of these we can define the word type
            self.information["type"] = self.soup.find("span", "tree-pos-info").text
        
        currentDefinition = {"text": "", "examples": []} # current definition and its examples being parsed

        for container in self.soup.find("div", "tree-body").find("ul", "meaningTree").find_all("li", "type-meaning depth-0"): # find each definition and it's examples
            for spanTag in container.find_all("span", "def html"): # parse through the text itself (span tags)
                if self.isDefinition(spanTag): # if current spanTag is a definition set current definition to equal it
                    if currentDefinition["text"]: # if definition has been found
                        self.information["definitions"].append(copy.copy(currentDefinition)) # populate the information
                        currentDefinition = {"text": "", "examples": []} # reset current information

                    currentDefinition["text"] = spanTag.text # set text to be the definition

                else:
                    currentDefinition["examples"].append(spanTag.text) # if text is an example for the current definition add it

        if currentDefinition["text"]: # if information was found
            self.information["definitions"].append(copy.copy(currentDefinition)) # add the definition and its examples

    def printInformation(self):
        cases = ["nominativ-acuzativ", "genitiv-dativ", "vocativ"]
        forms = "Nearticulat", "Articulat"

        print(self.information["lemma"] + ": " + self.information["type"])

        if len(self.information["definitions"]) > 4:
            definitions = self.information["definitions"][:4]
        
        else:
            definitions = self.information["definitions"]

        for definition in definitions:
            print("Definition:", definition["text"])
            print("Examples:")

            if definition["examples"]:
                for example in definition["examples"]:
                    print("-" + example)
            else:
                print("None available")

            print("\n")

        info = self.information["inflection"]

        if self.information["type"] == "verb":
            width = len("mai mult ca perfect")

            for person in info:
                for word in info.get(person):
                    if len(word) > width:
                        width = len(word)

            print("Inflection:")
            print(f"  Infinitive: {self.information['inflection']['infinitiv']}")
            print(f"  Infinitive lung: {self.information['inflection']['infinitiv lung']}")
            print(f"  Participiu: {self.information['inflection']['participiu']}")
            print(f"  Gerunziu: {self.information['inflection']['gerunziu']}")

            print("\n")

            print("Conjugation:")
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}} ║ {:^{width}} ║ {:^{width}} ║ {:^{width}}".format(
                "Persoana", "Prezent", "Conjunctiv Prezent", "Imperfect", "Perfect Simplu", "Mai Mult Ca Perfect", width=width))
            print("=" * (width * 7))

            persons = ["First Singular", "Second Singular", "Third Singular", "First Plural", "Second Plural", "Third Plural"]

            for person in persons:
                row = [person.lower()]
                row.extend(info[person.lower()])

                print("{:^{width}} ║ {:^{width}} | {:^{width}} | {:^{width}} | {:^{width}} | {:^{width}}".format(*row, width=width))
                print("-" * (width * 7))

        elif "substantiv" in self.information["type"]:
            print("Inflection:")
            width = len(cases[0])

            for case in cases:
                if width < len(str(info.get(case)["nearticulat"])):
                    width = len(str(info.get(case)["nearticulat"]))

                elif width < len(str(info.get(case)["articulat"])):
                    width = len(str(info.get(case)["articulat"]))
            
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("Nominativ-Acuzativ", "Genitiv-Dativ", "Vocativ", width=width))
            print("=" * (width * 3 + 5))
            for form in forms:
                lowerForm = form.lower()
                print("{:<{width}} ║ {:<{width}} ║".format(form, form, width=width))
                print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format(str(info.get(cases[0])[lowerForm]), str(info.get(cases[1])[lowerForm]), str(info.get(cases[2])[lowerForm]), width=width))
                print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("", "", "", width=width))

        else:
            cases = ["nominativ-acuzativ", "genitiv-dativ", "vocativ"]
            width = len(cases[0])
            for case in cases:
                if width < len(str(info.get(case)["masculine"]["nearticulat"])):
                    width = len(str(info.get(case)["masculine"]["nearticulat"]))    

                elif width < len(str(info.get(case)["masculine"]["articulat"])):
                    width = len(str(info.get(case)["masculine"]["articulat"]))

                elif width < len(str(info.get(case)["feminine"]["nearticulat"])):
                    width = len(str(info.get(case)["feminine"]["nearticulat"]))

                elif width < len(str(info.get(case)["feminine"]["articulat"])):
                    width = len(str(info.get(case)["feminine"]["articulat"]))

            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("Nominativ-Acuzativ", "Genitiv-Dativ", "Vocativ", width=width))
            print("=" * (width * 3 + 5))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("Masculine", "Masculine", "Masculine", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("", "", "", width=width))
            print("{:<{width}} ║ {:<{width}} ║ {:<{width}}".format("Nearticulat:", "Nearticulat:", "Nearticulat:", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format(str(info.get(cases[0])["masculine"]["nearticulat"]), str(info.get(cases[1])["masculine"]["nearticulat"]), str(info.get(cases[2])["masculine"]["nearticulat"]), width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("", "", "", width=width))
            print("{:<{width}} ║ {:<{width}} ║ {:<{width}}".format("Articulat:", "Articulat:", "Articulat:", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format(str(info.get(cases[0])["masculine"]["articulat"]), str(info.get(cases[1])["masculine"]["articulat"]), str(info.get(cases[2])["masculine"]["articulat"]), width=width))

            print("=" * (width * 3 + 5))

            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("Feminine", "Feminine", "Feminine", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("", "", "", width=width))
            print("{:<{width}} ║ {:<{width}} ║ {:<{width}}".format("Nearticulat:", "Nearticulat:", "Nearticulat:", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format(str(info.get(cases[0])["feminine"]["nearticulat"]), str(info.get(cases[1])["feminine"]["nearticulat"]), str(info.get(cases[2])["feminine"]["nearticulat"]), width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format("", "", "", width=width))
            print("{:<{width}} ║ {:<{width}} ║ {:<{width}}".format("Articulat:", "Articulat:", "Articulat:", width=width))
            print("{:^{width}} ║ {:^{width}} ║ {:^{width}}".format(str(info.get(cases[0])["feminine"]["articulat"]), str(info.get(cases[1])["feminine"]["articulat"]), str(info.get(cases[2])["feminine"]["articulat"]), width=width))


    def findSubstantivInflection(self):
        inflectionTables = self.soup.find_all("table", "lexeme", limit=2) # find all tables of inflections
        inflectionTable = None # table to be parsed

        for table in inflectionTables: # parse through tables of infletions
            if "substantiv" in table.text.lower(): # find first noun inflection table
                inflectionTable = table
                break

        if inflectionTable:
            inflectionRows = inflectionTable.find_all("tr")[1:] # each row of information, first row is just headers
            inflectionType = None  # Initialize inflectionType as None

            for row in inflectionRows:
                # find inflection type
                inflectionCell = row.find("td", attrs={"rowspan": "2", "class": "inflection"}) # cell that contains inflection type
                if inflectionCell:
                    inflectionType = inflectionCell.text.strip()

                inflectionForms = [] # current iteration's inflections to be added
                for word in row.find_all("ul", "commaList"):
                    forms = []
                    for li in word.find_all("li", class_="", title=""): # find inflections 
                        form_text = li.text.strip()
                        forms.append(form_text) # add inflections

                    inflectionForms.append(forms)

                if inflectionType not in self.information["inflection"]: # if inflection type couldnt be found 
                    self.information["inflection"][inflectionType] = []

                self.information["inflection"][inflectionType].extend(inflectionForms) # add iteration's inflections

            # Convert the inflection forms to tuples within a list
            for inflectionType, forms in self.information["inflection"].items():
                split = self.splitList(forms)
                if split:
                    if len(split) == 1:
                        self.information["inflection"][inflectionType] = {"nearticulat": split[0], "articulat": ()}
                    
                    else:
                        self.information["inflection"][inflectionType] = {"nearticulat": split[0], "articulat": split[1]}

                else:
                    self.information["inflection"][inflectionType] = {"nearticulat": (), "articulat": ()}



    def findAdjectivInflection(self):
        inflectionTables = self.soup.find_all("table", "lexeme", limit=2) # finds tables of ifnlections
        inflectionTable = None # table to be operated on

        # parses through tables to find the first adjective inflection table
        for table in inflectionTables: 
            if "adjectiv" in table.text.lower():
                inflectionTable = table
                break

        if inflectionTable:
            inflectionRows = inflectionTable.find_all("tr")[2:] # find rows of the table, first two are headers
            inflectionType = None  # Initialize inflectionType as None

            # iterate through rows of table
            for row in inflectionRows:
                # find inflection type
                inflectionCell = row.find("td", attrs={"rowspan": "2", "class": "inflection"})
                if inflectionCell: 
                    inflectionType = inflectionCell.text.strip()

                inflectionForms = [] # current interation's inflection forms to be added
                for word in row.find_all("ul", "commaList"):
                    forms = []
                    for li in word.find_all("li", class_="", title=""): # find all cells in row
                        form_text = li.text.strip()
                        forms.append(form_text)

                    inflectionForms.append(forms)

                if inflectionType not in self.information["inflection"]: # if inflection type could not be found
                    self.information["inflection"][inflectionType] = []

                self.information["inflection"][inflectionType].extend(inflectionForms) # populate inflection forms 

            # Convert the inflection forms to tuples and more readable content
            for inflectionType, forms in self.information["inflection"].items():
                split = self.splitList(forms)

                if split:
                    masculine = split[:2]
                    feminine = split[-2:]

                    self.information["inflection"][inflectionType] = {"masculine": {"nearticulat": masculine[0], "articulat": masculine[1]}, "feminine": {"nearticulat": feminine[0], "articulat": feminine[1]}}

                else:
                    self.information["inflection"][inflectionType] = {"masculine": {"nearticulat": (), "articulat": ()}, "feminine": {"nearticulat": (), "articulat": ()}}

    def findVerbInflection(self):
        inflectionTables = self.soup.find_all("table", "lexeme", limit=2) # find inflection tables
        inflectionTable = None # table to be operated ob

        # parse through tables to find first verb inflection table
        for table in inflectionTables: 
            if "verb" in table.text.lower():
                inflectionTable = table
                break

        if inflectionTable:
            # helper function to get the article of a cell
            def getArticle(tag):
                for element in tag.descendants:
                    if isinstance(element, str):
                        return element.text.strip()
        
                return ""
            
            # helper function to get the actual inflection of a cell
            def getText(tag): 
                return getArticle(tag) + tag.find("ul", "commaList").find("li", class_ = "", title_ = "").text.strip()

            # helper function to find current "persoana" that is being iterated
            def findPerson(tag):
                text = tag.find("td", "inflection person").text.strip()

                if "eu" in text:
                    return "first singular"

                elif "tu" in text:
                    return "second singular"
                
                elif "ea" in text:
                    return "third singular"
                
                elif "noi" in text:
                    return "first plural"
                
                elif "voi" in text:
                    return "second plural"
                
                else:
                    return "third plural"
                
            rows = inflectionTable.find_all("tr") # get all table rows
            others = [getText(i) for i in rows[1].find_all("td", "form")] # get text of special inflection cells
            tenseRows = rows[5:] # find main inflection rows, first 5 contain other information
             
            # define special inflections using others[]
            self.information["inflection"]["infinitiv"] = others[0]
            self.information["inflection"]["infinitiv lung"] = others[1]
            self.information["inflection"]["participiu"] = others[2]
            self.information["inflection"]["gerunziu"] = others[3]

            for row in tenseRows:
                inflections = []
                person = findPerson(row)    

                # iterate through all inflections of each row
                for tag in row.find_all("td", "form"): 
                    inflections.append(getText(tag))

                self.information["inflection"][person] = inflections # update information

    # helper function to split a list in half evenly, returns a tuple
    def splitList(self, lst):
        half = len(lst) // 2

        return tuple(zip(lst[:half], lst[half:]))

# usage code (executable file)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a word.")
        sys.exit(1)

    elif len(sys.argv) != 2:
        print("Please provide only one word.")
        sys.exit(1)

    word = sys.argv[1]
    dex = DexParser(word)
    dex.printInformation()
