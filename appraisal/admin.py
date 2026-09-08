from django.contrib import admin
from .models import Standard, FocusArea, MOV, AppraisalPeriod, Submission


class FocusAreaInline(admin.TabularInline):
    """Lets us add Focus Areas directly inside the Standard page."""
    model = FocusArea
    extra = 1  # show 1 empty extra row by default


class MOVInline(admin.TabularInline):
    """Lets us add MOVs directly inside the Focus Area page."""
    model = MOV
    extra = 1


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    inlines = [FocusAreaInline]


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'standard')
    inlines = [MOVInline]


@admin.register(MOV)
class MOVAdmin(admin.ModelAdmin):
    list_display = ('title', 'focus_area')


@admin.register(AppraisalPeriod)
class AppraisalPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'mov', 'period', 'status', 'submitted_at')
    list_filter = ('status', 'period')
    list_editable = ('status',)  # lets you approve/reject right from the list view