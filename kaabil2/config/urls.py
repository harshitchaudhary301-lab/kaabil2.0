from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("career-match/", views.career_match, name="career_match"),
    path("skill-gap/", views.skill_gap, name="skill_gap"),
    path("planner/", views.planner, name="planner"),
    path("quiz/", views.quiz, name="quiz"),
    path("quiz/submit/", views.quiz_submit, name="quiz_submit"),
    path("resume/", views.resume, name="resume"),
    path("jobs/", views.jobs, name="jobs"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
