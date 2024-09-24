from django.shortcuts import render
from .forms import ImagePromptForm
import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64
from django.contrib import messages


def init_pipeline():
    print("Model downloading...")
    try:
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        device = torch.device(
            "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
        pipe.to(device)
        print("Model downloaded")
        return pipe
    except Exception as e:
        print(f"An error occurred while downloading the model: {e}")
        raise RuntimeError("Failed to initialize the image generation model. Please try again later.")


pipeline = init_pipeline()


def generate_image(request):
    image_url = None
    download_link = None

    if request.method == 'POST':
        form = ImagePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            print(f"Image generation for prompt: {prompt}")
            try:
                image = pipeline(prompt, num_inference_steps=20).images[0]

                buffer = BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)

                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                image_url = f"data:image/png;base64,{image_base64}"
                download_link = f"data:image/png;base64,{image_base64}"

            except Exception as e:
                messages.error(request, f"An error occurred while generating the image: {e}")
                print(f"Error generating image: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = ImagePromptForm()

    return render(request, 'image_generator/generate_image.html',
                  {'form': form, 'image_url': image_url, 'download_link': download_link})
