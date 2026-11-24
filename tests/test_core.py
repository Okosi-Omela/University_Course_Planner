"""test for core.py
This should call the core module directly to verify the if the logic behaves as it should
"""

from core import Module, Student, Repository, PrerequisiteGraph, kahn_topological_sort, Plan


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



#Prerequisite graph and topological sort
# it is used by the course planner to determine which module a student can take and in what order. 
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


def test_plan_blocks_module_without_prerequisites():
    m1 = Module("CSC10087", "Computational Foundations", 30, "Semester 1")
    m2 = Module("CSC20109", "Web Technologies and Databases", 30, "Semester 1")
    catalogue = {"CSC10087": m1, "CSC20109": m2}
    
    
    graph = PrerequisiteGraph()
    #To take Web Technologies and Databases, the student must have passed level 4 Computational foundations
    graph.add_prerequisite("CSC10087", "CSC20109")
    
    #A new plan with no completed module
    plan = Plan(catalogue, graph)
    plan.add_semester("Year 1")
    
    #Attemplting to add a module 5 without the level 4 prerequisite
    error = plan.check_add_module("Year 1", "CSC20109")
    
    #It should block it and return an error message
    assert error is not None
    assert "requires CSC10087" in error
    

def test_plan_allow_module_when_prerequisite_is_completed():
    m1 = Module("CSC10087", "Computational Foundations", 30, " Semester 1")
    m2 = Module("CSC20109", "Web Technologies and Databases", 30, "Semester 1")
    catalogue = {"CSC10087": m1, "CSC20109": m2}
    
    graph = PrerequisiteGraph()
    graph.add_prerequisite("CSC10087", "CSC20109")

    # This student has already passed CSC10087 in level 4
    plan = Plan(catalogue, graph, completed_modules=["CSC10087"])
    plan.add_semester("Year 2")
    
    #Adding level 5 modules
    error = plan.check_add_module("Year 2", "CSC20109")
    
    #check if it succeed
    assert error is None
    assert plan.get_credits("Year 2") == 30   
    
def test_plan_enforces_credit_cap():
    #using real level 4 modules
    m1 = Module("CSC10083", "Agile Minds: Development and the Professional World", 30, "Semester 1")
    m2 = Module("CSC10087", "Computational Foundations", 30, "Semester 1")
    m3 = Module("CSC10084", "Problem Solving and Computer Programming", 30, "Semester 1-2")
    m4 = Module("CSC10085", "Introduction to Cybercrime", 15, "Semester 2")
    m5 = Module("CSC10086", "Fundamentals of Computer Systems", 15, "Semester 2")
    
    catalogue = {
        "CSC10083": m1,
        "CSC10087": m2,
        "CSC10084": m3,
        "CSC10085": m4,
        "CSC10086": m5
    }
    graph = PrerequisiteGraph()
    
    # Maximum credit unit allowed per year is 120
    plan = Plan(catalogue, graph, credit_cap=120)
    plan.add_semester("Year 1")
    
    #Add the first four modules 
    plan.check_add_module("Year 1", "CSC10083")
    plan.check_add_module("Year 1", "CSC10087")
    plan.check_add_module("Year 1", "CSC10084")
    plan.check_add_module("Year 1", "CSC10085")
    
    #Trying to add another module to make it up tp 120 credit unit
    error_1 = plan.check_add_module("Year 1", "CSC10086")
    assert error_1 is None
    assert plan.get_credits("Year 1") == 120
    
    #Lets try to add another module that will exceed the required unit of 120, the spp should throw an error
    m6 = Module("CSC10099", "Extra Module", 15, "Semester 2")
    plan.catalogue["CSC10099"] = m6
    error_2 = plan.check_add_module("Year 1", "CSC10099")
    assert error_2 is not None
    assert "exceeds the 120 credit cap" in error_2
    
    
def  test_cli_imports_without_crashing():
    # We just wanted to make sure cli.py has no syntax errors
    #cli.py should be imported alongside core.py
    from cli import show_menu, main
    assert show_menu is not None
    assert main is not None
    
    
def test_gui_imports_without_vrashing():
    from gui import CoursePlannerApp
    assert CoursePlannerApp is not None