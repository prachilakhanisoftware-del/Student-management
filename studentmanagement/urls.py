"""
URL configuration for studentmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from students import views
# from students.apiview import StudentListCreateView, StudentDetailView
# from students.apiview import StudentAPIView,StudentDetailAPIView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from students.apiview import StudentViewSet,LoginAPIView,LogoutView,HealthCheckAPIView,SentryTestAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
router = DefaultRouter()

router.register(
    "students",
    StudentViewSet,
    basename="student"
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path("add_students/", views.add_students, name="add_students"),
    path("delete/<int:pk>/", views.delete_students.as_view(), name="delete_students"),
    path("update/<int:id>/",views.update_students,name="update_students"),
    path("register/",views.register,name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("dashboard/", views.dashboard.as_view(), name="dashboard"),
    path("student/<int:id>/documents/add/", views.add_document,name="add_document"),
    path("student/<int:id>/documents/",views.student_documents,name="student_documents"),

    path("student/<int:pk>/",views.StudentDetailView.as_view(), name="student_detail"),
    path("documents/", views.documents, name="documents"),
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("security/",views.change_password,name="change_password"),

    path("accounts/", include("allauth.urls")),  
     path(
        "api/login/",
        LoginAPIView.as_view(),
       name="api-login"
    ),
        # OpenAPI schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
        path("api/", include(router.urls)),

    path(
    "api/token/",
    TokenObtainPairView.as_view(),
    name="token_obtain_pair",
),

path(
    "api/token/refresh/",
    TokenRefreshView.as_view(),
    name="token_refresh",
),
path("api/health/", HealthCheckAPIView.as_view()),
path("api/logout/", LogoutView.as_view()),
path("sentry-test/", SentryTestAPIView.as_view()),
#  path(
#         "api/students/",
#         StudentAPIView.as_view(),
#         name="student-api"
#     ),

#     path(
#     "api/students/<int:id>/",
#     StudentDetailAPIView.as_view(),
#     name="student-detail-api"
# ),

#  path("api/students/", StudentListCreateView.as_view(), name="student-list"),
#     path("api/students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
]




urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

# fetch("http://127.0.0.1:8000/api/students/", {
#     method: "GET",
#     headers: {
#         "Authorization": "Bearer YOUR_ACCESS_TOKEN"
#     }
# })
# .then(response => response.json())
# .then(data => console.log(data));



# const accessToken = "PASTE_YOUR_ACCESS_TOKEN_HERE";
# const refreshToken = "PASTE_YOUR_REFRESH_TOKEN_HERE";

# fetch("http://127.0.0.1:8000/api/logout/", {
#     method: "POST",
#     headers: {
#         "Authorization": "Bearer " + accessToken,
#         "Content-Type": "application/json"
#     },
#     body: JSON.stringify({
#         refresh: refreshToken
#     })
# })
# .then(response => response.json())
# .then(data => console.log(data));



