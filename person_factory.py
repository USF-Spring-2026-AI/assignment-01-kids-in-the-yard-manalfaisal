import csv
import random
import math

class PersonFactory:
    """Responsible for reading CSV data and generating people attributes."""

    def __init__(self):
        #Dictionary mapping year -> life expectancy
        self.life_expectancy = {}
        #Dictionary mapping decade -> birth rate
        self.birth_rate = {}
        #Dictionary mapping decade -> marriage rate
        self.marriage_rate = {}
        #Dictionary mapping (decade, gender) -> list of (name, frequency)
        self.first_names = {} 
        #Dictionary mapping rank -> probability weight
        self.rank_weight = {}
        #Dictionary mapping decade -> list of (last name, weight)
        self.last_names = {}

    def read_files(self):
        #Open file and automatically close when done
        with open("life_expectancy.csv", newline="") as file:
            #CSV reading pattern based on Python documentation:
            #https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(file)
            for row in reader: 
                #Extract birth year and corresponding life expectancy
                year = row["Year"].strip()
                exp = float(row["Period life expectancy at birth"])
                #Store in dictionary
                self.life_expectancy[year] = exp                

        #Read birth and marriage rates by decade
        with open("birth_and_marriage_rates.csv", newline="") as file:
            #CSV reading pattern based on Python documentation:
            #https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(file)
            for row in reader:
                decade_str = row["decade"].strip()
                #Convert "1950s" -> "1950"
                decade_year = decade_str[:4]
                #Store birth and marriage rates
                self.birth_rate[decade_year] = float(row["birth_rate"])
                self.marriage_rate[decade_year] = float(row["marriage_rate"])

        #Read first name frequencies by decade and gender
        with open("first_names.csv", newline="") as file:
            #CSV reading pattern based on Python documentation:
            #https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(file)
            for row in reader:
                decade_str = row["decade"].strip()
                decade_year = decade_str[:4]
                gender = row["gender"].strip().lower()
                name = row["name"].strip()
                freq = float(row["frequency"])

                #Key is (decade, gender)
                key = (decade_year, gender)

                #Initialize list if needed
                if key not in self.first_names:
                    self.first_names[key] = []

                #Append (name, probability weight)
                self.first_names[key].append((name, freq))

        #Read rank-to-probability file (single line of weights)
        with open("rank_to_probability.csv", newline="") as file:
            line = file.readline().strip()
            probs = [float(x) for x in line.split(",")]

            #Map rank "1" -> first probability, etc.
            #Rank-to-probability dictionary mapping refined with ChatGPT assistance
            self.rank_weight = {str(i + 1): probs[i] for i in range(len(probs))}

        #Read last names and attach weight based on rank
        with open("last_names.csv", newline="") as file:
            #CSV reading pattern based on Python documentation:
            #https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(file)
            for row in reader:
                decade_str = row["Decade"].strip()
                decade_year = decade_str[:4]
                rank = row["Rank"].strip()
                lname = row["LastName"].strip()

                #Lookup probability weight from rank
                weight = self.rank_weight[rank]

                #Initialize decade list if needed
                if decade_year not in self.last_names:
                    self.last_names[decade_year] = []

                #Append (last name, weight)
                self.last_names[decade_year].append((lname, weight))

    def calculate_death_year(self, birth_year):
        #Find decade of birth
        decade = (birth_year // 10) * 10

        #Clamp to minimum supported decade
        if decade < 1950:
            decade = 1950

        #Lookup life expectancy for that decade
        life_exp = self.life_expectancy[str(decade)]

        #Add random +/- 10 year adjustment
        adjustment = random.randint(-10, 10)

        #Return calculated year of death
        return int(birth_year + life_exp + adjustment)
    #Birth rate to child count probability range logic refined with ChatGPT assistance
    def get_num_children(self, parent_birth_year):
        #Determine decade of birth
        decade_year = (parent_birth_year // 10) * 10

        #Lookup birth rate for that decade
        birth_rate_value = self.birth_rate[str(decade_year)]

        #Determine range of children (±1.5 rule)
        min_children = math.ceil(birth_rate_value - 1.5)
        max_children = math.ceil(birth_rate_value + 1.5)

        #Ensure minimum is not negative
        min_children = max(0, min_children)

        #Return random number of children in range
        return random.randint(min_children, max_children)
    #Marriage probability handling logic refined with ChatGPT assistance 
    def should_get_partner(self, person_birth_year):
        #Determine decade of birth
        decade_year = (person_birth_year // 10) * 10

        #Lookup marriage probability
        prob = self.marriage_rate[str(decade_year)]

        #Return True with probability equal to marriage rate
        #Probability comparison logic inspired by:
        #https://realpython.com/python-random/
        return random.random() < prob
    
    def get_first_name(self, birth_year, gender):
        #Determine decade of birth
        decade_year = (birth_year // 10) * 10

        #Key is (decade, gender)
        key = (str(decade_year), gender.lower())

        #Fallback to 1950 if decade missing
        if key not in self.first_names:
            key = ("1950", gender.lower())

        #Separate names and weights
        names = [n for (n, w) in self.first_names[key]]
        weights = [w for (n, w) in self.first_names[key]]

        #Return weighted random first name
        #Weighted random selection logic inspired by:
        #https://docs.python.org/3/library/random.html#random.choices
        return random.choices(names, weights=weights, k=1)[0]
    
    def get_last_name(self, birth_year):
        #Determine decade of birth
        decade_year = (birth_year // 10) * 10
        key = str(decade_year)

        #Fallback to 1950 if decade missing
        if key not in self.last_names:
            key = "1950"

        #Separate names and weights
        names = [n for (n, w) in self.last_names[key]]
        weights = [w for (n, w) in self.last_names[key]]

        #Return weighted random last name
        #Weighted random selection logic inspired by:
        #https://docs.python.org/3/library/random.html#random.choices
        return random.choices(names, weights=weights, k=1)[0]
