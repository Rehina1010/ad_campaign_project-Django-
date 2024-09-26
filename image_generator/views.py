import os
from django.shortcuts import render
from .forms import ImagePromptForm
import requests
from io import BytesIO
import base64
from django.contrib import messages
import json
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HUGGING_FACE_ACCESS_TOKEN = os.getenv('HUGGING_FACE_ACCESS_TOKEN')

def generate_image(request):
    image_url = None
    download_link = None

    if request.method == 'POST':
        form = ImagePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            print(f"Generating image for prompt: {prompt}")

            headers = {
                "Authorization": f"Bearer {HUGGING_FACE_ACCESS_TOKEN}"
            }

            data = {
                "inputs": prompt,
                "options": {
                    "wait_for_model": True
                }
            }

            try:
                response = requests.post(HUGGING_FACE_API_URL, headers=headers, data=json.dumps(data))

                if response.status_code == 200:
                    image_data = response.content
                    buffer = BytesIO(image_data)
                    buffer.seek(0)

                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    image_url = f"data:image/png;base64,{image_base64}"
                    download_link = f"data:image/png;base64,{image_base64}"
                else:
                    messages.error(request, f"Failed to generate image: {response.status_code} - {response.text}")
                    print(f"Error from API: {response.status_code} - {response.text}")

            except Exception as e:
                messages.error(request, f"An error occurred while generating the image: {e}")
                print(f"Error generating image: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = ImagePromptForm()

    return render(request, 'image_generator/generate_image.html', {
        'form': form,
        'image_url': image_url,
        'download_link': download_link
    })
