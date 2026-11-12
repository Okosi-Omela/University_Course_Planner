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

   def to_dict(self) -> dict:
        """Return a JSON-ready dict representation of this module"""
        
        return {
            "module_code": self.module_code,
            "module_name": self.module_name,
            "module_credit": self.module_credit,
            "semester": self.semester
        } # type: ignore
   
   @classmethod
   def from_dict(cls, data: dict) -> "Module":
        """This will build a Module from a dictionary
        'cls' is the module class itself, and it is passed automatically because this
        is a class method."""
        
        return cls(
            module_code=data["module_code"],
            module_name=data["module_name"],
            module_credit=data["module_credit"],
            semester=data["semester"]
        )
        

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

   def to_dict(self) -> dict:
        """Return a JSON-ready dict representation of this student"""
        
        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "completed_modules": self.completed_modules
        } # type: ignore

   @classmethod
   def from_dict(cls, data: dict) -> "Student":
        """This will build a Student from a dictionary
        'cls' is the student class itself, and it is passed automatically because this
        is a class method."""
        
        return cls(
            student_id=data["student_id"],
            student_name=data["student_name"],
            completed_modules=data["completed_modules"]
        )
        
class Repository:
    """This block loads and saves the whole planner state o a JSON file
    This is the only class in the application that touches the filesystem, Everyother parts of the
    code communicates with this class, never directly to files. It is this seperation that will allow
    the CLI nad GUI to share one core logic. """
    
    
    def __init__(self, path: str = "data.json") -> None:
        self.path = Path(path)
        
    def load(self) -> dict:
        """" Returns the saved state as a dictionary.
        The application should start clean upon first run. It should return an empty catalogue"""
        
        if not self.path.exists():
            return {"modules": [], "students": []}
        text = self.path.read_text(encoding="utf-8")
        return json.loads(text)
    
    def save(self, data: dict) -> None:
        """Saves the state of the application to a JSON file"""
        
        text = json.dumps(data, indent=2)
        self.path.write_text(text, encoding="utf-8")