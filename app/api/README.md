# HbNB API

This folder contains the API layer of the HBnB application.

## Structure

- Organized by API versions, currently only `v1/` is implemented.
- Each version folder (e.g., `v1/`) contains modules for different entities:
  - `users.py` — User endpoints
  - `amenities.py` — Amenity endpoints
  - `places.py` — Place endpoints
  - `reviews.py` — Review endpoints

## Key Features

- Uses Flask-RESTx for defining namespaces, routes, models for validation, and automatic Swagger API documentation.
- Each entity module defines RESTful endpoints supporting creating, retrieving, updating (and deleting for reviews) resources.
- Input validation models enforce required fields and data types.
- Endpoints support:
  - `POST` to create
  - `GET` for list and single resource retrieval
  - `PUT` to update (full update with all required fields)
  - `DELETE` (only supported for reviews)

## API Documentation

Swagger UI is auto-generated and accessible at `/api/v1/` when the application is running.


