from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Create our model from the abstractuser model (our customzed model)
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default='avatar.png', upload_to='Profile_Pics')
    '''
        The following two lines are used to login using the email instead of the username,
        the REQUIRED_FIELDS = [] should be written with the USERNAME_FIELD = 'email'
    '''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

