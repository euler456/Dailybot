# Dailybot

Dailybot is a cloud-based automation bot that runs on Google Cloud Run. This project is designed to schedule and execute daily tasks at 5am, allowing for seamless task management and automation. The bot is built using Flask for the backend, and it integrates with Google Cloud services like Cloud Run, Cloud Scheduler, and Artifact Registry to deploy and manage the application.

## Technologies Used

- **Google Cloud Platform (GCP)**: Utilized Cloud Run for deploying the app in a serverless environment, Cloud Scheduler for automating daily execution, and Artifact Registry for managing Docker images.
- **Docker**: Used to containerize the application, making it portable and easy to deploy.
- **Flask**: The lightweight web framework used to develop the bot’s backend, which handles HTTP requests.
- **Python**: The main programming language for the bot's logic and integrations.

## Setup

1. **Build & push the Docker image**:
   ```sh
   docker build -t gcr.io/dailybot-project-455307/dailybot .
   docker push gcr.io/dailybot-project-455307/dailybot
