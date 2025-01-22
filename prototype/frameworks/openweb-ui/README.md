## Open-WebUI as an AI Agent framework

[Tim Baek, the founder of Open WebUI, shows why his project has over 3M downloads and 50K GitHub
stars.](https://youtu.be/-yyMSBARfgM?si=xriJzGZsZvDVI3Hz)

## AI Platform on OpenShift: Open-WebUI

If you've checked out [open-webui](https://docs.openwebui.com/) chances are you got up and running quickly with `ollama`. `open-webui` has a ton of
cool features like enabling web-search and RAG with chats. There is also a community maintained [`Tools` and `Functions`
collection](https://docs.openwebui.com/features/plugin/) with which to craft AI powered applications.

Check out the [open-webui documentation](https://docs.openwebui.com/).

### Run in OpenShift

This example configures chat web-search with `duckduckgo` search engine that requires no api key. 
This example will configure a [Google PSE](https://developers.google.com/custom-search/docs/tutorial/creatingcse)
if you:

1. Create a secret named `open-webui-google-pse` with the matching values in the commented section of [./openshift-deploy/resources/deployment.yaml]
2. Uncomment the section with the `open-webui-google-pse`

This example enables chat with `OPENAI` endpoint provided from a `vLLM/KServe` in-cluster `mixtral` model. See the deployment for the
secret and values that designate this. It also enables an embedded OLLAMA_BASE_URL with an ollama container within
the pod that allows for serving and downloading models from ollama registry. Remove the OPENAI references if not
running in this cluster or if you do not have an OPENAI_BASE_URL available. If in another cluster with another
OPENAI endpoint, create the `mixtral-vllm-key` secret and update the OPENAI_API_BASE_URL. These references are in
[./openshift-deploy/resources/deployment.yaml](./openshift-deploy/resources/deployment.yaml):

OPENAI endpoint refs to remove if no access to OPENAI endpoint (embedded `OLLAMA_API` endpoint will be used instead)

```yaml
         env:
            - name: OPENAI_API_BASE_URL
              value: "https://mixtral-mixtral-serve.example.com/v1"
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: mixtral-vllm-key
                  key: api_key
```

If you are logged into an OpenShift cluster, run the following from this directory:

```bash
oc new-project open-webui 
oc apply --kustomize ./openshift-deploy
oc get routes
```

You should be able to access the route and can from here experiment with the various open-webui features. Many of the
features available in the settings through the UI will be persisted, and many of them can be configured as
environment variables. 
