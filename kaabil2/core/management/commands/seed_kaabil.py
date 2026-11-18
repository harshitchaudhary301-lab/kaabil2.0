from django.core.management.base import BaseCommand
from core.models import Skill, CareerRole, RequiredSkill, QuizQuestion, Job

DATA = {
 "Software Developer": ["Python", "Problem Solving", "Data Structures", "Git", "Communication"],
 "Data Analyst": ["Python", "SQL", "Excel", "Data Visualization", "Communication"],
 "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
 "AI/ML Engineer": ["Python", "Statistics", "Machine Learning", "Data Structures", "Git"],
 "Web Developer": ["HTML", "CSS", "JavaScript", "Python", "Git"],
 "UI/UX Designer": ["UI/UX Design", "Communication", "Problem Solving", "HTML", "CSS"],
 "Cybersecurity Analyst": ["Networking", "Linux", "Python", "Problem Solving", "Communication"],
 "Cloud Engineer": ["Linux", "Networking", "Python", "Git", "Problem Solving"],
 "Business Analyst": ["Excel", "SQL", "Communication", "Data Visualization", "Problem Solving"],
 "Digital Marketing Specialist": ["Communication", "Data Visualization", "SEO", "Excel", "Problem Solving"],
}
class Command(BaseCommand):
    help = "Load starter career roles, skills, sample quiz and clearly labelled demo jobs."
    def handle(self, *args, **options):
        skill_map = {}
        categories = {"Communication":"Soft Skill","Problem Solving":"Soft Skill","UI/UX Design":"Design"}
        for name in sorted({s for values in DATA.values() for s in values}):
            skill_map[name], _ = Skill.objects.get_or_create(name=name, defaults={"category": categories.get(name, "Technical")})
        for role_name, names in DATA.items():
            role, _ = CareerRole.objects.get_or_create(name=role_name, defaults={"description": f"Explore the skills and learning path for a {role_name} career."})
            for name in names:
                RequiredSkill.objects.get_or_create(role=role, skill=skill_map[name], defaults={"required_level": 70})
        q, created = QuizQuestion.objects.get_or_create(
            question="Which language is commonly used for data analysis?",
            defaults={"skill":skill_map["Python"],"option_a":"Python","option_b":"HTML","option_c":"CSS","option_d":"XML","correct_option":"A","explanation":"Python has widely used data analysis libraries such as pandas and NumPy."})
        Job.objects.get_or_create(title="Junior Data Analyst Intern", company="KAABIL Demo Listings",
            defaults={"location":"Remote / India","description":"Sample listing for demonstrating the KAABIL job interface. This is not a live vacancy.","is_demo":True})
        Job.objects.get_or_create(title="Frontend Developer Intern", company="KAABIL Demo Listings",
            defaults={"location":"Hybrid / India","description":"Sample listing for demonstrating the KAABIL job interface. This is not a live vacancy.","is_demo":True})
        self.stdout.write(self.style.SUCCESS("Starter data loaded. Demo jobs are clearly labelled."))
