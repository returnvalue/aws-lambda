# Lab 4: Code Reusability (Lambda Layers)

**Goal:** Move shared libraries or custom logic out of the deployment package and into a Lambda Layer, allowing multiple functions to use the same code.

```bash
# 1. Create a dummy Python library folder structure (Required for Layers)
mkdir -p python
cat <<EOF > python/custom_logger.py
def log_message(msg):
    return f"[CUSTOM LAYER LOG] {msg}"
EOF

# 2. Zip the layer
zip -r layer.zip python

# 3. Publish the Layer version
LAYER_ARN=$(awslocal lambda publish-layer-version \
  --layer-name CustomLoggerLayer \
  --description "Shared logging utility" \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.9 \
  --query 'LayerVersionArn' --output text)

# 4. Attach the Layer to your existing Lambda function
awslocal lambda update-function-configuration \
  --function-name ServerlessProcessor \
  --layers $LAYER_ARN
```

## 🧠 Key Concepts & Importance

- **Lambda Layers:** A distribution mechanism for libraries, custom runtimes, and other function dependencies. Layers allow you to manage shared code and data separately from your function code.
- **Code Reusability:** By putting common code in a layer, multiple functions can use it without including it in their deployment package. This reduces the size of your deployment packages and makes it easier to update shared code.
- **Layer Structure:** Lambda layers are extracted to the `/opt` directory in the function's execution environment. For Python, libraries should be placed in a `python/` folder within the zip file so they are automatically added to the `sys.path`.
- **Versioning:** Layers are versioned. Each time you publish a new version, a new ARN is generated. Functions must be updated to use the specific version ARN.
- **Separation of Concerns:** Keep your function code focused on its specific business logic while offloading common utilities (like logging, authentication, or SDKs) to layers.

## 🛠️ Command Reference

- `lambda publish-layer-version`: Creates an AWS Lambda layer from a ZIP archive.
    - `--layer-name`: The name of the layer.
    - `--description`: A brief description of the layer version.
    - `--zip-file`: The path to the ZIP archive containing the layer content.
    - `--compatible-runtimes`: A list of runtimes that the layer is compatible with.
- `lambda update-function-configuration`: Updates the configuration for a specific Lambda function.
    - `--function-name`: The name of the function to update.
    - `--layers`: A list of function layers to add to the function (ARNs).
