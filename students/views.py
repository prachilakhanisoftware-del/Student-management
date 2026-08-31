from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Count,Q

from .models import students
from .models import teachers
from .forms import Studentform
from .forms import Registerform,StudentDocumentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.core.paginator import Paginator
import logging

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



logger=logging.getLogger(__name__)

def home(request):
    return render(request, "students/home.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )
        
        if user is not None:
            if user.groups.filter(name="teachers").exists():

               login(request, user)

            messages.success(
                    request,
                    "Login successful"
                )

            return redirect("dashboard")

        else:

            return render(
                request,
                "students/login.html",
                {
                    "error": "Invalid Username or Password"
                }
            )

    return render(request, "students/login.html")

from django.contrib.auth.models import User, Group

def register(request):

    if request.method == "POST":

        form = Registerform(request.POST)

        if form.is_valid():

            user=User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            teacher_group = Group.objects.get(name="teachers")

            user.groups.add(teachers)
        messages.success(
    request,
    "Registration Successful."
)
        return redirect("login")

    else:

        form = Registerform()

    return render(
        request,
        "students/register.html",
        {"form": form}
    )
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import students, teachers


class dashboard(LoginRequiredMixin, ListView):

    model = students
    template_name = "students/dashboard.html"
    context_object_name = "students"
    paginate_by = 8
    login_url = "login"
   
    def get_queryset(self):
        print(self.request.user)
        print(self.request.user.groups.all())

        queryset = students.objects.all().order_by('-id')

        course = self.request.GET.get("course")
        teacher = self.request.GET.get("teacher")
        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort")

        if course:
            queryset = queryset.filter(course=course)

        if teacher:
            queryset = queryset.filter(teacher_id=teacher)

        if search:
            queryset = queryset.filter(Q(name__icontains=search) |  Q(email__icontains=search))


        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["total_students"] = students.objects.count()

        context["total_teachers"] = teachers.objects.count()

        context["total_courses"] = students.objects.values("course").distinct().count()
        context["teachers"] = teachers.objects.all()
        context["students"] = context["page_obj"]
        return context

       
    
# from django.contrib import messages
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
# class StudentCreateView(LoginRequiredMixin, CreateView):

#     model = students

#     form_class = Studentform

#     template_name = "students/add_students.html"

#     success_url = reverse_lazy("dashboard")

#     def form_valid(self, form):

#         messages.success(
#             self.request,
#             "Student added successfully."
#         )

#         return super().form_valid(form)

def add_students(request):

    if request.method == "POST":
        
    #  print(request.FILES)       

     form=Studentform(request.POST,request.FILES)
     if form.is_valid():
        
        form.save()
        logger.info("Student Added Successfully")

        messages.success(
        request,
        "Student added successfully."
    )
        return redirect("dashboard")

    else:
         form=Studentform()
         logger.error(form.errors)
    

        # name = request.POST["name"]
        # age = request.POST["age"]
        # email = request.POST["email"]
        # course = request.POST["course"]

        # students.objects.create(
        #     name=name,
        #     age=age,
        #     email=email,
        #     course=course
        # )


    return render(request, "students/add_students.html", {
        "form": form})
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

class delete_students(LoginRequiredMixin, DeleteView):

    model = students

    template_name = "students/student_confirm_delete.html"

    success_url = reverse_lazy("dashboard")

    def post(self, request, *args, **kwargs):
        logger.info("student deleted successfully")
        messages.error(
            request,
            "Student deleted successfully."
        )

        return super().post(request, *args, **kwargs)
# def delete_students(request,id):
#     s1=students.objects.get(id=id)
#     s1.delete()
#     messages.success(
#             request,
#             "Student deleted successfully."
#         )
#     return redirect("dashboard")
# from django.views.generic import UpdateView
# from django.urls import reverse_lazy
# from django.contrib import messages

# class StudentUpdateView(LoginRequiredMixin, UpdateView):

#     model = students

#     form_class = Studentform

#     template_name = "students/update_students.html"

#     success_url = reverse_lazy("dashboard")

#     def form_valid(self, form):

#         messages.success(
#             self.request,
#             "Student updated successfully."
#         )

#         return super().form_valid(form)
def update_students(request, id):

    student = students.objects.get(id=id)

    if request.method == "POST":

        form = Studentform(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()
            logger.info("student updated successfully")

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("dashboard")

    else:

        form = Studentform(instance=student)

    return render(
        request,
        "students/update_students.html",
        {
            "form": form
        }
    )
  

def user_logout(request):

    logout(request)
    messages.warning(
        request,
        "Logout"
    )
    return redirect("/")

def add_document(request, id):

    student = get_object_or_404(students, id=id)

    if request.method == "POST":

        form = StudentDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(commit=False)

            document.student = student

            document.save()
            logger.info("Document uploaded successfully")

            messages.success(
                request,
                "Document uploaded successfully."
            )

            return redirect("dashboard")

    else:

        form = StudentDocumentForm()

    return render(
        request,
        "students/add_document.html",
        {
            "form": form,
            "student": student,
        }
    ) 


def student_documents(request, id):

    student = get_object_or_404(students, id=id)

    documents = student.documents.all()

    return render(
        request,
        "students/student_documents.html",
        {
            "student": student,
            "documents": documents,
        }
    )

from django.views.generic import DetailView

class StudentDetailView(LoginRequiredMixin, DetailView):

    model = students

    template_name = "students/student_detail.html"

    context_object_name = "student"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["documents"] = self.object.documents.all()

        return context



from .models import studentdocument

def documents(request):

    documents = studentdocument.objects.select_related("student")

    return render(request, "students/documents.html", {
        "documents": documents
    })



from .models import teachers
# @permission_required("teachers.teacher_list")
from django.views.decorators.cache import cache_page
@cache_page(60 * 5)
def teacher_list(request):
    print("database hit")
    teacher = teachers.objects.all()


    return render(request, "students/teachers.html", {
        "teachers": teacher
    })



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password Changed Successfully")

            return redirect("dashboard")

    else:

        form = PasswordChangeForm(request.user)

    return render(request, "students/security.html", {"form": form})
# ____________________________________________________________



# @login_required



# def dashboard(request):

#         if not request.user.is_authenticated:

#           messages.warning(
#             request,
#             "Please login first to access this page."
#         )

#           return redirect("login")

       
#         course = request.GET.get("course")
#         sort = request.GET.get("sort")
#         teacher = request.GET.get("teacher")
#         search = request.GET.get("search")
#         # Start with all students
#         all_student = students.objects.all()

# # Course filter
#         if course:
#             all_student = all_student.filter(course=course)

# # Teacher filter
#         if teacher:
#          all_student = all_student.filter(teacher_id=teacher)
#         teachers_list = teachers.objects.all()

# #search by name
        

#         if search:
         
#          all_student = all_student.filter(name__icontains=search)
# # Sorting
#         if sort:
#          all_student = all_student.order_by(sort)



#         paginator=Paginator(all_student,5)
#         page_number=request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(
#     request,
#     "students/dashboard.html",
#     {
#         "students": page_obj,
#         "teachers": teachers_list,
#     }
# )


