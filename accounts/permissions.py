from rest_framework import permissions


class IsownerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self,request,view):
        return False
    def has_object_permission(self,request,view,obj):
        
#        if request.method in permissions.SAFE_METHODS:
#            return True
#        
#        print(obj.user)
#        print(request.user)
#        return obj.user == request.user
        return False
#    