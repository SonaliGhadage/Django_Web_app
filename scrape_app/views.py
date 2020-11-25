from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from bs4 import BeautifulSoup
from urllib.request import urlopen

from urllib.error import HTTPError
from urllib.error import URLError

import logging
# To avoid ssl errors
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# This function allows us to handle the traffic from home page
def home(request):
    return render(request, "home.html")

# Function to extract data from given website with some test cases
def get_data(request):
    # As we want to post the url link, we are using POST method here
    val1 = request.POST["url"]

    if val1:

        # Checking for valid url
        try:
            page = urlopen(val1)
        except HTTPError as e:
            messages.info(request, "HTTP error")
            return redirect("home")
        except URLError as e:
            messages.info(request, "Server not found!")
            return render(request, "base.html")
        

        # Checking for valid information source of the website
        try:
            page = urlopen(val1)
            html = page.read()
            soup = BeautifulSoup(html, "html.parser")
            app_name = soup.find('div',attrs={'class': 'header-desktop__LongNameContainer-xc5gow-10 eZHaNZ'}).get_text(' ')
            app_version = soup.find('dd',attrs={'class': "information__Value-xn2n41-2 dvSoPl"}).get_text()
            no_of_downloads = soup.find('span', attrs={'class': "label-with-icon__LabelWithIcon-sc-162xi5e-0 bZRhOm"}).get_text()
            release_date = soup.find("meta", itemprop="datePublished")
            desc1 = soup.find('div', attrs={'class':'description__DescBody-sc-45j1b1-0 gdwZQU'})
            desc = desc1.find('p', itemprop="description").get_text("\n")
            return render(request, "result.html", {"app_name":app_name, "app_v":app_version, "app_d":no_of_downloads, "r_date":release_date["content"], "description":desc})

        except:
            messages.info(request, "Data not found, Invalid URL!")
            return render(request, "base.html")
        
    elif type(val1) == type(str):
        messages.info(request, "Please valid URL")
        return redirect("home")


    else:
        messages.info(request, "Please enter valid URL")
        return redirect("home")
    
