# -*- coding: utf-8 -*-
"""
Management command: seed_designs
Usage: python manage.py seed_designs

Copies all PNG images from the project's assets/mug_designs/ folder
into the Django media directory and creates ProductDesign records for each.
Run once after the first migration to pre-populate mug designs.
"""
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from api.models import ProductDesign


# Map filename prefix → category slug
CATEGORY_MAP = {
    'birthday':  'birthday',
    'love':      'love',
    'family':    'family',
    'friends':   'friends',
    'cats':      'cats',
    'general':   'general',
}


def pretty_name(stem: str) -> str:
    """Convert a filename stem like 'birthday_happy_birthday_with_phtots' → 'Happy Birthday With Photos'."""
    # Remove the category prefix (first word before underscore)
    parts = stem.split('_')
    if len(parts) > 1:
        parts = parts[1:]
    name = ' '.join(parts).replace('-', ' ').title()
    return name + ' Mug'


class Command(BaseCommand):
    help = 'Seeds ProductDesign records from assets/mug_designs/ PNG files.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing mug designs before seeding.',
        )

    def handle(self, *args, **options):
        # Locate assets folder (two levels up from backend/)
        assets_dir = settings.BASE_DIR.parent / 'assets' / 'mug_designs'
        if not assets_dir.exists():
            self.stderr.write(self.style.ERROR(f'Assets folder not found: {assets_dir}'))
            return

        if options['clear']:
            deleted, _ = ProductDesign.objects.filter(product_type='mug').delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted} existing mug designs.'))

        png_files = sorted(assets_dir.glob('*.png'))
        if not png_files:
            self.stderr.write(self.style.ERROR('No PNG files found in mug_designs/.'))
            return

        created = 0
        skipped = 0

        for png_path in png_files:
            stem = png_path.stem  # e.g. 'birthday_birthday'

            # Determine category from prefix
            prefix = stem.split('_')[0]
            category = CATEGORY_MAP.get(prefix, 'general')

            # Build a human-readable name
            name = pretty_name(stem)

            # Skip if already exists (by name + product_type)
            if ProductDesign.objects.filter(product_type='mug', name=name).exists():
                skipped += 1
                continue

            # Create the design and attach the image file
            design = ProductDesign(
                product_type='mug',
                name=name,
                category=category,
                description=f'Premium ceramic mug design — {name}. High-gloss wrap print.',
                price=219,
                original_price=299,
                sort_order=created,
                is_active=True,
            )
            with open(png_path, 'rb') as f:
                design.image.save(png_path.name, File(f), save=True)

            created += 1
            self.stdout.write(f'  Created: {name} [{category}]')

        self.stdout.write(
            self.style.SUCCESS(f'\nDone! Created {created} designs, skipped {skipped} duplicates.')
        )
