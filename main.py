from person_factory import PersonFactory
from family_tree import FamilyTree
#Code style follows PEP 8 conventions for indentation, naming, spacing, and documentation.
def main(): 
    """Entry point for generating and interacting with the family tree."""
    print("Reading files...")
    factory = PersonFactory()
    factory.read_files()

    print("Generating family tree...")
    tree = FamilyTree(factory)
    tree.generate_tree()

    while True: 
        print("\nAre you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")

        choice = input("> ").strip().upper()
        if choice == "T":
            print(f"The tree contains {len(tree.people)} people total")
        
        elif choice == "D": 
            decade_counts = {}
            for person in tree.people:
                decade = (person.year_born // 10) * 10
                if decade not in decade_counts:
                    decade_counts[decade] = 0
                decade_counts[decade] += 1
            for decade in sorted(decade_counts):
                print(f"{decade}: {decade_counts[decade]}")

        elif choice == "N":
            name_counts = {}
            for person in tree.people:
                full = person.full_name()
                if full not in name_counts: 
                    name_counts[full] = 0
                name_counts[full] += 1
            duplicates = [name for name in name_counts if name_counts[name] > 1]
            print(f"There are {len(duplicates)} duplicate names in the tree:")
            for name in duplicates:
                print(f"* {name}")
        elif choice == "Q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter T, D, or N.")
if __name__ == "__main__":
    main()