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
