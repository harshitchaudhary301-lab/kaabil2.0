from django.contrib import admin
from .models import Profile, Skill, StudentSkill, CareerRole, RequiredSkill, QuizQuestion, QuizAttempt, LearningTask, ResumeRecord, Job

admin.site.register([Profile, Skill, StudentSkill, CareerRole, RequiredSkill, QuizQuestion, QuizAttempt, LearningTask, ResumeRecord, Job])
