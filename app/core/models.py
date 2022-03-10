from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER = [
        ("Male", "Nam"),
        ("Female", "Nữ"),
    ]
    id = models.CharField(max_length=6, primary_key=True)
    cccd = models.CharField(max_length=12, null=True, blank=True, unique=True)
    tel = models.CharField(max_length=10, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, null=True, blank=True)
    avatar = models.FileField(null=True, default="avatar.svg")

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.id} -- {self.first_name} {self.last_name}"


class AcademicDepartment(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    dean = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Major(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    department = models.ForeignKey(AcademicDepartment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    salary = models.BigIntegerField(null=True, blank=True)
    department = models.ForeignKey(AcademicDepartment, on_delete=models.CASCADE)

    class Meta:
        ordering = ("user__id",)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class MajorClass(models.Model):
    ENGLISH_LEVEL = [
        ("a", "level 8"),
        ("b", "level 7"),
        ("c", "level 6"),
        ("d", "level 5"),
        ("e", "level 4"),
        ("f", "level 3"),
        ("g", "level 2"),
        ("h", "level 1"),
    ]

    id = models.CharField(max_length=6, primary_key=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True
    )
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    academic_year = models.IntegerField(null=True, blank=True, default=32)
    english_level = models.CharField(
        max_length=1, choices=ENGLISH_LEVEL, null=True, blank=True
    )


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    major_class = models.ForeignKey(MajorClass, on_delete=models.CASCADE)

    class Meta:
        ordering = ("user__id",)

    def __str__(self) -> str:
        return f"{self.user.id} -- {self.user.first_name} {self.user.last_name}"


class AdminstrationDepartment(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    manager = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(AdminstrationDepartment, on_delete=models.CASCADE)
    salary = models.BigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.id} -- {self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)


class Subject(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)
    prerequisite = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, db_constraint=False
    )
    credit = models.IntegerField()
    hour = models.IntegerField(null=True, blank=True)
    coefficient = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Teacher_Subject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("teacher", "subject")

    def __str__(self) -> str:
        return f"{self.teacher.user.first_name} {self.teacher.user.first_name}({self.teacher.user_id}) -- {self.subject.name}({self.subject.id})"


class Major_Subject(models.Model):
    SUBJECT_TYPE_CHOICES = [
        ("GE", "Giáo dục đại cương"),
        ("FS", "Học phần cơ sở"),
        ("CS", "Học phần bắt buộc"),
        ("ES", "Học phần lựa chọn"),
        ("IG", "Thực tập, khóa luận, chuyên đề tốt nghiệp"),
    ]
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_type = models.CharField(
        max_length=200, choices=SUBJECT_TYPE_CHOICES, null=True, blank=True
    )

    class Meta:
        unique_together = ("major", "subject")

    def __str__(self) -> str:
        return f"{self.major.id} -- {self.subject.id}"


class StudyTime(models.Model):
    SEMESTER_CHOICES = [
        (1, "Học kỳ 1"),
        (2, "Học kỳ 2"),
        (3, "Học kỳ 3"),
    ]
    GROUP_CHOICES = [
        (1, "Nhóm 1"),
        (2, "Nhóm 2"),
        (3, "Nhóm 3"),
    ]
    id = models.CharField(max_length=9, primary_key=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    group = models.IntegerField(choices=GROUP_CHOICES)
    year = models.IntegerField()

    def __str__(self) -> str:
        return f"Học Kỳ: {self.group}, Nhóm: {self.semester}, Năm: {self.year}"


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher_subject = models.ForeignKey(Teacher_Subject, on_delete=models.CASCADE)
    study_time = models.ForeignKey(StudyTime, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "study_time")

    def __str__(self) -> str:
        return f"{self.name} {self.study_time}"


class Student_Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "course")


class Attendance(models.Model):
    student_course = models.ForeignKey(Student_Course, on_delete=models.CASCADE)
    lesson = models.IntegerField(null=True, blank=True)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student_course", "lesson")


class Grade(models.Model):
    student_course = models.OneToOneField(
        Student_Course, on_delete=models.CASCADE, primary_key=True
    )
    mid_term_grade = models.FloatField(default=-1)
    final_grade = models.FloatField(default=-1)

    def __str__(self) -> str:
        return f"{self.student.user} -- {self.course.subject}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_time = models.ForeignKey(StudyTime, on_delete=models.CASCADE)
    paid_date = models.DateTimeField(auto_created=True)
    amount = models.BigIntegerField()

    class Meta:
        unique_together = ("user", "study_time")
