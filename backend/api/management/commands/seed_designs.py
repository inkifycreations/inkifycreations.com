# -*- coding: utf-8 -*-
"""
Management command: seed_designs
Usage: python manage.py seed_designs

Scans backend/media/designs/ for PNG images and creates ProductDesign records.
Automatically determines product type (mug, tshirt, polo, bottle) from filename prefix.
"""
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from api.models import ProductDesign


# Map filename keywords to product types and categories
PRODUCT_TYPE_MAP = {
    'mug_': 'mug',
    'tshirt_': 'tshirt',
    'polo_': 'polo',
    'bottle_': 'bottle',
}

CATEGORY_MAP = {
    'birthday': 'birthday',
    'love': 'love',
    'family': 'family',
    'friends': 'friends',
    'cat': 'cats',
    'mother': 'family',
    'father': 'family',
    'wedding': 'love',
    'anniversary': 'love',
    'motivat': 'motivational',
    'dad': 'family',
    'mom': 'family',
    'best': 'friends',
}


def extract_category(filename: str) -> str:
    """Extract category from filename."""
    name_lower = filename.lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in name_lower:
            return category
    return 'general'


def extract_product_type(filename: str) -> str:
    """Extract product type from filename prefix."""
    name_lower = filename.lower()
    for prefix, ptype in PRODUCT_TYPE_MAP.items():
        if name_lower.startswith(prefix):
            return ptype
    return 'mug'  # Default to mug


def pretty_name(stem: str) -> str:
    """Convert filename to human-readable name."""
    # Remove product type prefix if present
    for prefix in ['mug_', 'tshirt_', 'polo_', 'bottle_']:
        if stem.lower().startswith(prefix):
            stem = stem[len(prefix):]
            break
    
    # Convert to title case
    name = stem.replace('_', ' ').replace('-', ' ').title()
    return name


class Command(BaseCommand):
    help = 'Seeds ProductDesign records from backend/media/designs/ PNG files.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing designs before seeding.',
        )

    def handle(self, *args, **options):
        # Use the Django MEDIA_ROOT to locate designs
        designs_dir = Path(settings.MEDIA_ROOT) / 'designs'
        
        if not designs_dir.exists():
            self.stderr.write(self.style.ERROR(f'Designs folder not found: {designs_dir}'))
            return

        if options['clear']:
            deleted, _ = ProductDesign.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted} existing designs.'))

        png_files = sorted(designs_dir.glob('*.png'))
        if not png_files:
            self.stderr.write(self.style.ERROR('No PNG files found in media/designs/.'))
            return

        created = 0
        skipped = 0

        for png_path in png_files:
            stem = png_path.stem
            product_type = extract_product_type(stem)
            category = extract_category(stem)
            name = pretty_name(stem)

            # Skip if already exists
            if ProductDesign.objects.filter(product_type=product_type, name=name).exists():
                skipped += 1
                continue

            # Create the design
            design = ProductDesign(
                product_type=product_type,
                name=name,
                category=category,
                description=f'Beautiful {category} design for {product_type}.',
                price=239 if product_type == 'mug' else (349 if product_type == 'tshirt' else (599 if product_type == 'polo' else 299)),
                original_price=299 if product_type == 'mug' else (499 if product_type == 'tshirt' else (799 if product_type == 'polo' else 399)),
                sort_order=created,
                is_active=True,
            )
            
            with open(png_path, 'rb') as f:
                design.image.save(png_path.name, File(f), save=True)

            created += 1
            self.stdout.write(f'  Created: {name} [{product_type}/{category}]')

        self.stdout.write(
            self.style.SUCCESS(f'\nDone! Created {created} designs, skipped {skipped} duplicates.')
        )
