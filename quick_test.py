from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

print("=== Complete Integration Test ===\n")

# Create users
owner = User("Alice", "Smith", "alice@example.com", is_admin=True)
guest1 = User("Bob", "Jones", "bob@example.com")
guest2 = User("Charlie", "Brown", "charlie@example.com")

print(f"✅ Created 3 users")
print(f"   - {owner.first_name} (Admin: {owner.is_admin})")
print(f"   - {guest1.first_name}")
print(f"   - {guest2.first_name}\n")

# Create amenities
wifi = Amenity("Wi-Fi")
parking = Amenity("Parking")
pool = Amenity("Swimming Pool")
gym = Amenity("Gym")

print(f"✅ Created 4 amenities\n")

# Create place
place = Place(
    title="Luxury Beach House",
    description="Beautiful beach house with ocean view",
    price=250.0,
    latitude=34.0522,
    longitude=-118.2437,
    owner=owner
)

# Add amenities to place
place.add_amenity(wifi)
place.add_amenity(parking)
place.add_amenity(pool)
place.add_amenity(gym)

print(f"✅ Created place: {place.title}")
print(f"   Owner: {place.owner.first_name} {place.owner.last_name}")
print(f"   Price: ${place.price}/night")
print(f"   Amenities: {len(place.amenities)}\n")

# Create reviews
review1 = Review(
    text="Absolutely amazing! The view was breathtaking.",
    rating=5,
    place=place,
    user=guest1
)
place.add_review(review1)

review2 = Review(
    text="Great place, but a bit pricey.",
    rating=4,
    place=place,
    user=guest2
)
place.add_review(review2)

print(f"✅ Added {len(place.reviews)} reviews")
for i, review in enumerate(place.reviews, 1):
    print(f"   {i}. {review.rating}/5 by {review.user.first_name}: '{review.text[:40]}...'")
print()

# Calculate average rating
avg_rating = sum(r.rating for r in place.reviews) / len(place.reviews)
print(f"✅ Average rating: {avg_rating:.1f}/5\n")

# Display complete place information
print("=== Complete Place Details ===")
print(f"Title: {place.title}")
print(f"Description: {place.description}")
print(f"Price: ${place.price}/night")
print(f"Location: ({place.latitude}, {place.longitude})")
print(f"Owner: {place.owner.first_name} {place.owner.last_name} ({place.owner.email})")
print(f"Amenities:")
for amenity in place.amenities:
    print(f"  - {amenity.name}")
print(f"Reviews: {len(place.reviews)}")
for review in place.reviews:
    print(f"  - {review.rating}/5 by {review.user.first_name}: {review.text}")
print()

print("=== Integration Test Complete ===")
