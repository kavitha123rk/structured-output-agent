from pydantic import BaseModel, ValidationError
import pytest


# Student output structure
class Student(BaseModel):
    name: str
    age: int
    department: str


# Test 1: Valid student information
def test_valid_student():

    student = Student(
        name="Rahul",
        age=22,
        department="Mechanical Engineering"
    )

    assert student.name == "Rahul"
    assert student.age == 22
    assert student.department == "Mechanical Engineering"


# Test 2: Invalid age
def test_invalid_age():

    with pytest.raises(ValidationError):
        Student(
            name="Rahul",
            age="twenty-two",
            department="Mechanical Engineering"
        )


# Test 3: Missing student name
def test_missing_name():

    with pytest.raises(ValidationError):
        Student(
            age=22,
            department="Mechanical Engineering"
        )


# Test 4: Invalid age type
def test_invalid_age_type():

    with pytest.raises(ValidationError):
        Student(
            name="Rahul",
            age="hello",
            department="Computer Science"
        )