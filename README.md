# University Course Planner
A python application using Tkinker GUI, designed for academic advisors to manage an undergraduated Computer Science module catalogue and build valid, credit-checked study plans for students.

This application features a strick seperation of concerns: a single core logic engine drives both a Command Line Interface (CLI) and a Graphical User Interface (GUI).

## UK Higer Education Standards

This application is modelled specifically around the standard framework.
**1. Credit framework:** A full-time student load is exactly 120 UK credits per year.
**2. Module sizes:** Modules are modelled in standard 15-credit and 30-credit blocks.
**3. Proression:** Prerequisite graph enforces progression, meaning a student cannot take a Level 5 module without first passing the level 4 preequisite modules.
**4. Validation:** The application prevents advisors from assigning more than 120 credits to a single academic year.

## Features
**Module Catalogue** Adds modules with specific codes( for example CSC10087), title, and UK-standard credits.
**Prerequisite Validation** The application prevents a student from being scheduled for a module if they have not passed the prerequisite.
**Credit Capping:** The application enforces a strict maximum of 120 credits per year, preventing overloading.
**Data Persistence:** The application saves and loads the entire cataogue and stdent status to a local JSON file.
**Interactive GUI:** A user-friendly tabbed interface for advisors to qyuickly build plans.
**Command Line Interface (CLI):** A fast terminal-based alternative for power users.


## Architecture

The application is built using layered architecture to ensure clean, maintainable code:
1. **`core.py` The Engine:** Contains all business logic, data models (`Module`, `Student`), persistence (`Repository`), and algorithms (Kahn's Topological Sort, `Plan` validation).
2. **`cli.py` Text Front-End:** A thin wrapper that collects text input and talks to `core.py`.
3. **`gui.py` Graphical Front-End:** A Tkinter interface that renders buttons and inputs, delegating all validation and data handling to `core.py`.

## Algorihims and Data Structures
**Graphs and Topological Sort:** Prerequisites are modelled as a Directeed Acyclic Graph (DAG) using an adjacent list. We use **Kahn's Algorithm** to detect cycles and generate a valid course order in `O(V + E)` time.
**Greedy Validation:** The `Plan` class ats as a statefule validator, instantly checking prerequisites and credit caps before allowing a module to be added to a semester.

## How to Run the Application

### Prerequisite
Download and install Python 3.10+ if you already do not have it installed.

 **Clone the Repository:**
```bash
git clone https://github.com/Okosi-Omela/University_Course_Planner.git
cd University_Vourse_Planner
```
**Set up a virtual environment:**
python -m venv .venv 
# On Windows:
.venv\Scrips\activate
# On MacOS/Linus:
source .venv/bin/activate

**Install Requirement**
run
pip install -r requirements.txt

**Run the GUI**
run 
python gui.py

**Run the CLI**
run
python cli.py

## Testing
run 
pytest -v
