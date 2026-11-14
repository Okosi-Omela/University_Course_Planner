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

from core import Module, Student, Repository, PrerequisiteGraph, kahn_topological_sort

def test_topological_sort_produces_valid_order():
    graph = PrerequisiteGraph()
    graph.add_prerequisite("CSC44101", "CSC44102")
    graph.add_prerequisite("CSC44101", "CSC44103")
    graph.add_prerequisite("CSC44102", "CSC44104") 
    graph.add_prerequisite("CSC44102", "CSC44105")
    graph.add_prerequisite("CSC44103", "CSC44105")
    graph.add_prerequisite("CSC44104", "CSC44201")
    
    order = kahn_topological_sort(graph)
    
    assert order is not None
    # Prerequite should appear before it's dependent
    position = {code: index for index, code in enumerate(order)}
    for prerequisite, dependents in graph.dependents.items():
        for prerequisite, dependents in graph.dependents.items():
            for dependent in dependents:
                assert position[prerequisite] < position[dependent]
                
def test_topological_sort_includes_every_module():
    graph = PrerequisiteGraph()
    graph.add_prerequisite("CSC44101", "CSC44102")
    graph.add_prerequisite("CSC44102", "CSC44103")
    graph.add_module("CSC44201")
    
    
    order = kahn_topological_sort(graph)
    
    
    assert order is not None
    assert len(order) == 4
    assert set(order) == {"CSC44101", "CSC44102", "CSC44103", "CSC44201"}
    
    
def test_topological_sort_detects_cycles():
    graph = PrerequisiteGraph()
    graph.add_prerequisite("CSC44101", "CSC44102")  # Create a cycle: B requires A, A requires B
    graph.add_prerequisite("CSC44102", "CSC44103")   # C requires B
    graph.add_prerequisite("CSC44103", "CSC44101")   # A requires C, completing the cycle

    order = kahn_topological_sort(graph)

    assert order is None  # Should return None when a cycle is detected
