The demo from [here](https://github.com/benalexkeen/streamlit-azure-app-services) needed a tweak - set altair\<5 in requirements.txt.

Then run it locally - works.

Deploy Azure resource group:
```bash
az group create --name Govhack2023 --location "Australia East"
```
Deploy the template and parameters I modified:
```bash
az deployment group create \
  --name ExampleStreamlit \
  --resource-group Govhack2023 \
  --template-uri "https://github.com/jessearcana/govhack2023/streamlit-azure-app-services/azuredeploy.json" \
  --parameters '@streamlit-azure.parameters.json'
```