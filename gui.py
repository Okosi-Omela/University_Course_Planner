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
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        # Tab 1 Catalogue
        self.tab_catalogue = tk.Frame(self.notebook)
        self.notebook.add(self.tab_catalogue, text="Catalogue")
        self.build_catalogue_tab()
        
        
        # Tab 2 Planner
        self.tab_planner = tk.Frame(self.notebook)
        self.notebook.add(self.tab_planner, text="Planner")
        self.build_planner_tab()
        
        
        #  Tab 3 Data
        self.tab_data = tk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text="Save / Load")
        self.build_data_tab()
        
    
    def build_catalogue_tab(self) -> None:
        """Building widgets for adding modules."""
        tk.Label(self.tab_catalogue, text="Add a New Module", font=("Arial",12, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        tk.Label(self.tab_catalogue, text="Module Code:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_code = tk.Entry(self.tab_catalogue)
        self.entry_code.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(self.tab_catalogue, text="Module Title:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_title = tk.Entry(self.tab_catalogue, width=30)
        self.entry_title.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(self.tab_catalogue, text="Credits:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.entry_credits = tk.Entry(self.tab_catalogue)
        self.entry_credits.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(self.tab_catalogue, text="Semester:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.entry_semester = tk.Entry(self.tab_catalogue)
        self.entry_semester.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        tk.Button(self.tab_catalogue, text="Add Module", command=self.add_module).grid(row=5, column=0, columnspan=2, pady=15)
        
        # Listbox to display catalogue
        self.listbox_catalogue = tk.Listbox(self.tab_catalogue, width=60, height=10)
        self.listbox_catalogue.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
        self.refresh_catalogue_list()
        
        
    def build_planner_tab(self) -> None:
        """Building the widgets for planning"""
        tk.Label(self.tab_planner, text="Plan a Semester", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        tk.Label(self.tab_planner, text="Student Name").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_student = tk.Entry(self.tab_planner, width=30)
        self.entry_student.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(self.tab_planner, text="Semester Name").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_semester_name = tk.Entry(self.tab_planner, width=30)
        self.entry_semester_name.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        tk.Button(self.tab_planner, text="Create a Plan", command=self.create_plan).grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Label(self.tab_planner, text="Add Module to Plan", font=("Arial", 11, "bold")).grid(row=5, column=0, columnspan=2, pady=5)
        
        tk.Label(self.tab_planner, text="Module Code:").grid(row=6, column=0,sticky="e", padx=10, pady=5)
        self.entry_add_module = tk.Entry(self.tab_planner, width=30)
        self.entry_add_module.grid(row=5, column=1, sticky="w", padx=10, pady=5)            
        
        tk.Button(self.tab_planner, text="Add to Plan", command=self.add_to_plan). grid(row=7, column=0, columnspan=2, pady=10)
        
        self.label_plan_status = tk.Label(self.tab_planner, text="", fg="blue")
        self.label_plan_status.grid(row=7, column=0, columnspan=2, pady=10)
        
        #Store the current plan
        self.current_plan = None
        
    
    def build_data_tab(self) -> None:
        """Building widgets for saving and loading"""
        tk.Label(self.tab_data, text="Data Management", font=("Arial", 15, "bold")).pack(pady=20)
        tk.Label(self.tab_data, text="Make sure you want to save", fg="grey").pack(pady=5)
        
        save_btn = tk.Button(
            self.tab_data,
            text="SAVE CATALOGUE",
            command=self.save_data,
            font=("Arial",14, "bold"),
            bg="lightgreen",
            activebackground="green"
        )
        save_btn.pack(fill="both", expand=False, padx=10, pady=10)
               
    #the GUI talks to the core.py
    def add_module(self) -> None:
        """Add modules to the catalogue after reading the entry boxes."""
        code = self.entry_code.get().strip()
        title = self.entry_title.get().strip()
        
        if not code or not title:
            messagebox.showerror("Code and Title cannot be Empty.")
            return
        try:
            credits = int(self.entry_credits.get().strip())
        except ValueError:
            messagebox.showerror("Credits must be a number.")
            return
        semester = self.entry_semester.get().strip() or "Not Specified"
        
        new_module = Module(code, title, credits, semester)
        self.catalogue[code] = new_module
        self.graph.add_module(code)
        
        self.refresh_catalogue_list()
        messagebox.showinfo("Success", f"Added {code} to catalogue.")
        
    
    def refresh_catalogue_list(self) -> None:
        """Updating the Listbox to show all the current modules."""
        self.listbox_catalogue.delete(0, tk.END)
        for code, mod in self.catalogue.items():
            self.listbox_catalogue.insert(tk.END, f"{code} - {mod.module_title} ({mod.module_credit} credits)")


    def create_plan(self) -> None:
        """Initialize a Plan object for the student."""        
        student = self.entry_student.get().strip()
        sem = self.entry_semester_name.get().strip()
    
        if not student or not sem:
            messagebox.showerror("Student name and semester are required.")
            return
    
        self.current_plan = Plan(self.catalogue, self.graph)
        self.current_plan.add_semester(sem)
        self.label_plan_status.config(text=f"Created plan for {student} ({sem})")
    
    
    def add_to_plan(self) -> None:
        """Requesting the core to add a module to the active plan"""
        if self.current_plan is None:
            messagebox.showerror("Please create a plan first.")
            return
    
        code = self.entry_add_mod.get().strip()
        sem = self.entry_semester_name.get().strip()
    
        # GUI interacts with the core
        error = self.current_plan.check_add_module(sem, code)
    
        if error:
            messagebox.showerror("Validation Error", error)
        else:
            messagebox.showinfo("success", f"Added {code} to plan, Total credits: {self.current_plan.get_credits(sem)}")
        
    def save_data(self) -> None:
        """Saves the catalogue to JSON"""
        module_dicts = [mod.to_dict() for mod in self.catalogue.values()]
        self.data["modules"] = module_dicts
        self.repo.save(self.data)
        messagebox.showinfo("Successful! Data is saved")
    

if __name__ == "__main__":
    root =  tk.Tk()
    app = CoursePlannerApp(root)
    root.mainloop()
    
    