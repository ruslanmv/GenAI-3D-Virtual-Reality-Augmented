# Generative AI in 3D Virtual Reality

Hello everyone! In this repository, we are going to build a fascinating demo application that allows us to create 360-degree 3D environments using Generative AI. Imagine having the power to request an environment like, "Let me feel like I am at the beach," and the AI engine generates a 3D environment based on your prompt.

You can use your phone or VR headset to experience the created 3D environment. Additionally, the program can analyze engineering projects and generate 3D prototypes. The possibilities are endless, from generating 360-degree images for immersive 3D experiences with virtual reality to using the chatbot to create prototypes of supercars, airplanes, and more!

## Getting Started

To get started, you'll need the following:

1. An IBM Cloud account.
2. Watson AI services on the IBM Cloud platform.
3. Access to AWS SageMaker.

### Setting up the IBM Cloud and Watson AI

1. Create an account on [IBM Cloud](https://cloud.ibm.com/).

   - Go to the IBM Cloud website and click on "Sign up" to create a new account.
   - Follow the on-screen instructions to set up your account.

2. Once you have your IBM Cloud account, log in to your account [here](https://cloud.ibm.com/iam/apikeys).

   - On this page, click on "Create" to create a new API key.
   - Copy the generated API key.

3. In the project directory, create a `.env` file and add the following line:

   ```plaintext
   API_KEY=<your_ibm_cloud_api_key>
   ```

   - Replace `<your_ibm_cloud_api_key>` with the API key you copied earlier.

4. Additionally, we need to add the `PROJECT_ID` to the `.env` file.

   - Go to your IBM Cloud account, navigate to your project, and click on "Manage".
   - Copy the `Project ID` value.

   ```plaintext
   PROJECT_ID=<your_watsonx_project_id>
   ```

   - Replace `<your_watsonx_project_id>` with your actual WatsonX project ID.

### Setting up AWS SageMaker

1. Create an account on [AWS](https://aws.amazon.com/).

   - Go to the AWS website and click on "Create an AWS Account" to create a new account.
   - Follow the on-screen instructions to set up your account.

2. Once you have an AWS account, follow these steps to create an AWS SageMaker notebook instance:

   - Sign in to the AWS Management Console and open the SageMaker console.
   - In the sidebar, click on "Notebook instances".
   - Click on the "Create notebook instance" button.
   - Provide a name for your notebook instance.
   - Choose an instance type that has GPU support. This is important for running the required deep learning models.
   - (Optional) Customize other settings such as storage volume size, IAM role, etc.
   - Click on "Create notebook instance" to create the instance.

3. Once the notebook instance is created, click on "Open JupyterLab" to open the JupyterLab interface.

   - This will open a new tab in your web browser containing the JupyterLab interface.

### Building the project

1. In the JupyterLab interface, click on the "Terminal" tab to open a terminal.

   - This will open a terminal within the JupyterLab interface.

2. In the terminal, run the following commands to create a Python environment:

   ```bash
   conda create -n myenv python=3.10
   conda activate myenv
   ```

   - These commands create a new Python environment named "myenv" with Python version 3.10 and activate it.

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   - This command installs all the necessary Python packages and libraries required for the project.

4. Clone the repository:

   ```bash
   git clone https://github.ibm.com/ruslanmv/GenAI-3DVR.git
   ```

   - This command clones the project repository to your local machine.

5. Run the application:

   ```bash
   python app.py
   ```

   - This command starts the application and runs the Gradio interface.

6. In the terminal, you will see a link displayed. Copy and paste this link into your web browser.

   - The link will typically be something like `http://localhost:5000`.

7. The Gradio interface will be launched in your web browser.

   - You can now interact with the interface, enter your prompt, and generate 360° images.

8. Additionally, a Gradio shared link will be displayed in the terminal.

   - This link can be shared with others to access the Gradio interface online without running the code locally.

Please note that you need to replace `<your_ibm_cloud_api_key>` and `<your_watsonx_project_id>` with your actual credentials obtained from the IBM Cloud and Watson AI services.

## How to Contribute

We welcome contributions to improve and expand this project. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them to your branch.
4. Submit a pull request to the main repository.

We will review your changes and provide feedback before merging.

## License

This project is licensed under the MIT License.  file for details.

## Acknowledgements

- IBM Cloud and WatsonX AI for providing the AI services.
- The open-source community for their continuous support and inspiration.

Now, let's start building amazing 3D environments using Generative AI!

## Create Breathtaking 360° Worlds with Diffusion Models and LoRA
Imagine exploring a vibrant coral reef, a majestic mountain vista, or a bustling cityscape – all from the comfort of your screen, and in stunning 360°! Thanks to the power of diffusion models and a technique called LoRA (Latent Offset Regression Augmentation), this captivating experience is within reach.

This blog post guides you through the process of creating 360° images using pre-trained models available on platforms like Hugging Face and CivitAI. We'll explore the steps involved, delve into the code, and even build a simple front-end application with Gradio!

### Prerequisites
Before we embark on this creative journey, you'll need a few things:

* **A computer with a GPU:** Diffusion models are computationally intensive, so a GPU is highly recommended for smooth operation.
* **Python:** Ensure you have Python installed along with the required libraries (details in the code section).
* **A diffusion model interface:** We'll use AUTOMATIC1111 web UI ([Automatic1111 web UI for Stable Diffusion]) for this example.

### Setting the Stage: Finding the Right LoRA Model

Hugging Face offers a diverse range of pre-trained models. For our 360° image generation, we'll leverage the "ProGamerGov/360-Diffusion-LoRA-sd-v1-5" model, which utilizes the Stable Diffusion v1.5 base model. CivitAI might also offer similar models, so keep an eye out for tags like "360" or "equirectangular" during your exploration.

### Crafting the Narrative: Building Your Prompt

The magic lies in your text prompt! Here's where you define the essence of your 360° scene. Be as descriptive as possible, detailing the environment, objects, and the overall atmosphere you wish to create.

**Remember:** To activate the LoRA functionality, you need to include the trigger word specific to the chosen model. In our case, for "ProGamerGov/360-Diffusion-LORA-sd-v1-5", the trigger word is "qxj".

Here's an example prompt:

```
qxj, A breathtaking underwater coral reef teeming with colorful fish and vibrant coral formations bathed in sunlight filtering through the crystal-clear water.
```

### Unleashing Creativity: Generating the 360° Image

Now, it's time to bring your vision to life!

**1. Python Code:**

```python
from diffusers import StableDiffusionPipeline

# Load the model and LoRA (modify paths as needed)
pipe = StableDiffusionPipeline.from_pretrained(
    "s3://your-bucket/stable-diffusion-v1-5",  # Replace with your S3 bucket path
    lora_path="s3://your-bucket/ProGamerGov/360-Diffusion-LoRA-sd-v1-5"  # Replace with your S3 bucket path
)

# Craft your prompt with the LoRA trigger word
prompt = "qxj, Your creative prompt here"

# Generate the image
image = pipe(prompt, num_inference_steps=50).images[0]

# Save the image
image.save("your_360_image.png")
```

**2. Running the Code on AWS SageMaker:**

* **Package your code:** Create a Python environment with the required libraries (e.g., `diffusers`, `transformers`). Package your code and dependencies into a Docker image.
* **Create a SageMaker model:** Upload your Docker image to Amazon ECR and create a SageMaker model using the image.
* **Deploy an endpoint:** Deploy the model as an endpoint for real-time inference.
* **Send requests:** Use the SageMaker endpoint to send your prompts and receive the generated 360° images.

**3. Viewing the 360° Image:**

Several online tools and software allow you to view equirectangular images in 360°. You can search for "equirectangular image viewer" to find suitable options.

### Building the User Interface: A Gradio Touch

Gradio is a fantastic library for creating user-friendly interfaces for machine learning models. Let's build a simple Gradio app to interact with the 360° image generation process:

```python
import gradio as gr

def generate_360_image(prompt):
  # Your code from above to generate the image

  # Return the generated image
  return image

interface = gr.Interface(
  fn=generate_360_image,
  inputs="text",
  outputs="image",
  title="Generate 360° Images with LoRA",
)

interface.launch()
```

Save this code as another Python script (e.g., `app.py.py`). Run it using:

```
python app.py.py
```

This will launch the Gradio interface in your web browser, allowing you to enter your prompt and generate 360° images with ease.

### Enriching Prompts with WatsonX.ai (IBM) and LLama2

While the previous sections focused on generating visuals, let's explore how to enrich your prompts with WatsonX.ai, an AI service from IBM.

## Generate Environment Details with Watsonx.ai Llama2: A Step-by-Step Guide

This blog post guides you through creating detailed environment descriptions using Watsonx.ai's Llama2 large language model (LLM). We'll improve the provided script to allow users to specify their desired environment and then generate a rich description using Llama2.

**1. Setting Up:**

Before diving in, ensure you have the following:

* **An IBM Cloud account:** Sign up for a free account if you don't have one at [https://cloud.ibm.com/](https://cloud.ibm.com/).
* **Watsonx.ai service activated:** Activate Watsonx.ai in your IBM Cloud account and obtain your API key and project ID.

**2. Improved Script Breakdown:**

Here's the improved script with explanations:

```python
# Import necessary libraries
import os
from dotenv import load_dotenv

# Import Watsonx.ai libraries
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# Load credentials from a .env file (optional)
load_dotenv()
api_key = os.getenv("api_key", None)
watsonx_project_id = os.getenv("project_id", None)

def get_model(model_type, max_tokens, min_tokens, decoding, temperature):
    """
    Creates a Watsonx.ai LLM model object with specified parameters.
    """
    generate_params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.TEMPERATURE: temperature,
    }

    model = Model(
        model_id=model_type,
        params=generate_params,
        credentials={"apikey": api_key, "url": "https://us-south.ml.cloud.ibm.com"},
        project_id=watsonx_project_id,
    )
    return model

def generate_environment(prompt):
    """
    Generates a detailed description based on the user-provided prompt.
    """
    model_type = ModelTypes.MPT_7B_INSTRUCT2  # Adjust model type if needed
    max_tokens = 250
    min_tokens = 150
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    generated_response = model.generate(prompt=prompt)
    description = generated_response["results"][0]["generated_text"]
    return description

# Get user input for the desired environment
user_prompt = input("Describe your desired environment (e.g., beach with girls): ")

# Generate and print the description using Watsonx.ai Llama2
environment_description = generate_environment(user_prompt)
print(environment_description)
```

**3. Improvements:**

* **User Input:** The script now takes user input for the desired environment through `input()`.
* **Flexibility:** You can adjust the LLM model used (`model_type`) and other generation parameters (`max_tokens`, etc.) for better results.
* **Clarity:** More comments are added for better understanding.

**4. Running the Script:**

1. Save the script as a Python file (e.g., `generate_environment.py`).
2. Replace placeholders (`api_key`, `watsonx_project_id`) in your `.env` file with your actual credentials.
3. Run the script using `python generate_environment.py`.
4. Enter your desired environment prompt (e.g., `beach with girls`).
5. The script will use Watsonx.ai Llama2 to generate a detailed description based on your prompt.

**5. Note:**

* This script provides a basic example. You might need to adjust parameters and logic based on your specific needs and desired level of detail for the environment descriptions.
* Ensure you have Python and the required libraries installed before running the script.

**4. Building a Comprehensive Prompt:**

* **Combine elements:** Integrate the generated enrichments from WatsonX.ai, potentially refined by LaMDA 2, with your core creative prompt.
* **Example:**

```
qxj, A vibrant coral reef teeming with colorful fish, as described by a marine biologist with details on their unique adaptations (enrichment from WatsonX.ai). The sunlight filters through the crystal-clear water, illuminating the diverse coral formations in a mesmerizing display (your creative prompt).
```

By combining these tools, you can craft even more informative and inspiring prompts for your 360° image generation, enriching your creative journey.

Remember, this is just an example, and the possibilities are vast! Experiment with different LoRA models, prompt engineering techniques, and AI tools to unlock a world of creative expression in the realm of 360° imagery.

**5. Leveraging Gradio for Prompt Enrichment:**

* **Modify Gradio interface:** Update your Gradio interface to accept additional inputs for specifying the desired enrichment type and any relevant data for WatsonX.ai.
* **Integration example:**

```python
from gradio import Interface
from generate_environment import generate_environment as process_prompt

def generate_360_image(prompt, enrichment_type, data=None):
    # Use enrichment_type and data to trigger WatsonX.ai and potentially Llama 2
    # (implementation details omitted for brevity)
    enriched_prompt = process_prompt(prompt)

    # Generate the image using the enriched prompt
    # Note: You need to replace this line with your actual image generation code
    image = pipe(enriched_prompt, num_inference_steps=50).images[0]

    # Return the generated image
    return image

interface = Interface(
    fn=generate_360_image,
    inputs=["text", "dropdown", "text"],  # Prompt, enrichment type, and data (optional)
    outputs="image",
    title="Generate Enriched 360° Images with LoRA",
    description="Craft your prompt, choose enrichment, and witness the magic!",
)

interface.launch()

```

This enhanced Gradio interface allows users to not only create prompts but also specify the desired enrichment, potentially leading to even more creative and informative 360° image generation experiences.

**Remember:**

I hope this comprehensive guide empowers you to embark on a journey of creating captivating 360° worlds using the power of diffusion models, LoRA, and AI-driven prompt enrichment!
