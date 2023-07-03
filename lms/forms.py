from django import forms
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import *
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registerInputs'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id': 'email', 'class': 'registerInputs'}))
    group = forms.ChoiceField(
                        choices=(),
                        widget=forms.Select(attrs={'id': 'groups'}),
                        required=False
    )
    newGroup = forms.CharField(widget=forms.TextInput(attrs={'id': 'newGroup', 'class': 'registerInputs'}), label="New Group", required=False)
    class Meta:
        model = PendingAccounts
        fields = ['name', 'username', 'password', 'email', 'group']
        labels = {
            'name': _('Name'),
            'username': _('Desired Username'),
            'password': _('Password'),
            'email': _('E-mail'),
            'group': _("Group/Org")
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        groupNames = RegisteredGroups.objects.all().values_list('name', flat=True)
        groupName_choices = [(name, name) for name in groupNames]
        # Set the choices for the name field
        self.fields['group'].choices = groupName_choices    


    def save(self, commit=True):
        if ((self.cleaned_data['group'] == '') and (self.cleaned_data['newGroup'] == '')):
            return render(self.request, "lms/register.html", {
                "message": "Either select an existing group or enter a new group",
            })
            # raise ValidationError("Either select an existing group or enter a new group")
        
        if (self.cleaned_data['group'] != ''):
            groupName = self.cleaned_data['group']
            self.cleaned_data['group'] = groupName
            


        if (self.cleaned_data['newGroup'] != ''):
            groupName = self.cleaned_data['newGroup']
            if RegisteredGroups.objects.filter(name=groupName).exists():
                return render(self.request, "lms/register.html", {
                "message": "This group name already exists",
                })
                # return ValidationError("This group name already exists")
            self.cleaned_data['group'] = groupName
            
 
        return super(RegisterForm, self).save(commit=commit)
    

class AddCourse(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    class Meta:
        model = Courses
        fields = ['name', 'code']
        labels = {
            'name': _('Course name'),
            'code': _('Course Code (must be unique)')
        }


class AddStudent(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registerInputs'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']
        labels = {
            'name': _('Student name'),
            'username': _('Student username'),
            'password': _('Student password'),
            'email': _('Student E-mail')
        }


class AddTeacher(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registerInputs'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']
        labels = {
            'name': _('Teacher name'),
            'username': _('Teacher username'),
            'password': _('Teacher password'),
            'email': _('Teacher E-mail')
        }


class AddPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'registerInputs'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'registerInputs'}),
        required=False
    )
    file = forms.FileField(
        required=False,
        help_text='max. 20 megabytes'
    )
    class Meta:
        model = Posts
        fields = ['title', 'description', 'file', 'canSubmit']
        labels = {
            'title': _('Post Title'),
            'description': _('Post Description'),
            'file': _('File'),
            'canSubmit': _('Submissions')
        }

class AddSubmission(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'registerInputs'}),
        required=False
    )
    file = forms.FileField(
        required=False,
        help_text='max. 20 megabytes'
    )
    class Meta:
        model = Submissions
        fields = ['text', 'file']
        labels = {
            'text': _('Text Submission'),
            'file': _('File Submission')
        }

    def save(self, commit=True):
        if (('text' not in self.cleaned_data) and ('file' not in self.cleaned_data)):
            raise ValidationError('Either submit Text or File or both')
        return super(AddSubmission, self).save(commit=commit)