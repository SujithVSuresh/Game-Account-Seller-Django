from email.mime import image
from pyexpat import model
from django import forms
from .models import GameAccounts, PostImage


class GameAccountForm(forms.ModelForm):

    class Meta:
        model = GameAccounts
        fields = ('rate', 'description', 'game', 'acc_owner')
        widgets = {
            'acc_owner': forms.HiddenInput(),
            }    
   

class ImageForm(forms.ModelForm):

    class Meta:
        model = PostImage
        fields = ('images', 'game_account') 
        widgets = {
            'game_account': forms.HiddenInput(),
            }  
            

