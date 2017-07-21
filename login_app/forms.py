from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class ContactForm(forms.Form): #The actual app form. Add any fields necessary here.
    your_email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea, required=False)
    quality = forms.ChoiceField(label='Quality', widget=forms.Select(), choices=(('Best', 'Best'),
                                                                                 ('High', 'High'),
                                                                                 ('Normal', 'Normal')), required=True)
    material = forms.ChoiceField(label='Material', widget=forms.Select(), choices=(('PLA', 'PLA'),
                                                                                   ('ABS', 'ABS')), required=True)
    color = forms.ChoiceField(label='Color', widget=forms.Select(), choices=(('White', 'White'),
                                                                             ('Red', 'Red'),
                                                                             ('Green', 'Green'),
                                                                             ('Blue', 'Blue'),
                                                                             ('Black', 'Black'),
                                                                             ('Purple', 'Purple'),
                                                                             ('Yellow', 'Yellow')), required=True)
    quantity = forms.IntegerField(label='Quantity', required=True)
