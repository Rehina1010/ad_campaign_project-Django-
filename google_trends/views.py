from django.shortcuts import render
from pytrends.request import TrendReq
from django.views.generic import TemplateView
from .forms import TrendForm
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
from .trends import get_google_trends_data
from pytrends.exceptions import TooManyRequestsError
import pandas as pd

matplotlib.use('Agg')


def trends_view(request):
    form = TrendForm(request.POST or None)
    graph_url = None
    top_countries = None

    if request.method == 'POST' and form.is_valid():
        keyword = form.cleaned_data['keyword']
        pytrends = TrendReq(hl='en-US', tz=360)

        try:
            pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')

            plt.figure(figsize=(10, 6))
            trends_data = get_google_trends_data(keyword)
            plt.plot(trends_data.index, trends_data[keyword])
            plt.xlabel('Date')
            plt.ylabel('Interest')
            plt.title(f'Google Trends for {keyword}')
            plt.grid(True)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            interest_by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            top_countries = interest_by_region[keyword].sort_values(ascending=False).head(10).to_dict()

        except TooManyRequestsError:
            print("Too many requests. Please try again later.")
            return render(request, 'trends.html', {
                'form': form,
                'error_message': "Too many requests. Please try again later.",
                'graph_url': graph_url,
                'top_countries': top_countries,
            })
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'trends.html', {
                'form': form,
                'error_message': f"An error occurred: {e}",
                'graph_url': graph_url,
                'top_countries': top_countries,
            })

    return render(request, 'trends.html', {
        'form': form,
        'graph_url': graph_url,
        'top_countries': top_countries,
    })


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class CookiePolicyView(TemplateView):
    template_name = 'cookie_policy.html'


class TermsView(TemplateView):
    template_name = 'terms.html'