from person import Person
import random

class FamilyTree:
    """Generates and stores the entire simulated family tree."""
    def __init__(self, factory):
        self.people = []
        self.factory = factory
       
    def generate_tree(self):
        #Create first two people (born in 1950 and dealth year computed)
        start_last = self.factory.get_last_name(1950)
        p1 = Person("Desmond", start_last, 1950, self.factory.calculate_death_year(1950))
        p2 = Person("Molly", start_last, 1950, self.factory.calculate_death_year(1950))
        #Add them to master list of all people
        self.people.extend([p1,p2])
        #List tracks people we still need to generate children for
        #Tree expansion logic inspired by BFS traversal concepts:
        #https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
        to_process = [p1, p2]

        #Keep going until no more people left to expand
        while to_process:
            current_person = to_process.pop(0)
            if current_person.year_born > 2120:
                continue

            #If this person doesn't have a partner yet, they might get one
            if current_person.partner is None:
                if self.factory.should_get_partner(current_person.year_born):
                    #Partner birth year within +/- 10 years
                    partner_birth_year = current_person.year_born + random.randint(-10,10)
                    partner_birth_year = max(1950, partner_birth_year)
                    if partner_birth_year <= 2120:
                        partner_gender = random.choice(["male", "female"])
                        partner_first = self.factory.get_first_name(partner_birth_year, partner_gender)
                        partner = Person(partner_first, current_person.last_name, partner_birth_year, self.factory.calculate_death_year(partner_birth_year))
                        current_person.partner = partner
                        partner.partner = current_person

                        #Add partner to overall people's list + process list
                        self.people.append(partner)
                        to_process.append(partner)
            if current_person.partner is not None:
                if current_person.year_born > current_person.partner.year_born:
                    continue
            #Randomly decide how many children they have (0 - 2)
            num_children = self.factory.get_num_children(current_person.year_born)
            #Loop once for each child
            for _ in range(num_children):
                child_birth_year = current_person.year_born + random.randint(25,45)
                if child_birth_year > 2120:
                    continue
                child_gender = random.choice(["male", "female"])
                child_first = self.factory.get_first_name(child_birth_year, child_gender)
                child = Person(child_first, current_person.last_name, child_birth_year, self.factory.calculate_death_year(child_birth_year))
                #Adding child to parent's children list
                current_person.children.append(child)
                if current_person.partner is not None:
                    current_person.partner.children.append(child)
                #Adding child to overall people list
                self.people.append(child)
                #Adding children to processing list so THEY can have children later 
                to_process.append(child)

                