from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import requests
from webdev.models import Attempt

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

# Create your views here.
@login_required(login_url='/github/authorize/')
def index(request):
    return render(request, "webdev/index.html")

@login_required(login_url='/github/authorize')
def day1(request):
    return render(request, "webdev/day1.html")

@login_required(login_url='/github/authorize')
def pset1(request):
    if request.method == "POST":
        results = {1: ["At least 2 different headings", 0], 2: ["At least 3 paragraphs", 0], 3: ["At least 1 ordered list", 0], 4: ["At least 1 unordered list", 0], 5: ["At least 2 images", 0], 6: ["At least 1 hyperlink", 0], 7: ["At least 1 bold", 0], 8: ["At least 1 italic", 0], 9: ["At least 1 underline", 0], "passed": 0, "all": 9}
        test_case_passed = 0
    
        url = request.POST["url"]
        data = requests.get(url)
        parsed_html = BeautifulSoup(data.text, features="html.parser")

        # Test case #1: At least 2 different headings
        if len(parsed_html.find_all("h1") + parsed_html.find_all("h2") + parsed_html.find_all("h3") + parsed_html.find_all("h4") + parsed_html.find_all("h5") + parsed_html.find_all("h6")) >= 2:
            test_case_passed += 1
            results[1][1] = 1
        results[1].append(f'expected at least 2 heading tags, found {len(parsed_html.find_all("h1") + parsed_html.find_all("h2") + parsed_html.find_all("h3") + parsed_html.find_all("h4") + parsed_html.find_all("h5") + parsed_html.find_all("h6"))}')
        
        # Test case #2: At least 3 paragraphs
        if len(parsed_html.find_all("p")) >= 3:
            test_case_passed += 1
            results[2][1] = 1
        results[2].append(f'expected at least 3 p tags, found {len(parsed_html.find_all("p"))}')
        
        # Test case #3: At least 1 ordered list
        if len(parsed_html.find_all("ol")) >= 1:
            test_case_passed += 1
            results[3][1] = 1
        results[3].append(f'expected at least 1 ol tag, found {len(parsed_html.find_all("ol"))}')

        # Test case #4: At least 1 unordered list
        if len(parsed_html.find_all("ul")) >= 1:
            test_case_passed += 1
            results[4][1] = 1
        results[4].append(f'expected at least 1 ul tag, found {len(parsed_html.find_all("ul"))}')

        # Test case #5: At least 2 images
        if len(parsed_html.find_all("img")) >= 2:
            test_case_passed += 1
            results[5][1] = 1
        results[5].append(f'expected at least 2 img tags, found {len(parsed_html.find_all("img"))}')

        # Test case #6: At least 1 hyperlink
        if len(parsed_html.find_all("a")) >= 1:
            test_case_passed += 1
            results[6][1] = 1
        results[6].append(f'expected at least 1 a tags, found {len(parsed_html.find_all("a"))}')

        # Test case #7: At least 1 bold
        if len(parsed_html.find_all("b")) >= 1:
            test_case_passed += 1
            results[7][1] = 1
        results[7].append(f'expected at least 1 b tags, found {len(parsed_html.find_all("b"))}')

        # Test case #8: At least 1 italic
        if len(parsed_html.find_all("i")) >= 1:
            test_case_passed += 1
            results[8][1] = 1
        results[8].append(f'expected at least 1 i tags, found {len(parsed_html.find_all("i"))}')

        # Test case #9: At least 1 underline
        if len(parsed_html.find_all("u")) >= 1:
            test_case_passed += 1
            results[9][1] = 1
        results[9].append(f'expected at least 1 u tags, found {len(parsed_html.find_all("u"))}')

        print(test_case_passed)
        results["passed"] = test_case_passed
        results["submission"] = url

        a = Attempt.objects.create(user=request.user, data=results, pset=1)

        return redirect(f"/attempt/{a.id}")
    else:
        return render(request, "webdev/pset1.html")

@login_required(login_url='/github/authorize/')
def view_attempt(request, attempt_id):
    attempt = Attempt.objects.get(user=request.user, id=attempt_id)
    return render(request, "webdev/view-attempt.html", {
        "attempt": attempt
    })

@login_required(login_url='/github/authorize/')
def gradebook(request):
    pset1 = Attempt.objects.filter(user=request.user)[::-1][0]
    return render(request, "webdev/gradebook.html", {
        "pset1": pset1
    })
