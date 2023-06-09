# Generated by Django 4.2 on 2023-04-10 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_newsarticle_userprofile_delete_news'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsarticle',
            old_name='date_created',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='finished_list',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='to_read_list',
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='user',
            field=models.ForeignKey(default=-1234, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
