from django.contrib import admin
from .models import LearnerApply,ChangePassword,LearningMaterial, FeeStructure
# Register your models here.
admin.site.register(LearnerApply)

@admin.register(ChangePassword)
class ChangePasswordAdmin(admin.ModelAdmin):
    list_display = ['user','timestamp']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['category','totalFee']


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title', 'description')    