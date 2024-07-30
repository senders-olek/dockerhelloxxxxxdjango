# Use an official Python 3.11 runtime as an image
FROM python:3.12.4-slim

# Create non-privileged user
RUN useradd -m -s /bin/bash appuser

# Set working directory in the container
WORKDIR /app

# Install modules while staging
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Install Infisical
RUN apt-get update && apt-get install -y bash curl && curl -1sLf \
'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | bash \
&& apt-get update && apt-get install -y infisical


# Change ownership of application files to non-privileged user
RUN chown -R appuser:appuser /app
USER appuser
RUN whoami

# Don't forget to cover this with IPTables or server firewall
EXPOSE 8000

# For a FastAPI project, modify the command to run on container start with the infisical command
CMD ["infisical", "run", "--projectId", "ae156cee-0d22-4b4e-8f15-52715efb7d75", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]