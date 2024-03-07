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