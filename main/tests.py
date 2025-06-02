from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Group, Student, Subject, Grade
from .forms import GroupForm, StudentForm, SubjectForm, GradeForm

class ModelTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.student = Student.objects.create(name="John Doe", group=self.group)
        self.subject = Subject.objects.create(title="Math")
        self.group.subjects.add(self.subject)

    def test_group_creation(self):
        self.assertEqual(self.group.name, "Test Group")
        self.assertIn(self.subject, self.group.subjects.all())

    def test_student_creation(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.group, self.group)

    def test_grade_validation(self):
        grade = Grade(student=self.student, subject=self.subject, grade=4.0)
        try:
            grade.full_clean()  # Проверка валидаторов
        except ValidationError:
            self.fail("Grade should be valid with value 4.0")

    def test_invalid_grade(self):
        grade = Grade(student=self.student, subject=self.subject, grade=6.0)
        with self.assertRaises(ValidationError):
            grade.full_clean()  # 6.0 недопустимо


class ViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="View Test Group")

    def test_group_list_view(self):
        response = self.client.get(reverse('main:group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Group")

    def test_group_detail_view(self):
        response = self.client.get(reverse('main:group_detail', args=[self.group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Group")

class FormTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Юристы")
        self.subject = Subject.objects.create(title="Право")
        self.group.subjects.add(self.subject)

    def test_group_form_valid(self):
        form_data = {'name': 'Экономисты', 'subjects': [self.subject.id]}
        form = GroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_group_form_invalid(self):
        form = GroupForm(data={'name': ''})  # Название не задано
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_student_form_valid(self):
        form_data = {'name': 'Анна Иванова', 'group': self.group.id}
        form = StudentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_student_form_invalid(self):
        form_data = {'name': '', 'group': ''}  # оба поля пустые
        form = StudentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('group', form.errors)

    def test_subject_form_valid(self):
        form = SubjectForm(data={'title': 'Философия'})
        self.assertTrue(form.is_valid())

    def test_subject_form_invalid(self):
        form = SubjectForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


    def test_grade_form_invalid_grade(self):
        student = Student.objects.create(name="Петр Петров", group=self.group)
        form = GradeForm(data={'student': student.id, 'subject': self.subject.id, 'grade': 6.0})  # недопустимая оценка
        self.assertFalse(form.is_valid())
        self.assertIn('grade', form.errors)


class GradeFormTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Группа 101")
        self.student = Student.objects.create(name="Иван Иванов", group=self.group)
        self.subject = Subject.objects.create(title="Математика")
        self.group.subjects.add(self.subject)

    def test_grade_form_valid(self):
        form_data = {
            'subject': self.subject.id,
            'grade': 4.0
        }
        form = GradeForm(data=form_data)
        form.instance.student = self.student
        self.assertTrue(form.is_valid(), msg=form.errors)



