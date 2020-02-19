from django.contrib.auth.forms import UserCreationForm
from query.models import User

# Form for user register
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
