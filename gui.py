"""Working on the Tkinter graphical front end.
This will include widgets, button callsback to core function
display results"""

import tkinter as tk
from tkinter import messagebox
from core import Module, PrerequisiteGraph, Repository, Plan


class CoursePlannerApp:
    """The main GUI application interface"""
    
    def __init__(self, root: tk.Tk) ->None:
        self.root = root
        self.root.title("University Course Planner")
        self.root.geometry("600x500")
        
        # The core state
        self.repo = Repository("data.json")
        self.data = self.repo.load()
        self.catalogue: dict[str, Module] = {}
        self.graph = PrerequisiteGraph()