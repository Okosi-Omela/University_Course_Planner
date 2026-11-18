""" This is the command line front end of the application, It asks the user for input
Working mechanism
1. Add module to catalogue
2. Add prerequisite
3. Create a student plan.
4. Add Module to Semester
5. Save Data
6. Load Data
7. Quit
The cli.py collects input from the user, calls the core functions, prints results.

"""
from core import Module, PrerequisiteGraph, Repository, Plan
def show_menu() -> None:
    """ This display the main menu to the user"""
    print("\n--- University Course Planner ---")
    print("1. Add Module to Catalogue")
    print("2. Add Prerequisite")
    print("3. Plan a Student's Semester")
    print("4. Save Data")
    print("5. Quit")
    

def main() -> None:
    """ Runs the main CLI loop."""
    repo = Repository("data.json")
    data = repo.load()
    
    #Building our in-memory catalogue from the save Json data
    catalogue: dict[str, Module] = {}
    for mod_dict in data.get("modules", []):
        module = Module.from_dict(mod_dict)
        catalogue[module.module_code] = module
        
    #building the prerequisite graph
    graph = PrerequisiteGraph()
    for code in catalogue:
        graph.add_module(code)
        
    
    while True:
        show_menu()
        choice = inpu("Select an option (1 - 5): ")
        
        if choice == "1":
            #adds a module
            code = input("Enter module code (e.g., CSC10087): ")
            title = input("Enter module title: ")
            credits = int(input("Enter credits (e.g., 30): "))
            semester = input("Enter semester (e.g., Semester 1): ")
            
            new_module = Module(code, title, credits, semester)
            catalogue[code] = new_module
            graph.add_module(code)
            print(f"Success: Added {code}.")
            
        elif choice == "2":
            #add a prerequisite
            prereq = input("Enter the Prerequisite module code: ")
            dependent = input("Enter the Dependent module code (unlocked by prerequisite): ")
            
            if prereq in catalogue and dependent in catalogue:
                graph.add_prerequisite(prereq, dependent)
                print(f"Success: {prereq} is now a prerequisite for {dependent}.")
            else:
                print("Error: One or both modules codes do not exist in the catalogue. ")
                
        elif choice == "3":
            #Plan a student's semester