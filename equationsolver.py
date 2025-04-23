import urllib.request
from bs4 import BeautifulSoup
import requests
from sympy.solvers import solve
from sympy import Symbol
import re

url = "http://jobs.mythic-beasts.com/ukaig6ua6yieHo4o"

def getSoup(url):
    #make HTTP2 request and get content
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    return(soup)

def getEquation(soup):
    #parse the content of the webpage to extract the quadratic equation
    eqn = soup.find(text=re.compile('quadratic'))
    eqnlist = eqn.find_parent().find_next_sibling().contents
    a = eqnlist[0].replace(" ","").replace("−","-")
    b = eqnlist[3].replace(" ","").replace("−","-")
    c = eqnlist[5].rsplit("=",1)[0].replace(" ","").replace("−","-")
    eqn = a+"*x**2"+b+"*x"+c
    secret = soup.find(attrs={"name":"secret"})['value']
    return(eqn, secret)

def solveEquation(eqn, symbol='x'):
    #solve the equation for x
    x = Symbol('x')
    sols = solve(eqn, symbol)
    return(sols)

def submitForm(sols, secret):
    #submit the webform using the solved values and the secret
    payload = {"x0": sols[0], "x1": sols[1], "secret": secret, "submit": "Submit"}
    r = requests.post(url, data=payload)
    return(r.text)

if __name__ == "__main__":
    eqn, secret = getEquation(getSoup(url))
    sols = solveEquation(eqn)
    print(submitForm(sols, secret))
