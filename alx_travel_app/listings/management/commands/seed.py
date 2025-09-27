# listings/management/commands/seed.py
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from django.db import transaction

User = get_user_model()

SAMPLE_TITLES = [
    "Cozy downtown studio",
    "Sunny room near the beach",
    "Quiet countryside cabin",
    "Modern apartment with balcony",
    "Rustic cottage with garden",
    "Luxury penthouse suite",
    "Budget private room",
    "Spacious family home",
    "Historic flat in old town",
    "Mountain-view chalet",
]

CITIES = [
    ("Lagos", "NG"),
    ("Accra", "GH"),
    ("Nairobi", "KE"),
    ("Cairo", "EG"),
    ("Cape Town", "ZA"),
    ("Kigali", "RW"),
    ("Kampala", "UG"),
    ("Dakar", "SN"),
    ("Casablanca", "MA"),
    ("Tunis", "TN"),
]

LOREM = (
    "A comfortable place to stay with quick access to local attractions. "
    "Well suited for both business and leisure travelers."
)

class Command(BaseCommand):
    help = "Seed the database with sample listings (and optionally bookings/reviews)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--listings", type=int, default=10, help="Number of listings to create"
        )
        parser.add_argument(
            "--force", action="store_true", help="Delete existing sample listings first"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["listings"]
        force = options["force"]

        # Create a host user
        host_username = "seed_host"
        host, created = User.objects.get_or_create(
            username=host_username,
            defaults={"email": "seed_host@example.com", "is_staff": False},
        )
        if created:
            host.set_password("password123")
            host.save()
            self.stdout.write(self.style.SUCCESS(f"Created host user: {host_username}"))

        if force:
            removed = Listing.objects.filter(host=host).delete()
            self.stdout.write(self.style.WARNING("Deleted existing sample listings."))

        created_count = 0
        for i in range(count):
            title = SAMPLE_TITLES[i % len(SAMPLE_TITLES)]
            city, country = CITIES[i % len(CITIES)]
            price = Decimal(random.choice([20, 30, 45, 60, 80, 120, 200]))
            max_guests = random.choice([1, 2, 3, 4, 6])

            listing = Listing.objects.create(
                host=host,
                title=f"{title} #{i+1}",
                description=LOREM,
                city=city,
                country=country,
                price_per_night=price,
                max_guests=max_guests,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} listings (host={host_username})."))
