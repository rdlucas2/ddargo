# Building and Uploading the Docker Image

To build the Docker image and upload it to DockerHub, follow these steps:

1. Build the Docker image:
   ```
   #make a variable for your-dockerhub-username
   export DOCKERHUB_USERNAME="your-dockerhub-username"
   docker build -t $DOCKERHUB_USERNAME/goapp1:latest --target artifact .
   ```
   Replace `your-dockerhub-username` with your actual DockerHub username.

2. Log in to DockerHub:
   ```
   docker login
   ```
   Enter your DockerHub credentials when prompted.

3. Push the image to DockerHub:
   ```
   docker push $DOCKERHUB_USERNAME/goapp1:latest
   ```

4. To use the image, you can now pull it from DockerHub:
   ```
   docker pull $DOCKERHUB_USERNAME/goapp1:latest
   ```

# Running the Docker Image

To run the Docker image, use the following command:
```
docker run -it --rm -p 8080:8080 $DOCKERHUB_USERNAME/goapp1:latest
```

This command will start the container in interactive mode and remove it after it exits.

# Running the Tests

Build the test layer first:
```
docker build -t $DOCKERHUB_USERNAME/goapp1:test --target test .
```

To run the tests, use the following command:
```
docker run -it --rm -v $(pwd)/out:/app/out -p 8080:8080 $DOCKERHUB_USERNAME/goapp1:test
```

This command will start the container in interactive mode and remove it after it exits.

# sonarqube scan

start sonarqube container
```
docker run -d --name sonarqube -p 9000:9000 sonarqube
```

get sonarqube token
```
# use post method for curl
curl -X POST -u admin:admin http://localhost:9000/api/user_tokens/generate?name=sonarqube-scanner
```

run sonarqube scanner
```
docker run -it --rm -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_TOKEN="YOUR_SONARQUBE_TOKEN" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
```
# trivy scan
```
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)/out:/out" aquasec/trivy image --format table --output /out/trivy-report.txt --scanners vuln $DOCKERHUB_USERNAME/goapp1:latest
```
