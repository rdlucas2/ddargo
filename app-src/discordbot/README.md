
# discordbot

This repository contains a simple script posting a message to discord containerized using Docker - the intention being it'll be called as a k8s cronjob for the demo argo cluster setup. Below are instructions for building, testing, and scanning the application.

## Building and Uploading the Docker Image

To build the Docker image and upload it to DockerHub, follow these steps:

1. Build the Docker image:
   ```bash
   # Make a variable for your-dockerhub-username
   export DOCKERHUB_USERNAME="your-dockerhub-username"
   docker build -t $DOCKERHUB_USERNAME/discordbot:latest --target artifact .
   ```
   Replace `your-dockerhub-username` with your actual DockerHub username.

2. Log in to DockerHub:
   ```bash
   docker login
   ```
   Enter your DockerHub credentials when prompted.

3. Push the image to DockerHub:
   ```bash
   docker push $DOCKERHUB_USERNAME/discordbot:latest
   ```

4. To use the image, you can now pull it from DockerHub:
   ```bash
   docker pull $DOCKERHUB_USERNAME/discordbot:latest
   ```

## Running the Docker Image

To run the Docker image, use the following command:
```bash
docker run -it --rm -e DISCORD_WEBHOOK_URL='YOUR_URL_HERE' $DOCKERHUB_USERNAME/discordbot:latest
```

This command will start the container in interactive mode and remove it after it exits.

## Running the Tests

Build the test layer first:
```bash
docker build -t $DOCKERHUB_USERNAME/discordbot:test --target test .
```

To run the tests, use the following command:
```bash
docker run -it --rm -v $(pwd)/out:/app/out $DOCKERHUB_USERNAME/discordbot:test
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
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)/out:/out" aquasec/trivy image --format table --output /out/trivy-report.txt --scanners vuln $DOCKERHUB_USERNAME/discordbot:latest
```

This command will generate a vulnerability report and save it in the `out` folder as `trivy-report.txt`.

---

Follow these instructions to build, test, and scan your discordbot. If you encounter any issues, please consult the Docker, SonarQube, or Trivy documentation for additional guidance.
