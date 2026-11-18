from django.conf import settings
from django.db import models

class Profile(models.Model):
    STREAMS = [("CSE", "Computer Science"), ("IT", "Information Technology"),
               ("ECE", "Electronics"), ("ME", "Mechanical"), ("OTHER", "Other")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stream = models.CharField(max_length=20, choices=STREAMS, blank=True)
    college = models.CharField(max_length=160, blank=True)
    target_role = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=40, default="Technical")
    def __str__(self): return self.name

class StudentSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skill_levels")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=0, help_text="Self-assessed level from 0 to 100")
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ("user", "skill")
    def __str__(self): return f"{self.user}: {self.skill} ({self.level})"

class CareerRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, through="RequiredSkill", related_name="career_roles")
    def __str__(self): return self.name

class RequiredSkill(models.Model):
    role = models.ForeignKey(CareerRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.PositiveSmallIntegerField(default=70)
    class Meta:
        unique_together = ("role", "skill")

class QuizQuestion(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=250)
    option_b = models.CharField(max_length=250)
    option_c = models.CharField(max_length=250)
    option_d = models.CharField(max_length=250)
    correct_option = models.CharField(max_length=1, choices=[(x, x) for x in "ABCD"])
    explanation = models.TextField(blank=True)
    active = models.BooleanField(default=True)

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

class LearningTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    resource_url = models.URLField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["completed", "due_date", "-created_at"]

class ResumeRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True)
    estimated_score = models.PositiveSmallIntegerField(default=0)
    feedback = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    title = models.CharField(max_length=160)
    company = models.CharField(max_length=160)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(Skill, blank=True)
    application_url = models.URLField(blank=True)
    is_demo = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.title} - {self.company}"
