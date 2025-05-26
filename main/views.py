from django.shortcuts import render
from django.db.models import Avg
from .models import Student, Grade


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

