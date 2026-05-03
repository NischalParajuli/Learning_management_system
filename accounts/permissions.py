from rest_framework.permissions import BasePermission

class BaseRolePermisson(BasePermission):
  allowed_roles = []


  def has_permission(self, request, view):
    return (
      request.user.is_authenticated 
      and request.user.role in self.allowed_roles
    )
  
class IsAdmin(BaseRolePermisson):
  allowed_roles = ['admin']

class IsInstructor(BaseRolePermisson):
  allowed_roles = ['instructor']

class IsSponsor(BaseRolePermisson):
  allowed_roles = ['sponsor']

class IsStudent(BaseRolePermisson):
  allowed_roles = ['student']

