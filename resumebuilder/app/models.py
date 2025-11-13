from django.db import models

# Create your models here.
class Resume(models.Model):
    job_choices = [
        ("se", "Software Engineer"),
        ("sde", "Software Developer"),
        ("fullstack", "Full stack developer"),
        ("pydev", "Python developer"),
        ("reactdev", "React developer"),
        ("mernstack", "Mern stack"),
        ("qa", "QA Roles")
    ]
    name = models.CharField(max_length=30)
    job_title = models.CharField(max_length=10, choices=job_choices)
    p_sumary = models.TextField(max_length=300)
    skills = models.CharField(max_length=200)
    resume = models.FileField(upload_to="uploads/",blank=True)

    def __str__(self):
        return self.name