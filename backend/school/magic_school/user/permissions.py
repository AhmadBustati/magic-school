from rest_framework import permissions


class IsStudent(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_student():
            return True
        return False


class IsTeacher(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_teacher:
            return True
        return False

class IsStuff(permissions.IsAuthenticated):# teacher or employye
    def has_permission(self, request, view):
        if request.user.is_employee or request.user.is_teacher:
            return True
        return False

class IsManager(permissions.IsAuthenticated):# manager or employye
    def has_permission(self, request, view):
        if request.user.is_employee or request.user.is_manager:
            return True
        return False
