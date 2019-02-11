from django.contrib.auth.models import User


    

class EmailAuthBackend(object):
    """
    authenticate using email address
    """
    def authenticate(self,username=None,password=None):
        print('hhhhhhhhhhhhhhhhhhhhhhhhh')
        try:
          user= User.objects.get(email=username)
          print('user found')
          print(user)

          if user.check_password(password):
             print(user)
             print('user')
             return user
          print('not pass')
          return None
        except User.DoesNotExist:
           print('user not found')
           return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


