from django import forms
from .models import Group, Student, Subject, Grade

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subjects': forms.CheckboxSelectMultiple,
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddSubjectToGroupForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Выберите предмет",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'grade']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'min': 2, 'max': 5, 'step': 0.1}),
        }

