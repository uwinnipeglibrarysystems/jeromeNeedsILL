# Generated by Django 3.2.4 on 2021-09-18 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('illrequest', '0005_illmanualrequester'),
    ]

    operations = [
        migrations.CreateModel(
            name='relaisrequestsmade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('barcode', models.CharField(max_length=255)),
                ('ip', models.CharField(max_length=60)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='illrequest.illrequestbase')),
            ],
        ),
    ]
