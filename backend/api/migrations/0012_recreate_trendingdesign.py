from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_trendingdesign_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TrendingDesign',
        ),
        migrations.CreateModel(
            name='TrendingDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the trending design', max_length=100)),
                ('tagline', models.CharField(blank=True, help_text='Tagline or short description', max_length=255)),
                ('image', models.ImageField(help_text='Upload high-quality image for the trending blueprints display', upload_to='trending/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, help_text='Price to display (blank to hide)', max_digits=10, null=True)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, help_text='Original price to show strike-through (optional)', max_digits=10, null=True)),
                ('product_id', models.IntegerField(blank=True, help_text='ID of the product to customize when clicked (e.g. 1 for T-Shirt, 4 for Mug)', null=True)),
                ('sort_order', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Trending Design',
                'verbose_name_plural': 'Trending Designs',
                'ordering': ['sort_order', '-created_at'],
            },
        ),
    ]
