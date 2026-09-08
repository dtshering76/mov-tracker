from django.db import models
from django.contrib.auth.models import User


class Standard(models.Model):
    """e.g. 'Diversity of learners' """
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)  # controls display order

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class FocusArea(models.Model):
    """e.g. '1.3 Learners' gender, needs, interests and abilities' """
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='focus_areas')
    code = models.CharField(max_length=10)          # e.g. "1.3"
    description = models.CharField(max_length=300)  # e.g. "Learners' gender, needs..."

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} {self.description}"


class MOV(models.Model):
    """A single required piece of evidence under a Focus Area."""
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='movs')
    title = models.CharField(max_length=300)  # e.g. "Sample differentiated lesson plan"

    def __str__(self):
        return self.title


class AppraisalPeriod(models.Model):
    """e.g. '2026 Mid-Year Appraisal' """
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    """A teacher's uploaded evidence file for one MOV, in one period."""

    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    mov = models.ForeignKey(MOV, on_delete=models.CASCADE, related_name='submissions')
    period = models.ForeignKey(AppraisalPeriod, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/%Y/%m/')
    remarks = models.CharField(max_length=300, blank=True)  # teacher's optional note
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # a teacher can only submit ONE file per MOV per period
        unique_together = ('teacher', 'mov', 'period')

    def __str__(self):
        return f"{self.teacher.username} - {self.mov.title} ({self.period.name})"