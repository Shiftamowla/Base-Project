# Generated by Django 5.1.2 on 2024-10-20 04:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipePostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RecipeTitle', models.CharField(max_length=500, null=True)),
                ('Nutritional_Info', models.CharField(max_length=500, null=True)),
                ('Ingredients', models.CharField(max_length=1000, null=True)),
                ('Instructor', models.CharField(max_length=1000, null=True)),
                ('Category', models.CharField(choices=[('breakfast', 'breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], max_length=100, null=True)),
                ('Tag', models.CharField(choices=[('vegetarian', 'Vegetarian'), ('non-vegetarian', 'Non-Vegetarian')], max_length=100, null=True)),
                ('DifficultyLevel', models.CharField(choices=[('high', 'high'), ('medium', 'Medium'), ('low', 'Low')], max_length=100, null=True)),
                ('Image', models.ImageField(null=True, upload_to='Media/Blog_Pic')),
                ('PreparetionTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('CookingTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('TotalTime', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]