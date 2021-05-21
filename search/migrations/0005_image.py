# Generated by Django 3.2.3 on 2021-05-20 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20210520_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=200)),
                ('laboratory_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upload_images', to='search.laboratoryinfo')),
            ],
        ),
    ]