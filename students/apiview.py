from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins
from django.shortcuts import get_object_or_404
from .models import students
from .serializers import StudentSerializer
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsTeacherOrAdmin
from rest_framework.filters import (OrderingFilter)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,AllowAny,IsAdminUser)
import logging
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .tasks import send_welcome_message
from django.core.cache import cache
from django.db import connection
from django.db import transaction
from rest_framework.exceptions import ValidationError
logger=logging.getLogger(__name__)

class SentryTestAPIView(APIView):
    def get(self, request):
        raise Exception("🔥 Sentry test error")
 
class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response({
                "error": "Invalid username or password"
            })
        return Response({
            "message": "Login successful",
            "username": user.username
        })
        # token, created = Token.objects.get_or_create(
        #     user=user
        # )

        # return Response({
        #     "token": token.key
        # })

class HealthCheckAPIView(APIView):

    def get(self, request):

        health = {
            "status": "healthy",
            "database": "healthy",
            "redis": "healthy",
        }

        # Check PostgreSQL
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            health["database"] = "unhealthy"

        # Check Redis
        try:
            cache.set("health_check", "ok", timeout=10)

            if cache.get("health_check") != "ok":
                raise Exception("Redis is not responding")

        except Exception:
            health["redis"] = "unhealthy"

        # Overall status
        if (
            health["database"] == "unhealthy"
            or health["redis"] == "unhealthy"
        ):
            health["status"] = "unhealthy"

            return Response(
                health,
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            health,
            status=status.HTTP_200_OK
        )
class StudentViewSet(ModelViewSet):

    queryset = students.objects.all()

    serializer_class = StudentSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]
    def list(self, request, *args, **kwargs):
        cache_key = f"student_list:{request.get_full_path()}"
        print(request.version)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            logger.info("Student list CACHE HIT")
            return Response(cached_data)

        logger.info("Student list CACHE MISS")


        response = super().list(request, *args, **kwargs)
        cache.set(
            cache_key,
            response.data,
            timeout=60
    )

        return response
    
    def perform_create(self, serializer):

      logger.info("Starting student creation")

      try:
         with transaction.atomic():
            student = serializer.save()
            
            logger.info(
                "Student created successfully: %s",
                student.name
            )

            transaction.on_commit(
                lambda: cache.delete_pattern("student_list:*")
            )
            #raise Exception("TESTING STUDENT CREATION ERROR")

            transaction.on_commit(
                lambda: send_welcome_message.delay(
                    student.email,
                    student.name
                )
            )

         logger.info(
            "Transaction committed successfully for student: %s",
            student.name
        )

      except Exception:
        logger.exception("Failed to create student")
        raise ValidationError({
        "error": "Failed to create student",
        "detail": "Something went wrong while creating the student."
    })



    filterset_fields = ["name", "course"]


    ordering_fields = [
        "name",
        "email",
        "age",
        "id",
    ]

    def get_throttles(self):

        if self.action == "list":
            self.throttle_scope = "student_list"

        elif self.action == "profile":
            self.throttle_scope = "student_profile"

        return super().get_throttles()


    def get_permissions(self):

      if self.action == "list":
        permission_classes = [AllowAny]

      elif self.action == "create":
        permission_classes = [IsTeacherOrAdmin]

      elif self.action == "destroy":
        permission_classes = [IsAdminUser]

      else:
        permission_classes = [IsAuthenticated]

      return [permission() for permission in permission_classes]

    
    @action(detail=True, methods=["get"])
    def profile(self, request, pk=None, version=None):
     print("VERSION:", request.version)
     print("PK:", pk)

     student = self.get_object()

     if request.version == "v1":
        return Response({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

     elif request.version == "v2":
        return Response({
            "student_id": student.id,
            "full_name": student.name,
            "email_address": student.email
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )
# Concrete Generic Views


# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# class StudentListCreateView(ListCreateAPIView):
#     queryset = students.objects.all()
#     serializer_class = StudentSerializer

# class StudentDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = students.objects.all()
#     serializer_class = StudentSerializer

# -------------------------mixins--------------------------------------


# class StudentAPIView(

#     mixins.ListModelMixin,

#     mixins.CreateModelMixin,

#     GenericAPIView

# ):
#     queryset = students.objects.all()

#     serializer_class = StudentSerializer


#     def get(self, request):

#         return self.list(request)


#     def post(self, request):

#         return self.create(request)


    
# class StudentDetailAPIView(

#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     GenericAPIView

# ):
#   queryset = students.objects.all()

#   serializer_class = StudentSerializer

#   lookup_field = "id"
#   lookup_url_kwarg = "id"
  
#   def get(self, request, id):

#      return self.retrieve(request, id=id)

#   def put(self, request, id):

#     return self.update(request, id=id)

#   def patch(self, request, id):

#     return self.partial_update(request, id=id)

#   def delete(self, request, id):

#     return self.destroy(request, id=id)

# -------------------------GenericAPIView--------------------------------------
# class StudentAPIView(GenericAPIView):

#     queryset = students.objects.all()

#     serializer_class = StudentSerializer



#     def get(self, request):

#      student = self.get_queryset()

#      serializer = self.get_serializer(
#         student,
#         many=True
#     )

#      return Response(serializer.data)


#     def post(self, request):

#      serializer = self.get_serializer(
#         data=request.data
#     )

#      if serializer.is_valid():

#         serializer.save()

#         return Response(serializer.data)

#      return Response(serializer.errors)

# -------------------------------------API VIEW--------------------------------------------------------------
# class StudentAPIView(APIView):

#     def get(self, request):

#         student = students.objects.all()

#         serializer = StudentSerializer(
#             student,
#             many=True
#         )

#         return Response(serializer.data)

#     def post(self,request):
#         serializer = StudentSerializer(data=request.data)   

#         if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)

#         else:
#             print(serializer.errors)
#             return Response(serializer.errors)

# class StudentDetailAPIView(APIView):

#     def get(self, request, id):

#         student = get_object_or_404(students, id=id)

#         serializer = StudentSerializer(student)

#         return Response(serializer.data)


#     def put(self, request, id):
    
#             student = get_object_or_404(students, id=id)
    
#             serializer = StudentSerializer(
#             student,
#             data=request.data
#         )

#             if serializer.is_valid():

#               serializer.save()

#               return Response(serializer.data)

#             return Response(serializer.errors)

#     def patch(self, request, id):

#         student = students.objects.get(id=id)

#         serializer = StudentSerializer(
#         student,
#         data=request.data,
#         partial=True
#     )

#         if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data)

#         return Response(serializer.errors)

#     def delete(self, request, id):

#         student = students.objects.get(id=id)

#         student.delete()

#         return Response({
#         "message": "Student Deleted Successfully"
#     })
            


