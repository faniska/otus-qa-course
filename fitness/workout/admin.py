from django.contrib import admin

from .models import Category, MuscleGroup, Muscle, Exercise, ExerciseStress

admin.site.register(Category)
admin.site.register(MuscleGroup)
admin.site.register(Muscle)
admin.site.register(Exercise)
admin.site.register(ExerciseStress)
