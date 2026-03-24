from django.contrib.auth import authenticate as django_authenticate
from ninja.security import HttpBasicAuth, HttpBearer
from ninja import NinjaAPI, Schema
from typing import List, Optional
from datetime import date
from employees.models import Employee
from django.shortcuts import get_object_or_404
import secrets

api = NinjaAPI()


# Autenticació bàsica
class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = django_authenticate(username=username, password=password)
        if user:
            # Genera un token simple
            token = secrets.token_hex(16)
            user.auth_token = token
            user.save()
            return token
        return None

 
# Autenticació per Token Bearer
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = Usuari.objects.get(auth_token=token)
            return user
        except Usuari.DoesNotExist:
            return None
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

@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.get("/employees", response=List[EmployeeOut], auth=AuthBearer())
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}

@api.post("/employees", response=EmployeeOut)
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return employee