from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import requests
from webdev.models import Attempt
import js2py

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import cssutils
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By as by
from selenium.common.exceptions import NoSuchElementException        


# Create your views here.
def load_chrome_driver():

      options = Options()

      options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

      options.add_argument('--headless')
      options.add_argument('--disable-gpu')
      options.add_argument('--no-sandbox')
      options.add_argument('--remote-debugging-port=9222')

      return webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)

def cylinder_volume():
    import math
    import random

    r = random.randint(1, 10)
    h = random.randint(1, 10)

    return r, h, round(math.pi * r * r * h, 1)

@login_required(login_url='/github/authorize/')
def index(request):
    return render(request, "webdev/index.html")

@login_required(login_url='/github/authorize')
def day1(request):
    return render(request, "webdev/day1.html")

@login_required(login_url='/github/authorize')
def day2(request):
    return render(request, "webdev/day2.html")

@login_required(login_url='/github/authorize')
def day3(request):
    return render(request, "webdev/day3.html")

@login_required(login_url='/github/authorize')
def day4(request):
    return render(request, "webdev/day4.html")

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

@login_required(login_url='/github/authorize')
def pset2(request):
    if request.method == "POST":
        url = request.POST["url"]
        data = requests.get(url)

        parsed_html = BeautifulSoup(data.text, features="html.parser")

        if url[-1] == "/":
            url += "style.css"
        else:
            url += "/style.css"
        data = requests.get(url)
        sheet = cssutils.parseString(data.content)

        results = {}
        testcases = {1: ["Styles must be written in style.css", 0], 2: ["Style.css must be linked properly to the HTML", 0], 3: ["Use at least 5 selectors", 0], 4: ["At least 2 class selectors", 0], 5: ["At least 2 ID selectors", 0], 6: ["At least 2 fonts", 0], 7: ["At least 2 colors", 0], 8: ["At least 1 border usage", 0], 9: ["At least 1 flexbox usage", 0], "all": 9}

        color_count = 0
        font_count = 0
        border_count = 0
        flex_count = 0
        id_count = 0
        class_count = 0

        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for prop in rule.style:
                        results[rule.selectorText] = [prop.name, prop.value]
                        if prop.name == "font-family":
                            font_count += 1
                        elif "color" in prop.name:
                            color_count += 1
                        elif "border" in prop.name:
                            border_count += 1
                        elif "display" in prop.name and "flex" in prop.value:
                            flex_count += 1
                        elif rule.selectorText[0] == "#":
                            id_count += 1
                        elif rule.selectorText[0] == ".":
                            class_count += 1
        
        test_case_passed = 0
        # Test case #1
        if data.status_code == 200:
            test_case_passed += 1
            testcases[1][1] = 1
        testcases[1].append(f'expected status code 200, got status code {data.status_code}')
        
        # Test case #2
        link = parsed_html.find_all("link", attrs={"rel": "stylesheet", "href": "style.css"}) # 
        if len(link) == 1:
            test_case_passed += 1
            testcases[2][1] = 1
        testcases[2].append(f"expected style.css linked as stylesheet, found {len(link)}")

        # Test case #3
        selectors_count = len(results.keys())
        if selectors_count >= 5:
            test_case_passed += 1
            testcases[3][1] = 1   
        testcases[3].append(f"expected 5 selectors, found {selectors_count}")

        # Test case #4
        if class_count >= 2:
            test_case_passed += 1
            testcases[4][1] = 1   
        testcases[4].append(f"expected 2 class selectors, found {class_count}")
        
        # Test case #5
        if id_count >= 2:
            test_case_passed += 1
            testcases[5][1] = 1   
        testcases[5].append(f"expected 2 id selectors, found {id_count}")
        
        # Test case #6
        if font_count >= 2:
            test_case_passed += 1
            testcases[6][1] = 1   
        testcases[6].append(f"expected 2 font properties, found {font_count}")
        
        # Test case #7
        if color_count >= 2:
            test_case_passed += 1
            testcases[7][1] = 1   
        testcases[7].append(f"expected 2 color properties, found {color_count}")
        
        # Test case #8
        if border_count >= 1:
            test_case_passed += 1
            testcases[8][1] = 1   
        testcases[8].append(f"expected 1 border property, found {font_count}")
        
        # Test case #9
        if font_count >= 1:
            test_case_passed += 1
            testcases[9][1] = 1   
        testcases[9].append(f"expected 1 flex display, found {font_count}")
        
        testcases["passed"] = test_case_passed
        testcases["submission"] = url

        a = Attempt.objects.create(user=request.user, data=testcases, pset=2)

        print(results)
        print(testcases)

        return redirect(f"/attempt/{a.id}")
    else:
        return render(request, "webdev/pset2.html")

@login_required(login_url='/github/authorize')
def pset3(request):
    if request.method == "POST":
        results = {1: ["function sumDouble is defined", 0], 2: ["function sumDouble accept 2 arguments", 0], 3: ["sumDouble(1, 2) -> 3", 0], 4: ["sumDouble(3, 2) -> 5", 0], 5: ["sumDouble(2, 2) -> 8", 0], 6: ["sumDouble(-1, 0) -> -1", 0], 7: ["sumDouble(3, 3) -> 12", 0], 8: ["sumDouble(0, 0) -> 0", 0], 9: ["sumDouble(0, 1) -> 1", 0], 10: ["sum_double(3, 4) -> 7", 0], "passed": 0, "all": 10}
        content = request.FILES['file'].read().decode("utf-8")
        test_case_passed = 0

        func = js2py.eval_js(content + " var exist= typeof sumDouble === 'function'")        
        if func == True:
            test_case_passed += 1
            results[1][1] = 1
            args_needed = js2py.eval_js(content + " var args=sumDouble.length")        
            if args_needed == 2:
                test_case_passed += 1
                results[2][1] = 1
                
                func = js2py.eval_js(content)  
                if func(1, 2) == 3:
                    results[3][1] = 1
                    test_case_passed += 1
                results[3].append(f"expected output 3, outputed {func(1, 2)} instead")

                if func(3, 2) == 5:
                    results[4][1] = 1
                    test_case_passed += 1
                results[4].append(f"expected output 5, outputed {func(3, 2)} instead")
                
                if func(2, 2) == 8:
                    results[5][1] = 1
                    test_case_passed += 1
                results[5].append(f"expected output 8, outputed {func(2, 2)} instead")

                if func(-1, 0) == -1:
                    results[6][1] = 1
                    test_case_passed += 1
                results[6].append(f"expected output 3, outputed {func(-1, 0)} instead")

                if func(3, 3) == 12:
                    results[7][1] = 1
                    test_case_passed += 1
                results[7].append(f"expected output 12, outputed {func(3, 3)} instead")

                if func(0, 0) == 0:
                    results[8][1] = 1
                    test_case_passed += 1
                results[8].append(f"expected output 0, outputed {func(0, 0)} instead")

                if func(0, 1) == 1:
                    results[9][1] = 1
                    test_case_passed += 1
                results[9].append(f"expected output 1, outputed {func(0, 1)} instead")

                if func(3, 4) == 7:
                    results[10][1] = 1
                    test_case_passed += 1
                results[10].append(f"expected output 7, outputed {func(3, 4)} instead")

            else:
                results[2].append(f"expect 2 arguments, found {args_needed}")
        else:
            results[1].append("Function sumDouble is undefined")
        
        results["passed"] = test_case_passed
        # results["submission"] = url

        a = Attempt.objects.create(user=request.user, data=results, pset=3)
        return redirect(f"/attempt/{a.id}")
    else:
        return render(request, "webdev/pset3.html")

@login_required(login_url='/github/authorize')
def pset4(request):
    if request.method == "POST":
        results = {1: ["Website has two input fields with id r and id h", 0], 2: ["Website has a button with id button", 0], 3: ["Website has a div with id result", 0], 4: ["Input 2 for radius and 3 for height, output 37.7", 0], 5: ["Input 3 for radius and 4 for height, output 113.1", 0], 6: ["Input 4.5 for radius and 5.5 for height, output 349.9", 0], 7: ["Random Test #1", 0], 8: ["Random Test #2", 0], 9: ["Random Test #3", 0], "passed": 0, "all": 9}
        test_cases_passed = 0

        url = request.POST["url"]
        driver = load_chrome_driver() 
        driver.get(url)
        try:
            r = driver.find_element(by.ID, "r")
            h = driver.find_element(by.ID, "h")
            results[1][1] = 1
            test_cases_passed += 1
            try:
                button = driver.find_element(by.ID, "button")
                results[2][1] = 1
                test_cases_passed += 1

                try:
                    res = driver.find_element(by.ID, "result")
                    results[3][1] = 1
                    test_cases_passed += 1


                    r.clear()
                    h.clear()
                    r.send_keys("2")
                    h.send_keys("3")
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == "37.7":
                        results[4][1] = 1
                        test_cases_passed += 1
                    results[4].append(f"Expected 37.7, found {res}")

                    r.clear()
                    h.clear()
                    r.send_keys("3")
                    h.send_keys("4")
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == "113.1":
                        results[5][1] = 1
                        test_cases_passed += 1
                    results[5].append(f"Expected 113.1, found {res}")
                    
                    r.clear()
                    h.clear()
                    r.send_keys("4.5")
                    h.send_keys("5.5")
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == "349.9":
                        results[6][1] = 1
                        test_cases_passed += 1
                    results[6].append(f"Expected 37.7, found {res}")
                    
                    r.clear()
                    h.clear()
                    radius, height, volumn = cylinder_volume()
                    r.send_keys(str(radius))
                    h.send_keys(str(height))
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == str(volumn):
                        results[7][1] = 1
                        test_cases_passed += 1
                    results[7].append(f"Expected {volumn} with r {radius} and h {height}, found {res}")

                    r.clear()
                    h.clear()
                    radius, height, volumn = cylinder_volume()
                    r.send_keys(str(radius))
                    h.send_keys(str(height))
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == str(volumn):
                        results[8][1] = 1
                        test_cases_passed += 1
                    results[8].append(f"Expected {volumn} with r {radius} and h {height}, found {res}")

                    r.clear()
                    h.clear()
                    radius, height, volumn = cylinder_volume()
                    r.send_keys(str(radius))
                    h.send_keys(str(height))
                    button.click()
                    res = driver.find_element(by.ID, "result").text
                    if res == str(volumn):
                        results[9][1] = 1
                        test_cases_passed += 1
                    results[9].append(f"Expected {volumn} with r {radius} and h {height}, found {res}")

                except NoSuchElementException:
                    results[3].append("Can't find element with id result")

            except NoSuchElementException:
                results[2].append("Can't find element with id button")

        except NoSuchElementException: 
            results[1].append("Can't find element with id r or h")
    
        results["passed"] = test_cases_passed
        results["submission"] = url

        a = Attempt.objects.create(user=request.user, data=results, pset=4)
        return redirect(f"/attempt/{a.id}")
    else:
        return render(request, "webdev/pset4.html")

@login_required(login_url="/github/authorize")
def pset5(request):
    if request.method == "POST":
        results = {1: ["Website has an input text with id city", 0], 2: ["Website has a button with id button", 0], 3: ["Website has a h3 tag with id location", 0], 4: ["Website has a h3 tag with id condition", 0], 5: ["Website has an img tag with id img", 0], 6: ["Website has a h3 tag with id temp", 0], 7: ["location update correctly with input London", 0], 8: ["condition update correctly with input London", 0], 9: ["img update correctly with input London", 0], 10: ["temp update correctly with input London", 0], "passed": 0, "all": 10}
        test_cases_passed = 0
        url = request.POST["url"]

        url = request.POST["url"]
        driver = load_chrome_driver() 
        driver.get(url)

        try:
            city = driver.find_element(by.ID, "city")
            test_cases_passed += 1
            try:
                button = driver.find_element(by.ID, "button")
                test_cases_passed += 1
                try:
                    location = driver.find_element(by.ID, "location")
                    test_cases_passed += 1
                    try:
                        condition = driver.find_element(by.ID, "condition")
                        test_cases_passed += 1
                        try:
                            img = driver.find_element(by.ID, "img")
                            test_cases_passed += 1
                            try:
                                temp = driver.find_element(by.ID, "temp")
                                test_cases_passed += 1

                                city.send_keys("London")
                                button.click()
                                location = driver.find_element(by.ID, "location").text
                                condition = driver.find_element(by.ID, "condition").text
                                img = driver.find_element(by.ID, "img").get_attribute("src")
                                temp = driver.find_element(by.ID, "temp").text

                                _location, _condition, _img, _temp = get_weather_info("London")

                                if _location == location:
                                    test_cases_passed += 1
                                    results[7][1] = 1
                                results[7].append(f"expect {_location}, got {location}")

                                if _condition == condition:
                                    test_cases_passed += 1
                                    results[8][1] = 1
                                results[8].append(f"expect {_condition}, got {condition}")

                                if _img == img:
                                    test_cases_passed += 1
                                    results[9][1] = 1
                                results[9].append(f"expect {_img}, got {img}")

                                if _temp == temp:
                                    test_cases_passed += 1
                                    results[10][1] = 1
                                results[10].append(f"expect {_temp}, got {temp}")

                            except NoSuchElementException:
                                results[6].append("Can't find element with id temp")
                        except NoSuchElementException:
                            results[5].append("Can't find element with id img")
                    except NoSuchElementException:
                        results[4].append("Can't find element with id condition")
                except NoSuchElementException:
                    results[3].append("Can't find element with id location")
            except NoSuchElementException:
                results[2].append("Can't find element with id button")
        except NoSuchElementException:
            results[1].append("Can't find element with id city")

        results["passed"] = test_cases_passed
        results["submission"] = url

        a = Attempt.objects.create(user=request.user, data=results, pset=5)
        return redirect(f"/attempt/{a.id}")
    
    else:
        return render(request, "webdev/pset5.html")

@login_required(login_url='/github/authorize/')
def view_attempt(request, attempt_id):
    attempt = Attempt.objects.get(user=request.user, id=attempt_id)
    return render(request, "webdev/view-attempt.html", {
        "attempt": attempt
    })

@login_required(login_url='/github/authorize/')
def gradebook(request):
    pset1 = {"data": {"passed": 0, "all": 9}}
    pset2 = {"data": {"passed": 0, "all": 9}}
    pset3 = {"data": {"passed": 0, "all": 10}}
    pset4 = {"data": {"passed": 0, "all": 9}}
    pset5 = {"data": {"passed": 0, "all": 10}}

    if len(list(Attempt.objects.filter(user=request.user, pset=1))) != 0:
        pset1 = Attempt.objects.filter(user=request.user, pset=1)[::-1][0]
    if len(list(Attempt.objects.filter(user=request.user, pset=2))) != 0:
        pset2 = Attempt.objects.filter(user=request.user, pset=2)[::-1][0]
    if len(list(Attempt.objects.filter(user=request.user, pset=3))) != 0:
        pset3 = Attempt.objects.filter(user=request.user, pset=3)[::-1][0]
    if len(list(Attempt.objects.filter(user=request.user, pset=4))) != 0:
        pset4 = Attempt.objects.filter(user=request.user, pset=4)[::-1][0]
    if len(list(Attempt.objects.filter(user=request.user, pset=5))) != 0:
        pset5 = Attempt.objects.filter(user=request.user, pset=5)[::-1][0]
    
    return render(request, "webdev/gradebook.html", {
        "pset1": pset1,
        "pset2": pset2,
        "pset3": pset3,
        "pset4": pset4,
    })

def get_weather_info(city):
    data = requests.get(f"https://api.weatherapi.com/v1/current.json?key=e6c594e2589a4528a3114629221807&q={city}").json()
    return data["location"]["name"], data["current"]["condition"]["text"], data["current"]["condition"]["icon"], data["current"]["temp_c"]
