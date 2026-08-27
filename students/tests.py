from django.test import TestCase,Client 
from django.contrib.auth.models import User,Group
from .models import students,teachers,studentdocument
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import Registerform
# Create your tests here.

class StudentTest(TestCase):
   

    def test_cerate_stud(self):

        t1=teachers.objects.create(
                    teacher_name="priya",
                    course="Django",
                    t_email="p@gmail.com",
                    salary=60000
                )
        self.assertEqual(t1.teacher_name,"priya")
        self.assertEqual(t1.course,"Django")
        self.assertEqual(t1.t_email,"p@gmail.com")
        self.assertEqual(t1.salary,60000)

          
        photo= SimpleUploadedFile("image4.png",
             b"file_content",
             content_type="image/png")
        s1=students.objects.create(
            name="vidhya",
            age="21",
            email="v@gmail.com",
            course="Python",
            photo=photo,
            teacher=t1
        )
        self.assertEqual(s1.name,"vidhya")
        self.assertEqual(s1.age,"21")
        self.assertEqual(s1.email,"v@gmail.com")
        self.assertEqual(s1.course,"Python")
        self.assertEqual(s1.teacher.teacher_name, "priya")
        self.assertTrue(s1.photo.name.startswith("students/image4"))

        document = SimpleUploadedFile(
            "certificate.pdf",
            b"pdf_content",
            content_type="application/pdf"
        )

        doc = studentdocument.objects.create(
            student=s1,
            document_type="Certificate",
            file=document
        )
        self.assertEqual(doc.student.name, "vidhya")
        self.assertEqual(doc.document_type, "Certificate")
        self.assertTrue(doc.file.name.endswith(".pdf"))

    def test_register_form_valid(self):

        form = Registerform(
            data={
                "username": "rahul",
                "email": "rahul@gmail.com",
                "password": "Rahul@123"
            }
        )

        self.assertTrue(form.is_valid())

class StudentIntegrationTest(TestCase):

    def setUp(self):

        self.client = Client()

    def test_home_page(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


    def test_login(self):

        teacher_group = Group.objects.create(name="teachers")

        user = User.objects.create_user(
                username="rahul",
                password="12345678"
    )
        user.groups.add(teacher_group)

        response = self.client.post(
        "/login/",
        {
            "username": "rahul",
            "password": "12345678"
        }
    )

        self.assertRedirects(response, "/dashboard/")