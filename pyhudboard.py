import urllib2, socket, random
import json, datetime, os, sys
from peopleworkingonbuilds import *

#CONFIG
servers = [
  {"url" : "http://10.113.192.70:9080/view/Tests", "name" : "Product"} ,
  {"url" : "http://10.112.120.57:8080/", "name" : "ci.dev.int"}
]
exclude = [
#    "appcmd (master)",
    "customsearch (master)",
#    "libspe (master)",
    "psadmin",
#    "reaxml (master)",
    "rsearch (master)",
    "rsearch (project rea1)",
    "rsearch (quagmire)",
    "rsearch (build2.0)",
    "spire (master)", 
    "librea (rca_two)", 
    "rsearch (rca_two)" 
]

claims = get_claims_as_hash()

voices = ['Zarvox', 'Trinoids', 'Fred', 'Ralph', 'Princess', 'Victoria']

f = open("template.html", 'r')
template = f.read()
f.close()

def hudson_color_to_css(color):
    if color.find('anime') > -1:
        return "building"
    if color == "blue":
        return "success"
    if color == "red":
        return "failure"
    if color == "offline":
	return "offline"
    if color == "message":
	return "message"
    return "undefined"

def create_html_element(name, status):
    html = "<article class=\"[status]\" worker=\"[worker]\"><header><h1>[name]</h1></header></article>"
    color = hudson_color_to_css(status)
    if claims.has_key(name):
        if status == "red":
            color = color + " workedon"
            html = html.replace("[worker]", claims[name])
        elif status == "blue":
            claims.pop(name)
    #if name.find("reaxml") > -1:
    #    color = "onhold"
    #    if claims.has_key(name):
    #        color = color + " workedon"
    return html.replace("[name]", name).replace(" (master)", "").replace("[status]", color)

def write_html_file(content):
    f = open('dash.html', 'w')
    f.write(content)
    f.close()

if __name__ == '__main__':
    try:
        socket.setdefaulttimeout(5)
        offline_servers = []
        jobs = []
        for server in servers:
            try:
                o = json.loads(urllib2.urlopen(urllib2.Request(server['url'] + "/api/json")).read())
                jobs.extend(o['jobs'])
            except:
                offline_servers.append(server['name'])
        
        html_elements = ""
        for job in jobs:
            if job['name'] not in exclude:
                html_elements += create_html_element(job['name'], job['color'])
        for os in offline_servers:
            html_elements += create_html_element("OFFLINE: " + os, "offline")
        
        html_elements += create_html_element(datetime.datetime.now().strftime("%A %d/%m/%Y - %H:%M:%S"), "message")
        write_html_file(template.replace("[content]", html_elements))
        save_claims(claims)
    except Exception, (error):
        content = """<html>
                        <head>
                            <script type='text/javascript'>setTimeout('window.location.reload()', 5000)</script>
                        </head>
                        <body>
                            <h1>ERROR, LOOK INTO IT!!!</h1>
                            <h2>[error]</h2>
                        </body>
                    </html>"""
        write_html_file(content.replace("[error]", str(error)))
