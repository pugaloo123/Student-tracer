from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Student, Grade, Group, Subject



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


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'main/group_list.html', {'groups': groups})


def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    students = Student.objects.filter(group=group)
    subjects = Subject.objects.all()

    student_data = []

    for student in students:
        grade_dict = {}
        for subject in subjects:
            # средняя оценка по конкретному предмету
            avg_grade = Grade.objects.filter(student=student, subject=subject).aggregate(avg=Avg('grade'))['avg']
            grade_dict[subject.title] = round(avg_grade, 2) if avg_grade is not None else '-'

        # средний балл по всем предметам
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

    # ищем лучшего и худшего студента
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

