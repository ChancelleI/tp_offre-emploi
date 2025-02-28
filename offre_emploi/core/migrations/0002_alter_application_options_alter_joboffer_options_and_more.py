# Generated by Django 5.1.5 on 2025-02-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['-application_date']},
        ),
        migrations.AlterModelOptions(
            name='joboffer',
            options={'ordering': ['-published_at']},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='recommendation',
            options={'ordering': ['-recommendation_score']},
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('accepted', 'Acceptée'), ('rejected', 'Refusée')], db_index=True, default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='contract_type',
            field=models.CharField(choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('Freelance', 'Freelance'), ('Stage', 'Stage'), ('Alternance', 'Alternance')], db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='contact_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('job_seeker', "Chercheur d'emploi"), ('recruiter', 'Recruteur')], db_index=True, max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('job_offer', 'job_seeker')},
        ),
    ]
