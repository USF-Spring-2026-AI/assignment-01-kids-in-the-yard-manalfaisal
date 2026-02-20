class Person:
    """Represents one individual in the family tree."""
    def __init__(self, first_name, last_name, year_born, year_died):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.year_died = year_died
        self.partner = None
        self.children = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"