## Run Open WebUI in local container

This example uses vLLM to serve a single GGUF model locally. It uses [ramalama](https://github.com/containers/ramalama)
to download the model and podman to run vLLM. It runs Open WebUI as a pod with the OpenAI API URL
from the local vLLM. Ollama is not used in this example.

vLLM is not supported on arm (MacOS), so this will only work on x86 systems.
You can switch vLLM for a local llamacpp server if running on MacOS.

### 1. Pull models from huggingface using `ramalama`

#### Install ramalama

```bash
git clone git@github.com:containers/ramalama && cd ramalama
python -m venv venv
source venv/bin/activate
pip install ramalama
cp venv/bin/ramalama ~/.local/bin/.
deactivate
which ramalama # ensure it's there
ramalama pull huggingface://bartowski/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf
```

You should now have this on your filesystem:

```bash
$ ls -al ~/.local/share/ramalama/models/huggingface/bartowski/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf
```

### Run vLLM container

Serve Llama3 model with vLLM. This only works on x86 systems for now.
The vLLM container requires privilege. For simplicity, run both as `root` user.

```bash
sudo su
./vllm-podman-cmd
```

### Run Open WebUI container

```bash
sudo su
./open-webui-podman-cmd
```

Access `open-webui` at `http://ip-addr-or-localhost:8001`

You can now interact with the open-webui features. Note I've disabled the ollama API, so it's only using the generic openai API.
I do not have ollama running locally, and I don't need it.

Now check out the [open-webui documentation](https://docs.openwebui.com/) to start playing with your full-featured local AI platform!
The beefier your local system, the better it will be. I'm running in a RHEL AI VM in AWS.
