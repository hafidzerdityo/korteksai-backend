# Backend Template FastAPI

A really simple backend template built with FastAPI, designed to jumpstart your backend development with ease. It's packed with essential features, including authentication using JSON Web Tokens (JWT), user management, and a containerized PostgreSQL database. The entire stack is containerized with Docker, simplifying deployment.

## Key Features

- **FastAPI**: Harness the power of FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

- **SQLAlchemy ORM**: Utilize SQLAlchemy as the ORM to interact with the PostgreSQL database, enabling efficient database operations and data modeling.

- **Async Capabilities**: Leverage asynchronous programming to handle concurrent operations efficiently, making your application responsive.

- **Authentication**: Secure your APIs with JSON Web Tokens (JWT) to ensure robust user authentication and authorization.

- **User Management**: Easily manage user accounts, including registration, login, and profile management.

- **Database**: Utilize a containerized PostgreSQL database to store your application's data, ensuring data integrity and scalability.

- **Dockerized**: Simplify deployment with Docker and Docker Compose. Run `docker-compose up`, and your entire application stack is up and running.

## Getting Started

1. Clone this repository.

2. Inside the `app` folder, create the following `.env` files for configuration:

   - Create `auth.env` (For JWT secret key):

     ```plaintext
     JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
     ```

   - Create `service.env` (For Service config):

     ```plaintext
     SERVICE_PORT=8004
     SERVICE_HOST=0.0.0.0
     SERVICE_WORKERS=4
     ```

   - Create `config.env` (For Database config):
     ```plaintext
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=default15p
     POSTGRES_HOST=postgres_rest_template
     POSTGRES_PORT=8003
     POSTGRES_DB=rest_template
     ```

   Feel free to change the values in the `.env` files based on your needs.

3. On the root directory, run the following command to start the development server along with the database. Make sure you have docker installed:
   ```bash
   docker-compose up
   ```
