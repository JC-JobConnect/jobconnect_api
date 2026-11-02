
from django.db import migrations, models
import django.db.models.deletion


def connect_jobs_to_companies(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Company = apps.get_model('jobs', 'Company')

    database = schema_editor.connection.alias

    for job in Job.objects.using(database).all().iterator():
        company_name = (job.company or '').strip()

        if not company_name:
            company_name = 'Unknown Company'

        company, created = Company.objects.using(database).get_or_create(
            name=company_name,
            defaults={'location': 'Unknown'}
        )

        job.company_new_id = company.id
        job.save(using=database, update_fields=['company_new'])


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_company'),
    ]

    operations = [
        # 1. Create a temporary ForeignKey column.
        migrations.AddField(
            model_name='job',
            name='company_new',
            field=models.ForeignKey(
                to='jobs.company',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='jobs',
                null=True,
                blank=True,
            ),
        ),

        # 2. Match existing company names with Company records.
        migrations.RunPython(
            connect_jobs_to_companies,
            migrations.RunPython.noop,
        ),

        # 3. Remove the old text field.
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),

        # 4. Rename the new ForeignKey to company.
        migrations.RenameField(
            model_name='job',
            old_name='company_new',
            new_name='company',
        ),

        # 5. Make the ForeignKey required.
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(
                to='jobs.company',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='jobs',
            ),
        ),
    ]
