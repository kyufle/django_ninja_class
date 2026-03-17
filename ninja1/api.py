from ninja import NinjaAPI, Schema
from typing import List, Optional
from datetime import date
from employees.models import Employee
from django.shortcuts import get_object_or_404

api = NinjaAPI()

# --- 1. Definición de SCHEMAS (Deben ir ARRIBA) ---

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int
    birthdate: Optional[date] = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: Optional[int] = None
    birthdate: Optional[date] = None

# --- 2. Definición de RUTAS (Deben ir ABAJO de los schemas) ---

@api.get("/hello")
def hello(request):
    return "Hello world"

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    return Employee.objects.all()

@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    return get_object_or_404(Employee, id=employee_id)

@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}