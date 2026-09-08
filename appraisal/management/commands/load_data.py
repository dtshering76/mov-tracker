from django.core.management.base import BaseCommand
from appraisal.models import Standard, FocusArea, MOV

# Your data from the appraisal framework image
DATA = [
    ("Diversity of learners", [
        ("1.3", "Learners' gender, needs, interests and abilities."),
    ]),
    ("Learning environment", [
        ("2.1", "Safe and protective learning environment."),
        ("2.4", "Support for learner participation."),
    ]),
    ("Content and Pedagogical Knowledge", [
        ("3.1", "Content and Pedagogical Knowledge"),
        ("3.5", "Higher order thinking skills."),
        ("3.7", "Medium of instruction."),
    ]),
    ("Planning and Teaching", [
        ("4.2", "Teaching learning plans and processes."),
        ("4.3", "Teaching learning resources including ICT."),
    ]),
    ("Assessment and Reporting", [
        ("5.1", "Design and utilization of classroom assessment strategies."),
        ("5.2", "Monitoring and evaluation of learner progress and achievement."),
        ("5.5", "Use of assessment data to enhance teaching."),
    ]),
    ("Personal Growth and Professional Development", [
        ("6.3", "Professional reflection and learning."),
        ("6.5", "Professional networks with colleagues."),
    ]),
    ("Professional Engagement and Bhutanese Values", [
        ("7.1", "Engagement of parents and community."),
        ("7.3", "School policies and procedures."),
    ]),
]


class Command(BaseCommand):
    help = "Loads Standards and Focus Areas, with placeholder MOVs, into the database."

    def handle(self, *args, **options):
        for order, (standard_name, focus_areas) in enumerate(DATA, start=1):
            standard, _ = Standard.objects.get_or_create(
                name=standard_name, defaults={'order': order}
            )
            self.stdout.write(f"Standard: {standard_name}")

            for code, description in focus_areas:
                focus_area, _ = FocusArea.objects.get_or_create(
                    standard=standard, code=code, defaults={'description': description}
                )
                self.stdout.write(f"  Focus Area {code}: {description}")

                # Add 4 placeholder MOVs — rename these later in Django Admin
                for i in range(1, 5):
                    MOV.objects.get_or_create(
                        focus_area=focus_area,
                        title=f"MOV {i} for {code} (edit this title in Admin)"
                    )

        self.stdout.write(self.style.SUCCESS("Done! Data loaded successfully."))
        