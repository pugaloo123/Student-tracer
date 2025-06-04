from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from collections import defaultdict

from .models import Student, Grade, Group, Subject
from .forms import GroupForm, StudentForm, SubjectForm, AddSubjectToGroupForm, GradeForm



def home(request):
    groups = Group.objects.all()
    return render(request, 'main/home.html', {'groups': groups})


def report(request):
    students = Student.objects.all()
    student_avg = []

    for student in students:
        avg = Grade.objects.filter(student=student).aggregate(Avg('grade'))['grade__avg'] or 0
        student_avg.append((student, round(avg, 2)))

    best = max(student_avg, key=lambda x: x[1], default=None)
    worst = min(student_avg, key=lambda x: x[1], default=None)

    return render(request, 'main/report.html', {
        'student_avg': student_avg,
        'best': best,
        'worst': worst
    })


'''Group views'''
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'main/group_list.html', {'groups': groups})


def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    students = Student.objects.filter(group=group)
    subjects = group.subjects.all()

    student_data = []

    for student in students:
        grade_dict = {}
        for subject in subjects:
            grades_qs = Grade.objects.filter(student=student, subject=subject)
            avg_grade = grades_qs.aggregate(avg=Avg('grade'))['avg']
            grade_dict[subject.title] = round(avg_grade, 2) if avg_grade is not None else '-'

        avg_total = [
            v for v in grade_dict.values()
            if isinstance(v, (int, float))
        ]
        avg = round(sum(avg_total) / len(avg_total), 2) if avg_total else '-'

        student_data.append({
            'student': student,
            'grades': grade_dict,
            'avg': avg
        })

    numeric_data = [s for s in student_data if isinstance(s['avg'], (int, float))]
    best = max(numeric_data, key=lambda x: x['avg'], default=None)
    worst = min(numeric_data, key=lambda x: x['avg'], default=None)

    return render(request, 'main/group_detail.html', {
        'group': group,
        'students': students,
        'subjects': subjects,
        'student_data': student_data,
        'best': best,
        'worst': worst,
    })

def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = GroupForm()
    return render(request, 'main/group_form.html', {'form': form, 'title': 'Создать группу'})

def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = GroupForm(instance=group)
    return render(request, 'main/group_form.html', {'form': form, 'title': 'Редактировать группу'})

def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('main:home')
    return render(request, 'main/group_confirm_delete.html', {'group': group})


'''Student views'''
def student_create(request):
    group_id = request.GET.get('group')
    initial = {'group': group_id} if group_id else None

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            if group_id:
                return redirect('main:group_detail', group_id=group_id)
            else:
                return redirect('main:home')
    else:
        form = StudentForm(initial=initial)
    return render(request, 'main/student_form.html', {'form': form, 'title': 'Добавить студента'})


def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('main:group_detail', group_id=student.group.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'main/student_form.html', {'form': form, 'title': 'Редактировать студента'})

def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('main:group_detail', group_id=student.group.id)
    return render(request, 'main/student_confirm_delete.html', {'student': student})

'''Subjects view'''
# views.py

# def subject_create_for_group(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#
#     if request.method == 'POST':
#         form = SubjectForm(request.POST)
#         if form.is_valid():
#             subject = form.save()
#             group.subjects.add(subject)  # Добавляем предмет только этой группе
#             return redirect('main:group_detail', group_id=group.id)
#     else:
#         form = SubjectForm()
#
#     return render(request, 'main/subject_form.html', {
#         'form': form,
#         'group': group,
#         'title': 'Добавить предмет в группу'
#     })

def add_subject_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = AddSubjectToGroupForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            group.subjects.add(subject)
            return redirect('main:group_detail', group_id=group_id)
    else:
        form = AddSubjectToGroupForm()

    return render(request, 'main/add_subject_to_group.html', {
        'form': form,
        'group': group
    })


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'main/subject_list.html', {'subjects': subjects})


def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'main/subject_form.html', {'form': form, 'title': 'Добавить предмет'})


def subject_edit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('main:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'main/subject_form.html', {'form': form, 'title': 'Редактировать предмет'})


def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        return redirect('main:subject_list')
    return render(request, 'main/subject_confirm_delete.html', {'subject': subject})

"""Grades"""



def grades_table(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = Grade.objects.filter(student=student).select_related('subject')
    return render(request, 'main/grades_table.html', {
        'student': student,
        'grades': grades,
    })


def add_grade(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.save()
            return redirect('main:grades_table', student_id=student.id)
    else:
        form = GradeForm()
    return render(request, 'main/add_edit_grade.html', {
        'form': form,
        'student': student,
        'grade': None
    })

def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('main:grades_table', student_id=grade.student.id)
    else:
        form = GradeForm(instance=grade)
    return render(request, 'main/add_edit_grade.html', {
        'form': form,
        'student': grade.student,
        'grade': grade
    })



def delete_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    student = grade.student

    if request.method == 'POST':
        grade.delete()
        return redirect('main:grades_table', student.id)

    return render(request, 'main/confirm_delete_grade.html', {'grade': grade})

