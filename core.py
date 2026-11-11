"""The Core logic of University Course Planner python application."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Module:
   """ 
   attributes:  
   module_code: A unique code to represent each module for example "CSC44102".
   module_name: The name of the module for example "Foundations of Programming".
   module_credit: The number of credits for the module.
   semester: The semester in which the module is offered.
   
   """
    
   module_code: str
   module_name: str
   module_credit: int
   semester: str


@dataclass
class Student:
   """
   attributes:
   student_id: This is a unique  id for example "S0001".
   student_name: This is the full name of a student for example "Ommy Oma".
   completed_modules: Shows codes of modules the student passed.
   
   """
    
   student_id: str
   student_name: str
   completed_modules: list[str] = field(default_factory=list)   
    