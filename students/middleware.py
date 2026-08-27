import time
from django.shortcuts import redirect
from django.urls import resolve

class Studmiddleware:

    def __init__(self,get_response):

        self.get_response=get_response

    def __call__(self,request):
        allowed_urls = [
            "/",
            "/login/",
            "/register/",
        ]

        if (
            not request.user.is_authenticated
            and request.path not in allowed_urls
                and not request.path.startswith("/admin/")
            and not request.path.startswith("/api/")

        ):
            return redirect("home")

        start = time.time()

        print(request.path)
        current_url = resolve(request.path_info).url_name
        print(current_url)
        response = self.get_response(request)

          
        end = time.time()

        print(end - start)

        return response