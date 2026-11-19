"""Working on the Tkinter graphical front end.
This will include widgets, button callsback to core function
display results"""

import tkinter as tk
from tkinter import messagebox, ttk
from core import Module, PrerequisiteGraph, Repository, Plan


class CoursePlannerApp:
    """The main GUI application interface"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("University Course Planner")
        self.root.geometry("600x500")
        
        # The core state
        self.repo = Repository("data.json")
        self.data = self.repo.load()
        self.catalogue: dict[str, Module] = {}
        self.graph = PrerequisiteGraph()
        
        # Load existing modules from the JSON file
        for mod_dict in self.data.get("modules", []):
            module = Module.from_dict(mod_dict)
            self.catalogue[module.module_code] = module
            self.graph.add_module(module.module_code)
            
        
        # Building the UI
        self.build_ui()
        
    
    def build_ui(self) -> None:
        """Creating the tabls and widgets."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(file="both", expand=True, padx=10, pady=10)
        
        
        # Tab 1 Catalogue
        self.tab_catalogue tk.Frame(self.notebook)
        self.notebook.add(self.tab_catalogue, text="Catalogue")
        self.build_catalogue_tab()
        
        
        # Tab 2 Planer
        self.tab_planner = tk.Frame(self.notebook)
        self.notebook.add(self.tab_planner, text="Planner")
        self.build_planner_tab()
        
        
        #  Tab 3 Data
        self.tab_data = tk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text="Save / Load")
        self.build_data_tab()