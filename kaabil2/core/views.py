from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from .forms import SignUpForm, ProfileForm, ResumeUploadForm
from .models import Profile, Skill, StudentSkill, CareerRole, RequiredSkill, QuizQuestion, QuizAttempt, LearningTask, ResumeRecord, Job
from .scoring import calculate_role_fit, skill_gaps

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Welcome to KAABIL. Let's build your career plan.")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)
    skills = StudentSkill.objects.filter(user=request.user).select_related("skill")
    tasks = LearningTask.objects.filter(user=request.user)
    quiz_count = QuizAttempt.objects.filter(user=request.user).count()
    completed = tasks.filter(completed=True).count()
    total = tasks.count()
    readiness = round(sum(s.level for s in skills) / skills.count()) if skills.exists() else 0
    return render(request, "dashboard.html", {"profile": profile, "profile_form": form, "skills": skills,
        "tasks": tasks[:5], "quiz_count": quiz_count, "readiness": readiness,
        "completed": completed, "task_total": total})

def _role_results(user):
    student_levels = {x.skill_id: x.level for x in StudentSkill.objects.filter(user=user)}
    results = []
    for role in CareerRole.objects.prefetch_related("requiredskill_set__skill"):
        req = {r.skill_id: r.required_level for r in role.requiredskill_set.all()}
        results.append({"role": role, "fit": calculate_role_fit(req, student_levels),
                        "gaps": skill_gaps(req, student_levels)})
    return sorted(results, key=lambda x: x["fit"], reverse=True)

@login_required
def career_match(request):
    results = _role_results(request.user)
    return render(request, "career_match.html", {"results": results})

@login_required
def skill_gap(request):
    roles = CareerRole.objects.all()
    selected = request.GET.get("role")
    role = CareerRole.objects.filter(pk=selected).first() if selected else None
    if role is None and roles.exists():
        role = roles.first()
    rows = []
    if role:
        levels = {x.skill_id: x.level for x in StudentSkill.objects.filter(user=request.user)}
        for req in RequiredSkill.objects.filter(role=role).select_related("skill"):
            current = levels.get(req.skill_id, 0)
            rows.append({"skill": req.skill, "current": current, "required": req.required_level,
                         "gap": max(req.required_level-current, 0)})
    return render(request, "skill_gap.html", {"roles": roles, "selected_role": role, "rows": rows})

@login_required
def planner(request):
    if request.method == "POST":
        task = get_object_or_404(LearningTask, pk=request.POST.get("task_id"), user=request.user)
        task.completed = not task.completed
        task.save(update_fields=["completed"])
        return redirect("planner")
    tasks = LearningTask.objects.filter(user=request.user)
    return render(request, "planner.html", {"tasks": tasks})

@login_required
def quiz(request):
    questions = QuizQuestion.objects.filter(active=True).select_related("skill")[:5]
    return render(request, "quiz.html", {"questions": questions})

@login_required
def quiz_submit(request):
    if request.method != "POST":
        return redirect("quiz")
    results = []
    question_ids = [key for key in request.POST.keys() if key.isdigit()]
    for question in QuizQuestion.objects.filter(active=True, id__in=question_ids):
        selected = request.POST.get(str(question.id), "")
        if selected not in "ABCD":
            continue
        correct = selected == question.correct_option
        QuizAttempt.objects.create(user=request.user, question=question, selected_option=selected, is_correct=correct)
        results.append({"question": question, "correct": correct, "explanation": question.explanation})
    return render(request, "quiz_result.html", {"results": results, "score": sum(r["correct"] for r in results), "total": len(results)})

@login_required
def resume(request):
    form = ResumeUploadForm(request.POST or None, request.FILES or None)
    latest = ResumeRecord.objects.filter(user=request.user).first()
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        try:
            path = record.file.path
            if path.lower().endswith(".pdf"):
                import pdfplumber
                with pdfplumber.open(path) as pdf:
                    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            else:
                from docx import Document
                text = "\n".join(p.text for p in Document(path).paragraphs)
            record.extracted_text = text[:30000]
            keywords = ["python", "java", "sql", "communication", "project", "education", "experience", "html", "css", "javascript"]
            found = [k for k in keywords if k in text.lower()]
            record.estimated_score = min(100, round(len(found) / len(keywords) * 100))
            record.feedback = {"found_keywords": found, "missing_keywords": [k for k in keywords if k not in found],
                               "note": "This is a basic keyword coverage estimate, not an actual ATS vendor score."}
            record.save()
            messages.success(request, "Resume uploaded and analyzed.")
            return redirect("resume")
        except Exception:
            messages.error(request, "We could not read this file. Please try another valid PDF or DOCX.")
    return render(request, "resume.html", {"form": form, "latest": latest})

@login_required
def jobs(request):
    listings = Job.objects.filter(active=True)
    query = request.GET.get("q", "").strip()
    if query:
        listings = listings.filter(title__icontains=query) | listings.filter(company__icontains=query)
    return render(request, "jobs.html", {"jobs": listings.distinct()})
