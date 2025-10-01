# HbNB Services

This folder contains the business logic layer of the HBnB application.

## Structure

- The main component is the **Facade** class (`facade.py`), which provides a simplified interface for managing all business operations.
- The Facade interacts with the persistence layer (repositories) and models to create, retrieve, update, and delete entities.

## Key Features

- Implements validation and business rules beyond model-level checks.
- Ensures consistency when handling related entities, e.g., verifying that referenced users or places exist before creating a review or place.
- Abstracts and centralizes business logic to keep the API layer simple and clean.
- Supports all entities: User, Place, Amenity, and Review.
- Provides methods such as `create_user`, `update_place`, `delete_review`, etc.

## Usage

The API layer calls Facade methods to perform operations, which in turn manipulate the models and interact with the underlying repositories to persist data.



