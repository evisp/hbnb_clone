
# HbNB Models

This folder contains the core business models used by the HBnB application.

## Structure

- Each Python module defines one or more models representing application entities:
  - `user.py` — User model with attributes like first name, last name, and email.
  - `place.py` — Place model including relationships to owner and amenities.
  - `amenity.py` — Amenity model describing features available at places.
  - `review.py` — Review model connecting user reviews with places.

## Key Features

- Models include data validation using property setters to enforce:
  - Non-empty strings where required.
  - Valid numeric ranges for latitude, longitude, price.
  - Valid email format for users.
- Models handle entity relationships explicitly:
  - Places connect to owners (`User`) and amenities.
  - Reviews link users to places.
- Models serve as the foundation for all business and persistence logic.

## Usage

Models are instantiated and managed by the service (facade) layer and are passed between layers to ensure consistent data integrity and validation.

