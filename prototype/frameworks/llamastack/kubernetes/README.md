# VLLM serve
This serves as a starting point to deploy `meta-llama/Llama-3.1-8B-Instruct` long term this should be handled by RHOAI.

## Requirements
A secret must be created to allow for the vLLM server to pull in the model at startup time.

```
oc create secret generic huggingface-secret --from-literal=HF_TOKEN=hf_values
```

## Deploy
The vLLM deployment will take the secret from above and use it to pull in the model. To launch the vLLM deployment run the following.

```
oc create -f llama-serve/vllm.yaml
oc expose deployment/vllm
```

## Using the vLLM server
The vLLM instance is running with a service this service can be accessed by other namespaces in the cluster but also by using port-forward.

To use port-forward run the following.

```
kubectl port-forward service/vllm 8000:8000
```

## Testing
To test the model is operating correctly.

```
 curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 200,
        "temperature": 0
    }'
```


# Llama stack
To run llama stack we can utlize the kubernetes svc address along with providing a configmap for the unique values we want to test.


## Building Llama stack
If you need to use a specific branch or even the main branch of the Llama stack repository in your container image the following steps should be ran.

```
git clone git@github.com:meta-llama/llama-stack.git
python -m venv venv
source venv/bin/activate
pip install -U .
USE_COPY_NOT_MOUNT=true LLAMA_STACK_DIR=. llama stack build --template remote-vllm --image-type container
podman tag localhost/distribution-remote-vllm:dev quay.io/redhat-et/llama:2-27-2025
podman push quay.io/redhat-et/llama:2-27-2025
```

Update the `deployment.yaml` file using the image generated above.

## Configmap
A predefined configmap exists with entirely too many options but is a placeholder for what can be added. Create the configmap defining your unique settings. Then create the CM. The `template.yaml` file does not need to be modified. It contains the jinja chat template.

```
oc create -f llama-stack/configmap.yaml
oc create -f llama-stack/template.yaml
```


## Deployment
The deployment doesn't really have any unique values at this time. We will most likely learn more as we progress

```
oc create -f llama-stack/deployment.yaml
```

## Access
This deployment isn't exposed so depending on where you need to access it from expose it accordingly.

If you want to deploy a chat server and point to the llama-stack then run the following.

```
oc expose deployment/llamastack-deployment
```

If you want to access the llama-stack externally from the cluster then you must expose the svc which will create a route.

```
oc expose svc/llamastack-deployment
```

This will generate a route similar to this.

NOTE: This will be unique to your environment.

```
llamastack-deployment-llama-serve.apps.ocp-beta-test.nerc.mghpcc.org
```

## Using the endpoints
Now that everything is available in the OpenShift cluster you can utilize the vLLM instance and the Llama Stack server by performing the following.

NOTE: The INFERENCE_ADDR will be based on your OpenShift environemnt.

```
export INFERENCE_MODEL="meta-llama/Llama-3.2-1B-Instruct"
export LLAMA_STACK_PORT=8321
export INFERENCE_ADDR=vllm-llama-serve.apps.ocp-beta-test.nerc.mghpcc.org
```