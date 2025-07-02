cd backend
pip install requirements -r requirements.txt

test running the app: fastapi run main.py

create the docker image: docker build -t fastapi-app .

run the docker image: docker run -p 8000:8000 fastapi-app
this should open a browser and you should be able to hit your endpoints

# Deploy Azure resources
## Web App
Create a basic web app with the container deployment and linux OS

## Container registry
Create the registry with no special settings

# Settings
## Web App
Change the configuration for SCM Basic Auth Publishing to On
Change the identity to On (creating a system assigned identity)

## Container Registry
IAM (Access Control) create a role for the system assigned identity created for the web app. ACR Pull as the role. Members -> Managed Identity -> App Service and find the managed identity for the app you just created.

# Build image and deploy to registry
az login --tenant ed9aa516-5358-4016-a8b2-b6ccb99142d0
az acr login --name <CONTAINER_REGISTRY_RESOURCE_NAME>

Tag the image: docker tag fastapi-app scherbringfastapi.azurecr.io/fastapi-app

Push the image to the container registry: docker push scherbringfastapi.azurecr.io/fastapi-app

You should be able to see the container in your container registry now

# Deploy the container to your web app
Deployment center, click the container name (there should be a default container name from the quickstart that was deployed). Then change the source to an Azure Container Registry and the registry you deployed. Authentication = managed identity. Identity = system assigned. Image = the name of the image from the container registry (this is manually entered when you have a system identity). Image tag (latest) or whatever you used when creating the image.

BE SURE TO CHANGE THE PORT TO 8000 OR WHATEVER YOU USE WITH THE DOCKER IMAGE. THE DEFAULT PORT OF 80 DOESN'T WORK WITH CODESPACES, SO WE CHANGE IT TO WORK LOCALLY AND NEED TO CHANGE OUR DEPLOYMENT TO EXPECT THE SAME