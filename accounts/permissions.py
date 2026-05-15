"""Permission classes for role-based access control.

Provides permission classes that verify user authentication and role
to enforce access control across different endpoints.
"""

from rest_framework.permissions import BasePermission


class BaseRolePermisson(BasePermission):
    """Base permission class for role-based access control.
    
    Verifies that the user is authenticated and belongs to one of the
    allowed roles for the view.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        """Check if user is authenticated and has allowed role.
        
        Args:
            request: HTTP request object.
            view: View being accessed.
        
        Returns:
            bool: True if user is authenticated and has allowed role.
        """
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsAdmin(BaseRolePermisson):
    """Permission class for admin role."""
    allowed_roles = ['admin']


class IsInstructor(BaseRolePermisson):
    """Permission class for instructor role."""
    allowed_roles = ['instructor']


class IsSponsor(BaseRolePermisson):
    """Permission class for sponsor role."""
    allowed_roles = ['sponsor']


class IsStudent(BaseRolePermisson):
    """Permission class for student role."""
    allowed_roles = ['student']