# HBnB Project

This project implements a backend API for the HBnB application, managing users, places, amenities, and reviews.

## Overview

The HBnB API provides RESTful endpoints to create, read, update, and (where applicable) delete entities such as users, places, amenities, and reviews. It is built with Python Flask and Flask-RESTx, using a service-oriented architecture with clear separation between API, business logic, and data models.

## Project Structure

```
app/              # Main application code
├── api/          # API endpoints organized by entity and version
├── models/       # Business models with validation and relationships
├── services/     # Business logic and facade layer
├── persistence/  # Data repositories (in-memory storage)
tests/            # Automated tests for API endpoints and logic
config.py         # Application configuration
run.py            # Application entry point
README.md         # You are here: project overview and navigation
```

## Getting Started

1. Create and activate a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run the application with:
   ```bash
   python3 run.py
   ```
4. Access the Swagger API documentation at: `http://127.0.0.1:5000/api/v1/`

## Folder Documentation

- [app/ README](app/README.md) – Details about application structure and components.
- [app/api/ README](app/api/README.md) – API endpoint structure and namespaces.
- [app/models/ README](app/models/README.md) – Models description and validation rules.
- [app/services/ README](app/services/README.md) – Business logic and facade pattern usage.
- [tests/ README](tests/README.md) – Testing strategy and how to run tests.

## Testing

Testing is done via automated unit tests using unittest/pytest and manual tests using cURL and Swagger UI.

