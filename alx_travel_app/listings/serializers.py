# listings/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Listing, Booking, Review

User = get_user_model()

class ListingSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source="host.username")
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "address", "city", "country",
            "price_per_night", "max_guests", "host", "average_rating",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "host", "created_at", "updated_at", "average_rating"]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 2)


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Booking
        fields = [
            "id", "listing", "user", "start_date", "end_date",
            "guests", "total_price", "status", "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def validate(self, data):
        """
        Ensure end_date > start_date and guest count ≤ listing.max_guests.
        Also compute a simple total_price if not provided (optional).
        """
        start = data.get("start_date")
        end = data.get("end_date")
        listing = data.get("listing")

        if start and end and end <= start:
            raise serializers.ValidationError("end_date must be after start_date")

        guests = data.get("guests", 1)
        if listing and guests > listing.max_guests:
            raise serializers.ValidationError("guest count exceeds maximum for this listing")

        return data

    def create(self, validated_data):
        # Optionally compute total_price if not provided: nights * price_per_night
        total_price = validated_data.get("total_price")
        if total_price is None:
            nights = (validated_data["end_date"] - validated_data["start_date"]).days
            validated_data["total_price"] = nights * validated_data["listing"].price_per_night
        # user should be set by the view; if not available, leave it.
        return super().create(validated_data)
