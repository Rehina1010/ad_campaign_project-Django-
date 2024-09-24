import re
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import google.generativeai as gai
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from .models import Campaign
from .forms import CampaignForm
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY_FOR_AI')


@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(owner=request.user)
    return render(request, 'campaigns/campaign_list.html', {'campaigns': campaigns})


@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)
    return render(request, 'campaigns/campaign_detail.html', {'campaign': campaign})


@login_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.owner = request.user
            campaign.save()
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/campaign_form.html', {'form': form})


@login_required
def edit_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaigns/campaign_form.html', {'form': form})


@login_required
def delete_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted successfully.')
        return redirect('campaigns:campaign_list')
    return render(request, 'campaigns/campaign_confirm_delete.html', {'campaign': campaign})


def clean_text(text):
    cleaned_text = re.sub(r'\*', '', text).strip()
    return cleaned_text


@login_required
def improve_campaign(request, pk):
    if not api_key:
        messages.error(request, "API key for AI is not configured.")
        return redirect('campaigns:campaign_detail', pk=pk)

    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)

    if request.method == 'POST':
        prompt = (
            f"I want to improve my Google Ads campaign. Please provide the following information in the format 'key: value' "
            f"so I can easily extract it.\n\n"
            f"Campaign Name: {campaign.title}\n"
            f"Budget for the day: {campaign.budget}\n"
            f"Description: {campaign.description}\n\n"
            f"Please respond with the improved data for 'Improved Campaign Name', 'Improved Budget', 'Improved Description', "
            f"and explanations for why these changes were made, formatted as 'key: value'.")

        gai.configure(api_key=api_key)
        model = gai.GenerativeModel('gemini-1.5-flash-8b-exp-0827')
        try:
            response = model.generate_content(prompt)
            improved_text = response.text
            cleaned_text = clean_text(improved_text)
            improved_data = extract_improvements(cleaned_text)

            return render(request, 'campaigns/improve_campaign.html', {
                'campaign': campaign,
                'improved_data': improved_data,
                'explanation': cleaned_text
            })
        except Exception as e:
            messages.error(request, f"Error generating content: {e}")
            return redirect('campaigns:campaign_detail', pk=pk)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def extract_improvements(text):
    title_match = re.search(r'Improved Campaign Name:\s*(.*)', text)
    title = title_match.group(1).strip() if title_match else None

    description_match = re.search(r'Improved Description:\s*(.*)', text)
    description = description_match.group(1).strip() if description_match else None

    budget_match = re.search(r'Improved Budget:\s*([\d.]+)', text)
    try:
        budget = float(budget_match.group(1)) if budget_match else None
    except ValueError:
        budget = None

    return {
        "title": title,
        "description": description,
        "budget": budget
    }


@login_required
def save_improvements(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, owner=request.user)

    if request.method == 'POST':
        improved_title = request.POST.get('improved_title')
        improved_description = request.POST.get('improved_description')
        improved_budget = request.POST.get('improved_budget')

        if improved_title:
            campaign.title = improved_title
        if improved_description:
            campaign.description = improved_description
        if improved_budget:
            try:
                campaign.budget = float(improved_budget)
            except ValueError:
                messages.error(request, 'Invalid budget value.')
                return redirect('campaigns:campaign_detail', pk=pk)

        campaign.save()
        messages.success(request, 'Campaign improvements saved successfully.')
        return redirect('campaigns:campaign_detail', pk=pk)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
