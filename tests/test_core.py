"""test for core.py
This should call the core module directly to verify the if the logic behaves as it should
"""

from core import Module, Student, Repository


def test_module_equality_uses_field_values():
    a = Module("CSC44102", "Foundations of Programming", 15, "Fall")
    b = Module("CSC44102", "Foundations of Programming", 15, "Fall")
    assert a == b
    
    
def test_module_to_dict_and_back():
    original = Module("CSC44102", "Foundations of Programming", 15, "Fall")
    rebuilt = Module.from_dict(original.to_dict())
    assert rebuilt == original
    
    
def test_students_have_independent_completed_list():
    a = Student("S001", "Ommy Oma")
    b = Student("S002", "Nancy Nanny")
    a.completed_modules.append("CSC44102")
    assert a.completed_modules == ["CSC44102"]
    assert b.completed_modules == []
    

def test_student_to_dict_and_back():
    original = Student("S001", "Ommy Oma", ["CSC44102", "CSC44103"])
    rebuilt = Student.from_dict(original.to_dict())
    assert rebuilt == original
    

def test_repository_save_then_load_roundtrip(tmp_path):
    repo =  Repository(tmp_path / "does_not_exist.json")
    assert repo.load() == {"modules": [], "students":[]}
    

def test_repository_load_returns_empty_when_file_missing(tmp_path):
    repo = Repository(tmp_path / "does_not_exist.json")


def test_repository_save_then_load_roundtrip(tmp_path):
    repo = Repository(tmp_path / "data.json")
    payload = {
        "modules": [Module("CSC44102", "Foundations of Programming", 15, "Fall").to_dict()],
        "students": [Student("S001", "Ommy Oma", ["CSC44102"]).to_dict()]
    } 
    repo.save(payload)
    loaded = repo.load()
    assert loaded == payload