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