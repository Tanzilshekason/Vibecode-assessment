# TaskFlow - Task Management System

TaskFlow is a comprehensive task and project management application built with Ruby on Rails. It helps teams organize projects, assign tasks, track progress, and collaborate effectively.

## Features

- **Project Management**: Create and manage projects with deadlines and progress tracking
- **Task Assignment**: Assign tasks to team members with priorities and due dates
- **Team Collaboration**: Organize teams and manage member permissions
- **Progress Tracking**: Visualize project progress with completion percentages
- **Reporting**: Generate reports on team performance and project status

## Tech Stack

- Ruby on Rails 4.2.0
- SQLite database
- Bootstrap for frontend (planned)
- Devise for authentication (planned)

## Getting Started

### Prerequisites
- Ruby 2.3+
- Bundler
- SQLite3

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Set up the database:
   ```bash
   rails db:setup
   rails db:migrate
   ```
4. Start the server:
   ```bash
   rails server
   ```
5. Visit `http://localhost:3000`

## Project Structure

- `app/controllers/` - Controllers for projects, tasks, teams, and users
- `app/models/` - Models for Project, Task, Team, User, and associations
- `app/services/` - Business logic services
- `app/views/` - View templates (ERB)
- `config/` - Application configuration

## API Endpoints

- `GET /projects` - List all projects
- `POST /projects` - Create a new project
- `GET /projects/:id` - Get project details
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /teams` - List all teams

## Development Notes

This repository is intentionally messy and contains a production-like project with various issues including security vulnerabilities, poor structure, duplicate logic, missing validation, no tests, and bugs in logic. The codebase serves as an exercise for developers to identify and fix these problems.

## License

MIT