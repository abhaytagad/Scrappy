# Use a base image with Python
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt (make sure langdetect is in it)
RUN pip install --no-cache-dir -r requirements.txt

# Alternatively, if you don't have requirements.txt, you can install specific packages
# RUN pip install langdetect

# Add /app/python/bin to PATH
ENV PATH="/app/python/bin:${PATH}"

# Remove deprecated eggs or other invalid distributions (optional)
RUN rm -rf /app/__main__.egg

# Expose the port your app runs on (if applicable)
EXPOSE 8000

# Define the command to run your application
CMD ["python", "app.py"]  # or whatever your entrypoint script is
