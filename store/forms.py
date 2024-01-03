from .models import * #Imports all models from Django's .models module
from django.contrib.auth.forms import UserCreationForm #Imports a Django form class for User Registration
from django.contrib.auth.models import User #Imports built in User model provided by Django for user authentication
from django import forms #Imports base forms module from Django

#Creates a custom registration form that inherits from the built in user creation form
class RegisterForm(UserCreationForm):
    email = forms.EmailField() #Creates email field in form
    
    #Lists the fields that should be included in the form
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    #Creates function save, that is called when the registration form is sent
    def save(self, commit=True):
        user = super().save(commit=False) #Calls the save method from UserCreationForm but doesnt commit changes before input validation
        user.email = self.cleaned_data['email'] #Sets the email attribute of the User object to the validated user input 

        #If the user input is valid, save the User's information
        if commit:
            user.save()
            # Create and associate a customer instance with the relevant User input
            customer = Customer(user=user, name=user.username, email=user.email)
            customer.save() #Commit changes to database

        return user #Returns the user object

#Creates SearchForm class
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search') #Defines searchbar query 


