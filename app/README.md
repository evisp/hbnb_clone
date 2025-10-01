# HBnB App 

This folder contains the main application source code for the HBnB API.

## Structure

- `api/`  
  Contains the API endpoint definitions, organized by entity (users, places, amenities, reviews) and version (v1). Each entity has its own namespace with routes and models for input validation and documentation.

- `models/`  
  Defines the core business models representing the data entities of the application (User, Place, Amenity, Review). Models include data validation and relationships.

- `services/`  
  Implements the business logic layer with a Facade pattern. The facade provides methods to create, retrieve, update, and delete entities, abstracting the interaction between API and repositories.

- `persistence/`  
  Contains data repository implementations. Currently, stores data in-memory using repositories for each entity.

## Key Points

- The application follows a layered architecture: API Layer → Service (Facade) Layer → Persistence Layer → Models.
- Input validation and error handling are implemented mainly via models and API layer using Flask-RESTx.
- The `services/facade.py` file provides a single entry point to perform business operations on all entities.
- In-memory persistence enables easy testing and prototyping; it can be replaced with a database later.

## Running the Application

The app folder is imported and used within the Flask application defined in `run.py`. The API endpoints become accessible once the app is running.

