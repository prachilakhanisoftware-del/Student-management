from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class teachers(models.Model):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,null=True,blank=True
    # )

    teacher_name=models.CharField(max_length=45)
    course = models.CharField(max_length=100)
    t_email = models.EmailField()
    salary = models.IntegerField()

    def __str__(self):
        return self.teacher_name

class students(models.Model):
    name=models.CharField(max_length=40)
    age=models.IntegerField()
    email=models.EmailField(unique=True)
    # course=models.ManyToManyField(courses)
    course=models.CharField(max_length=67, db_index=True
                            )
    photo=models.FileField(upload_to="students/",
)
    teacher=models.ForeignKey(teachers,
                               on_delete=models.CASCADE,
                              related_name="students",    blank=True,
    null=True

                             )
    def __str__(self):
        return self.name

class studentdocument(models.Model):

    DOCUMENT_TYPES = [
        ("Certificate", "Certificate"),
        ("Assignment", "Assignment"),
        ("Marksheet", "Marksheet"),
        ("Notes", "Notes"),
        ("Other", "Other"),
    ]

    student = models.ForeignKey(
        students,
        on_delete=models.CASCADE,
        
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to="student_documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.document_type}"


    # class courses(models.Model):
#     c_name=models.CharField(max_length=100)

#     def __str__(self):
#         return self.c_name