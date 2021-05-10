from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.conf import settings
import json
import requests
from .models import Articles
import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
from googlesearch import search
import whois
from datetime import datetime
from datetime import date
import time
from dateutil.parser import parse as date_parse
import numpy as np
import pickle
import os
# Create your views here.

def index(request):
    return render(request, 'index.html')

def news(request):
    return render(request, 'news.html')

def news_render(request):
    return render(request, 'news_render.html')

def news_search(request):
    if request.method == 'POST':
        date = request.POST.get('inpDate',False)
        keyword = request.POST.get('newsKeyword',False)
        
        query = "https://newsapi.org/v2/everything?apiKey=b52afaa2a9004a3aab6960fe91c5aac1&language=en&q='"+keyword+"'&from="+date+"&to="+date

        resp = requests.get(query)


        resp = resp.json()
       
        path = os.path.join(settings.BASE_DIR,"FakeDetector/DecisionTree_model.pkl")
        
        with open(path,'rb') as file:
            pickle_model = pickle.load(file)
        
        myObj = []

        if(int(resp['totalResults'])> 0):
            arts = resp["articles"]
            for i in arts:
                desc = i['description']
                predikt = pickle_model.predict([desc])
                id = i['source']['id']
                name = i['source']['name']
                author = i['author']
                title = i['title']
                description = i['description']
                url = i['url']
                published_at = i['publishedAt']
                if(predikt == ['true']):
                    prediction = True
                else:
                    prediction = False
                if ("urlToImage" in i.keys()) and i['urlToImage']!=None:
                    urlToImage = i['urlToImage']
                else:
                    urlToImage = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOQAAADdCAMAAACc/C7aAAAAaVBMVEXDw8MAAADGxsaXl5fJycnMzMxSUlKRkZF1dXV5eXnCwsIFBQWlpaV+fn66urqurq5dXV1sbGxMTEyKiopXV1czMzOcnJwaGhqoqKiEhIQlJSUrKysODg5mZmZHR0ezs7M7OzsVFRU5OTmFwHepAAAC+klEQVR4nO3bi1KjMBSAYXIarIbea2uttVXf/yE36Q0qobrITHP0/2Z2Zt2xDP+GQEDMMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANQ56dCtY+JcZge9zgzsrXvipGc61EtzLO29KbpKLMx9mkPpI83H410XFiblyGFufy7Ph0lHPnSya/aByFuqRv7sSqchUvwV83k4EHFtt6QhcrwOl4GXZdv9VBApq3CdK/w1c9nykNUQ+XK6pG/abin5SFmWy5Z+u6FMP7K6unttt6cKIqflSE4a9tQd/zRtKflI6ZeRw6Y9deFS2ryl5COzUXkzMWoIcZm45bixUkGkfd6PormyyBMZPxkzaVouKIjM7PAwjtPm/XRP4Rse8/hgaoh0djzdbl9XeePJxc7CUBdmHi/REOkPx3Bb2DTlnOwP6L34vNQReZ3szqffRXRa/oJIcetzpJnksS2pj3T5pPrIqmfr6wL9kbZvynWf/8uuPi21Rzrxa4WijCzMW/0j6iKdV/lSZPH5Ges0V3+4flqi+uV77Ql07QmCtkg7GlcumM4uI0/ZC+UjGe67FpVl+qhWGGw/f0pRpIS99aeWjTtV2rdopBleTktNkZkMwvmzMHf20BCaY42FWV3MXFWR2eZY8ezvpY/N8aF8UhuZz84jtV+Iu/d4YfiGu+oHFUX6e43i1LDODs1FfCT9P8+lXN7piZRxNWOS23nTOB7syvsRPZHZ+qKhv2uckMfBLqelmsjLew1/anlpOlbLwT5vSUeks/2rQVG9U5eSyLC0+f+3JE53XToiRT6+OjhjPjRFunz6dVHM9DAtVURG7zW+ZbAfSw2R0mpCHvi1vFMRabctC/1/zdaKisjTTwnaRIYfhCmIdHbQunF/Rl5J8pEizfca37Pxkzr5yNnXHdfNJPGRHNrRvP9D81HqkbnNO5D2W5K//X1XFyK7kuyby3/iHXTp8rcJVmk2/onfCwEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALi1f4DsKck70eEzAAAAAElFTkSuQmCC"
                ArtObj = Articles()
                ArtObj.id = id
                ArtObj.name = name
                ArtObj.author = author
                ArtObj.title = title
                ArtObj.description = description
                ArtObj.url = url
                ArtObj.published_at = published_at
                ArtObj.prediction = prediction
                ArtObj.urlToImage = urlToImage
                myObj.append(ArtObj)
            return render(request,'news_render.html',{"newss":myObj})
        else:
            return HttpResponse("<h1>No news found</h1>")
        
def verify_news(request):
    return render(request, 'verify_news.html')


def news_checker(request):
    if request.method == "POST":
        newsText = request.POST.get('newsPastingArea',False)

        path = os.path.join(settings.BASE_DIR,"FakeDetector/DecisionTree_model.pkl")
      
        with open(path,'rb') as file:
            
            pickle_model = pickle.load(file)

        pre = pickle_model.predict([newsText])

        if(pre == ['fake']):
            pre = "fake"
        else:
            pre = "true"
        
        dict  = {"prediction":pre}
        return JsonResponse(dict,status = 200)

def phishing_detection(request):
    return render(request, 'phishing_detection.html')

# verifying the phish

def phishing_checker(request):

    inArr = ["ckpcet.ac.in","scet.ac.in","https://ckpcet.ac.in","https://scet.ac.in","http://ckpcet.ac.in","http://ckpcet.ac.in","www.ckpcet.ac.in","www.scet.ac.in"]

    def diff_month(d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

# Generate data set by extracting the features from the URL


#1. Having IP address

    def having_ip_address(url):
        try:
            ipaddress.ip_address(url)
            return -1
        except:
            return 1

    #2. URL length

    def url_len(url):
        if len(url) < 54:
            return 1
        elif len(url) >= 54 and len(url) <= 75:
            return 0
        else:
            return -1

    #3. Shortening Service

    def shortening_service(url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
        if match:
            return -1
        else:
            return 1

    #4. having @ symbol        

    def having_at_symbol(url):
        if re.findall("@", url):
            return -1
        else:
            return 1

    #5. double slash redirect

    def double_slash_redirect(url):
        list = [x.start(0) for x in re.finditer('//', url)]
        if list[len(list)-1] > 6:
            return -1
        else:
            return 1

    #6. prefix suffix

    def prefix_suffix(url):
        if re.findall(r"https?://[^\-]+-[^\-]+/", url):
            return -1
        else:
            return 1

    #7. having sub domain

    def having_subdomain(url):
        if len(re.findall("\.", url)) == 1:
            return 1
        elif len(re.findall("\.", url)) == 2:
            return 0
        else:
            return -1

    #8. ssl final state

    def ssl_final_state(url,response):
        try:
            if response.text:
                return  1
            else:
                return 0
        except:
            return -1

    #9. Domain registration length

    def Domain_registeration_length(url,whois_response):
        expiration_date = whois_response.expiration_date
        registration_length = 0
        try:
            expiration_date = min(expiration_date)
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            registration_length = abs((expiration_date - today).days)

            if registration_length / 365 <= 1:
                return -1
            else:
                return 1
        except:
            return 0

    #10. Favicon

    def favicon(url,soup,domain):
        if soup == -999:
            return -1
        else:
            try:
                for head in soup.find_all('head'):
                    for head.link in soup.find_all('link',href=True):
                        dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                        if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                            return 1
                            raise StopIteration
                        else:
                            return -1
                            raise StopIteration
            except StopIteration:
                return 0
    #11 port

    def port(url):
        try:
            port = domain.split(":")[1]
            if port:
                return -1
            else:
                return 1
        except:
            return 1

    #12 HTTPS token

    def https_token(url):
        if re.findall(r"^https://", url):
            return 1
        else:
            return -1

    #13 Request URL

    def request_url(soup,domain,url):
        i = 0
        success = 0
        if soup == -999:
            return -1
        else:
            for img in soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                if url in img['src'] or domain in img['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for audio in soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for embed in soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for iframe in soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            try:
                percentage = success/float(i) * 100
                if percentage < 22.0:
                    return 1
                elif((percentage >= 22.0) and (percentage < 61.0)):
                    return 0
                else:
                    return -1
            except:
                return 0

    #14 URL of anchor

    def url_of_anchor(soup,url,domain):
        percentage = 0
        i = 0
        unsafe = 0
        if soup == -999:
            return -1
        else:
            for a in soup.find_all('a', href=True):
                # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                # there in the actual a['href']
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                    unsafe = unsafe + 1
                i = i + 1

            try:
                percentage = unsafe / float(i) * 100
            except:
                return 1

            if percentage < 31.0:
                return 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                return 0
            else:
                return -1

    #15 Links in tag

    def links_in_tag(url,soup,domain):
        i = 0
        success = 0
        if soup == -999:
            return -1
        else:
            for link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                if url in link['href'] or domain in link['href'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for script in soup.find_all('script', src=True):
                dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                if url in script['src'] or domain in script['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1
            try:
                percentage = success / float(i) * 100 
                if percentage < 17.0 :
                    return 1
                elif((percentage >= 17.0) and (percentage < 81.0)) :
                    return 0 
                else :
                    return -1
            except:
                return 1

    #16 server form handler

    def  SFH(url,soup):
        try:
            for form in soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    return -1
                elif url not in form['action'] and domain not in form['action']:
                    return 0
                else:
                    return 1
        except:
            return -1

    #17 submitting to email

    def submitting_to_email(url,response):
        if response == "":
            return -1
        else:
            if re.findall(r"[mail\(\)|mailto:?]", response.text):
                return 1
            else:
                return-1

    #18 Abnormal URL

    def abnormal_url(response):
        if response == "":
            return -1
        else:
            if response.text == "":
                return 1
            else:
                return -1

    #19 Redirect

    def redirect(response):
        if response == "":
            return -1
        else:
            if len(response.history) <= 1:
                return -1
            elif len(response.history) <= 4:
                return 0
            else:
                return 1

    #20 on mouse over

    def on_mouse_over(response):
        if response == "":
            return -1
        else:
            if re.findall("<script>.+onmouseover.+</script>", response.text):
                return 1
            else:
                return -1

    #21 right click

    def right_click(response):
        if response == "":
            return -1
        else:
            if re.findall(r"event.button ?== ?2", response.text):
                return 1
            else:
                return -1

    #22 popupwindow

    def popup_window(response):
        if response == "":
            return -1
        else:
            if re.findall(r"alert\(", response.text):
                return 1
            else:
                return -1

    #23 Iframe

    def iframe(response):
        if response == "":
            return -1
        else:
            if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                return 1
            else:
                return -1

    #24 age of domain

    def age_of_domain(response):
        if response == "":
            return -1
        else:
            try:
                registration_date = re.findall(
                    r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
                if diff_month(date.today(), date_parse(registration_date)) >= 6:
                    return -1
                else:
                    return 1
            except:
                return 0

    #25 DNS Record

    def dns_record(domain,whois_response):
        dns = 1
        try:
            d = whois.whois(domain)
        except:
            dns = -1
        expiration_date = whois_response.expiration_date
        registration_length = 0
        try:
            expiration_date = min(expiration_date)
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            registration_length = abs((expiration_date - today).days)
            if dns == -1:
                return -1
            else:
                if registration_length / 365 <= 1:
                    return -1
                else:
                    return 1
        except:
            return -1

    #26 web traffic

    def web_traffic(url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen(
                "http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
            rank = int(rank)
            if (rank < 100000):
                return 1
            else:
                return 0
        except TypeError:
            return -1


    #27 page rank

    def page_rank(global_rank):
        try:
            if global_rank > 0 and global_rank < 100000:
                return -1
            else:
                return 1
        except:
            return 0

    #28 google index

    def google_index(url):
        site = search(url, 5)
        if site:
            return 1
        else:
            return -1

    #29 links pointing to page

    def links_pointing_to_page(response):
        if response == "":
            return -1
        else:
            number_of_links = len(re.findall(r"<a href=", response.text))
            if number_of_links == 0:
                return 1
            elif number_of_links <= 2:
                return 0
            else:
                return -1

    #30 statistical report

    def statistical_report(url):
        url_match = re.search(
            'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
        try:
            ip_address = socket.gethostbyname(domain)
            ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                                '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                                '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                                '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                                '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                                '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match:
                return -1
            elif ip_match:
                return -1
            else:
                return 1
        except:
            return 0
            print('Connection problem. Please check your internet connection!')





    def get_predictions(url):
        if not re.match(r"^https?", url):
            url = "http://" + url

        # Stores the response of the given URL
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            response = ""
            soup = -999

        # Extracts domain from the given URL
        domain = re.findall(r"://([^/]+)/?", url)[0]
        if re.match(r"^www.", domain):
            domain = domain.replace("www.", "")

        # Requests all the information about the domain
        whois_response = whois.whois(domain)

        rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
                "name": domain
        })

        try:
            global_rank = int(re.findall(
                r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
        except:
            global_rank = -1




        #calling functions

        data_array = []

        data_array.append(having_ip_address(url))

        data_array.append(url_len(url))

        data_array.append(shortening_service(url))

        data_array.append(having_at_symbol(url))

        data_array.append(double_slash_redirect(url))

        data_array.append(prefix_suffix(url))

        data_array.append(having_subdomain(url))

        data_array.append(ssl_final_state(url,response))

        data_array.append(Domain_registeration_length(url,whois_response))

        data_array.append(favicon(url,soup,domain))

        data_array.append(port(domain))

        data_array.append(https_token(url))

        data_array.append(request_url(soup,domain,url))

        data_array.append(url_of_anchor(soup,url,domain))

        data_array.append(links_in_tag(url,soup,domain))

        data_array.append(SFH(url,soup))

        data_array.append(submitting_to_email(url,response))

        data_array.append(abnormal_url(response))

        data_array.append(redirect(response))

        data_array.append(on_mouse_over(response))

        data_array.append(right_click(response))

        data_array.append(popup_window(response))

        data_array.append(iframe(response))

        data_array.append(age_of_domain(response))

        data_array.append(dns_record(domain,whois_response))

        data_array.append(web_traffic(url))

        data_array.append(page_rank(global_rank))

        data_array.append(google_index(url))

        data_array.append(links_pointing_to_page(response))
        
        for i in range(0,len(data_array)):
            if data_array[i] is None:
                data_array[i]=0

        new_input = []
        new_input.append(data_array)
        array = np.array(new_input)
        array.reshape(-1,1)

        pkl_filename = os.path.join(settings.BASE_DIR,"FakeDetector/random_forest_model.pkl")
        with open(pkl_filename,'rb') as file:
            pickle_model = pickle.load(file)

        new_output = pickle_model.predict(array)
        return new_output[0]
    
    if request.method == "POST":
        URL = request.POST.get('inputURL',False)

    

        pre = get_predictions(URL)
        
        if(pre>=-1 and pre<0.5):
            pre = "Phish"
        elif(pre>=0.5 and pre<=1):
            pre = "Authentic"
        else:
            pre = "Doubt"
        
        if(URL in inArr):
            pre = "Authentic"
        
        dict  = {"prediction":pre}
        return JsonResponse(dict,status = 200)