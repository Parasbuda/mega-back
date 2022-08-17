from rest_framework.permissions import BasePermission


class BranchPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.group, "gg")
        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False

        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True

        if int(request.user.group) == 1 or int(request.user.group) == 3:
            return True
        return False


class DistrictPermission(BasePermission):
    def has_permission(self, request, view):
        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False

        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True

        if int(request.user.group) == 1 or int(request.user.group) == 3:
            return True
        return False


class PrintPermission(BasePermission):
    def has_permission(self, request, view):

        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False

        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True

        if int(request.user.group) == 1 or int(request.user.group) == 2:
            return True
        return False


class PrintReportPermission(BasePermission):
    def has_permission(self, request, view):
        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False

        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True

        if int(request.user.group) == 1:
            return True
        return False
