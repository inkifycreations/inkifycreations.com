from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_trendingdesign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trendingdesign',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='trending_designs',
                to='api.product'
            ),
        ),
    ]
