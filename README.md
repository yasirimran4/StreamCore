# Python Async OOP Movie App

This repository contains a simple command-line movie application implemented with asynchronous Python, object-oriented programming, and SQLite persistence. The project demonstrates a clean separation between business logic, data access, and user interaction while using asynchronous database operations.

## Overview

The application supports:
- user registration and login
- admin-only movie management (add, edit, delete)
- authenticated movie listing
- liking movies with an incremental like count
- watching movies with view tracking
- user watch history

The intent is to show a real-world OOP architecture using async patterns and a lightweight data layer.

## Architecture

The code is organized into the following layers:

- `cli/`: command-line interface and user interaction flow
- `database/`: database connection, schema creation, and persistence classes
- `models/`: domain models for `User` and `Movie`
- `services/`: application services for authentication and movie operations
- `decorators/`: authorization and authentication guards

### Key implementation details

- Async I/O with `asyncio` for CLI prompts and SQLite access
- `aiosqlite` for asynchronous database operations
- OOP encapsulation for models and service classes
- separation of concerns between presentation, service, and persistence
- database schema initialization at application startup
- role-based access control using decorators

## Installation

1. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install aiosqlite
```

3. Run the application:

```bash
python main.py
```

The SQLite database file is stored at `storage/movie_app.db` and is created automatically when the application starts.

## Usage

When the application runs, the CLI presents a menu for:
- registering a new user
- logging in
- viewing movies
- adding/editing/deleting movies as an admin
- liking a movie
- watching a movie
- viewing watch history
- logging out

A user must be authenticated before they can like, watch, or list movies. Only admin users can manage movie records.

## Project Details

### Authentication

User authentication is handled by `services/auth_service.py` and stored in SQLite through `database/user_data.py`. Login state is kept on the `User` model after successful authentication.

### Movie management

Movie operations are implemented in `services/movie_service.py` and persisted by `database/movie_data.py`. The application tracks:
- movie title
- like count
- view count
- history of watched movies

### Watch history

Watch history is stored in a dedicated `history` table. Each record links a user to a movie and includes a timestamp.

## File structure

- `main.py` — application entry point
- `cli/app.py` — interactive CLI implementation
- `database/connection.py` — async SQLite connection wrapper
- `database/schema.py` — table creation and schema setup
- `models/user.py` — user domain model
- `models/movie.py` — movie domain model
- `services/auth_service.py` — registration and login service
- `services/movie_service.py` — movie business logic service
- `decorators/auth_decorator.py` — authenticated access guard
- `decorators/admin_decorator.py` — admin authorization guard

## Recommended improvements

For a production-ready version, consider:
- password hashing and secure credential storage
- richer error handling and user feedback
- migration support for schema changes
- unit tests for service and persistence layers
- session management beyond in-memory login state

## Conclusion

This project is a small but complete example of building a CLI application with Python async patterns and SQLite persistence. It focuses on clean architectural boundaries and practical use of object-oriented design in a terminal-based workflow.
