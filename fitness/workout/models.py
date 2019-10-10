from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Muscle Groups'

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Muscles'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=128)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    muscles = models.ManyToManyField(Muscle)

    class Meta:
        verbose_name_plural = 'Exercises'

    def __str__(self):
        return self.name


class ExerciseStress(models.Model):
    exercise = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT, related_name='+')
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT, related_name='+')
    value = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Exercise Stress'
        verbose_name_plural = 'Exercise Stresses'

    def __str__(self):
        return self.name
