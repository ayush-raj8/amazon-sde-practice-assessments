from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("cuisine", models.CharField(max_length=80)),
                (
                    "ingredients",
                    models.CharField(
                        help_text="Comma-separated ingredient list", max_length=500
                    ),
                ),
                (
                    "diet",
                    models.CharField(
                        choices=[
                            ("any", "Any"),
                            ("vegetarian", "Vegetarian"),
                            ("vegan", "Vegan"),
                        ],
                        default="any",
                        max_length=20,
                    ),
                ),
                ("cook_time_minutes", models.PositiveIntegerField()),
            ],
        ),
    ]
