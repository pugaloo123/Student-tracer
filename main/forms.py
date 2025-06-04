from django import forms
from django.forms import modelformset_factory
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
            'grade': forms.NumberInput(attrs={'min': 2, 'max': 5}),
        }

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if not (2 <= grade <= 5):
            raise forms.ValidationError("Оценка должна быть от 2 до 5.")
        return grade


