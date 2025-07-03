# fastApi-React
The purpose of the repository is to provide a base template for fullstack web development, featuring a frontend built with React and a backend powered by FastAPI.

# Clone the Repo
Clone the repo to bring it into your own environment.
```
git clone https://github.com/jscherb1/fastApi-React.git
```

# Development Environment

## Coding Environment

It is recommended to use GitHub Codespaces as your coding environment. Codespaces come pre-installed with tools such as Docker and Git.

> **Note:** This setup has not been tested for local environments! Local installation requirements may vary.

## Recommended Extensions

- Copilot
- Python

# Local Development
## Set environment variables
Use the .env.example files for reference to create a .env file and set the appropriate variables.

## Run the Docker container
From a terminal, run:
```bash
docker-compose up
```
This will build and run the two docker container images: frontend and backend.

## Port Forwarding
⚠️**Important:** After running the docker images, be sure to change the backend port (by default port 8000) to Public visibility. Without this change, your front end container can not communicate with the backend container. ⚠️

# Deployment
The assumption is that you're deploying your application to Azure using containers and app services.

## Pre-requisites
To install the Azure CLI, run:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
This is required to perform Azure operations from the command line.

## Deploying Cloud Resources

### Required Resources
- Azure Container Services: 
- Web App (Front End)
- Web App (Back End)

### Steps
1. Create a resource group
2. Deploy a Azure Container Services resource
3. Deploy a Web App (frontend)
    - Create a basic web app with the container deployment and linux OS. Choose a quickstart container.  This will be changed later.
4. Deploy a Web App (backend)
    - Create a basic web app with the container deployment and linux OS. Choose a quickstart container.  This will be changed later.

5. Configure Resources

    Web App (Both frontend and backend):
    - Change the configuration for SCM Basic Auth Publishing to On
    - Change the identity to On (creating a system assigned identity)
    - Create and set environment variables for your application

    Container Registry:
    - IAM (Access Control) create a role for the system assigned identity created for the web app. ACR Pull as the role. Members -> Managed Identity -> App Service and find the managed identity for the app you just created.

6. Push containers to the registry
    - Use the manual or automated process to build and push the containers to the registry. This is a pre-requisite to have images in the registry so you can configure you applications to use the images.
7. Connect the Web App to the proper container (both Web App resources)
    - Click Ops:
        - From the Deployment center in each web app resource, click the container name (there should be a default container name from the quickstart that was deployed). Then change the source to an Azure Container Registry and the registry you deployed. Authentication = managed identity. Identity = system assigned. Image = the name of the image from the container registry (this is manually entered when you have a system identity). Image tag (latest) or whatever you used when creating the image.
    - Command Line:
        - Backend:
        ⚠️ Set the appropriate variables before running!
        ```bash
        echo "🔄 Updating backend container settings..."
        az webapp config container set \
          --name $BACKEND_WEB_APP_NAME \
          --resource-group $RESOURCE_GROUP \
          --docker-custom-image-name $ACR_LOGIN_SERVER/backend:latest \
          --docker-registry-server-url https://$ACR_LOGIN_SERVER
        ```
        - Frontend:
        ⚠️ Set the appropriate variables before running!
        ```bash
        echo "🔄 Updating frontend container settings..."
        az webapp config container set \
          --name $FRONTEND_WEB_APP_NAME \
          --resource-group $RESOURCE_GROUP \
          --docker-custom-image-name $ACR_LOGIN_SERVER/frontend:latest \
          --docker-registry-server-url https://$ACR_LOGIN_SERVER
        ```
8. Restart the Web App Resources
    - Click Ops:
        - In the Azure Portal for each resource, manually restart the web app. It will take a few minutes for the web app to pull the new image and use the new code.
    - Command Line
        - Backend:
        ⚠️ Set the appropriate variables before running!
        ```bash
        echo "🔄 Restarting backend web app..."
        az webapp restart --name $BACKEND_WEB_APP_NAME --resource-group $RESOURCE_GROUP
        ```
        - Frontend:
        ⚠️ Set the appropriate variables before running!
        ```bash
        echo "🔄 Restarting frontend web app..."
        az webapp restart --name $FRONTEND_WEB_APP_NAME --resource-group $RESOURCE_GROUP
        ```

## GitHub Configuration
## Create a Service Principal to do the deployments
From the command line run the following command:
```bash
az ad sp create-for-rbac --name "github-acr-push" --role acrpush --scopes $(az acr show --name <ACR_NAME> --query id --output tsv)
```
Be sure to replace the <ACR_NAME> with the name of your Azure Container Registry (e.g. myregistry)

Example output:
```json
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "displayName": "github-acr-push",
  "password": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```
Keep this output safe — you'll need the values for GitHub secrets.


### GitHub Secrets
#### Collect required values
| Secret Name             | Value                                            |
| ----------------------- | ------------------------------------------------ |
| `AZURE_CLIENT_ID`       | `"appId"` from output                            |
| `AZURE_CLIENT_SECRET`   | `"password"` from output                         |
| `AZURE_TENANT_ID`       | `"tenant"` from output                           |
| `AZURE_SUBSCRIPTION_ID` | Run: `az account show --query id -o tsv`         |
| `ACR_NAME`              | Your ACR name (e.g., `myregistry`)               |
| `ACR_LOGIN_SERVER`      | ACR login server (e.g., `myregistry.azurecr.io`) |

#### Add GitHub Secrets
In your GitHub repo:
1. Go to Settings → Secrets and variables → Actions.
2. Click New repository secret for each of the following:

| Name                    | Value                                      |
| ----------------------- | ------------------------------------------ |
| `AZURE_CLIENT_ID`       | From service principal `appId`             |
| `AZURE_CLIENT_SECRET`   | From service principal `password`          |
| `AZURE_TENANT_ID`       | From service principal `tenant`            |
| `AZURE_SUBSCRIPTION_ID` | From `az account show`                     |
| `ACR_NAME`              | Your ACR name                              |
| `ACR_LOGIN_SERVER`      | Your ACR login server (with `.azurecr.io`) |


#### Validate Access (Optional) 
Run this from the command line to test that your service principal is functional:
```bash
az login --service-principal -u <appId> -p <password> --tenant <tenant>
az acr login --name <ACR_NAME>
```

## Build and Push Containers to Registry
### Manual Scripts
There are scripts created that allow you to manually 

Modify the scripts with the correct arguments (e.g. ACR_NAME) to perform the deployments

Make scripts executable
```bash
chmod +x scripts/*.sh
```

Run the command from the root directory:
```bash
./scripts/build-and-push-all.sh v1.0.0
```
### Automated CI/CD
Make a change to the code and push the changes to the main branch (either directly or through a PR). This should trigger the GitHub Actions to run which will build and push your images to the container registry automatically.