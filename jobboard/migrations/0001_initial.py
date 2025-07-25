# Generated by Django 5.1.7 on 2025-06-17 08:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('education', 'Education'), ('plumbing', 'Plumbing'), ('electrical', 'Electrical'), ('cleaning', 'Cleaning'), ('other', 'Other')], max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=50)),
                ('payment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_needed', models.DateField()),
                ('is_assigned', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_jobs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('expected_rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='applied', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobboard.jobpost')),
            ],
        ),
    ]
