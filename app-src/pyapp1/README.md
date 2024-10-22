
# pyapp1 - FastAPI Application

This repository contains a simple FastAPI application containerized using Docker. Below are instructions for building, testing, and scanning the application.

## Building and Uploading the Docker Image

To build the Docker image and upload it to DockerHub, follow these steps:

1. Build the Docker image:
   ```bash
   # Make a variable for your-dockerhub-username
   export DOCKERHUB_USERNAME="your-dockerhub-username"
   docker build -t $DOCKERHUB_USERNAME/pyapp1:latest --target artifact .
   ```
   Replace `your-dockerhub-username` with your actual DockerHub username.

2. Log in to DockerHub:
   ```bash
   docker login
   ```
   Enter your DockerHub credentials when prompted.

3. Push the image to DockerHub:
   ```bash
   docker push $DOCKERHUB_USERNAME/pyapp1:latest
   ```

4. To use the image, you can now pull it from DockerHub:
   ```bash
   docker pull $DOCKERHUB_USERNAME/pyapp1:latest
   ```

## Running the Docker Image

To run the Docker image, use the following command:
```bash
docker run -it --rm -p 8000:8000 $DOCKERHUB_USERNAME/pyapp1:latest
```

This command will start the container in interactive mode and remove it after it exits. Add --entrypoint /bin/sh to explore the container.

## Running the Tests

Build the test layer first:
```bash
docker build -t $DOCKERHUB_USERNAME/pyapp1:test --target test .
```

To run the tests, use the following command:
```bash
docker run -it --rm -v $(pwd)/out:/app/out -p 8000:8000 $DOCKERHUB_USERNAME/pyapp1:test
```

This command will start the container in interactive mode and remove it after it exits, with test outputs available in the `out` folder.

## SonarQube Scan

Start the SonarQube container:
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube
```

Generate a SonarQube token:
```bash
# Use a POST method for curl
curl -X POST -u admin:admin http://localhost:9000/api/user_tokens/generate?name=sonarqube-scanner
```

Run SonarQube scanner:
```bash
docker run -it --rm -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_TOKEN="YOUR_SONARQUBE_TOKEN" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
```
Replace `YOUR_SONARQUBE_TOKEN` with the token generated in the previous step.

## Trivy Scan

Run Trivy security scan to check for vulnerabilities:
```bash
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)/out:/out" aquasec/trivy image --format table --output /out/trivy-report.txt --scanners vuln $DOCKERHUB_USERNAME/pyapp1:latest
```

This command will generate a vulnerability report and save it in the `out` folder as `trivy-report.txt`.

---

Follow these instructions to build, test, and scan your FastAPI application effectively. If you encounter any issues, please consult the Docker, SonarQube, or Trivy documentation for additional guidance.
