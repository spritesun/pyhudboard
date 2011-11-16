import urllib2, socket, random
import json, datetime, os, sys
from peopleworkingonbuilds import *
import traceback
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open("config.txt"))
items = config.items("servers")
servers=[]
for item in items:
    servers.append({"url": item[1], "name": item[0]})

exclude_builds = [a.strip() for a in config.get("exclude", "builds").split(",")]
exclude_colors = [a.strip() for a in config.get("exclude", "colors").split(",")]

font_size = config.get("font", "size")

claims = get_claims_as_hash()

def get_file_content(path): 
    f = open("templates/dashboard.html", 'r')
    content = f.read()
    f.close()
    return content

def write_file_content(path, content):
    f = open(path + ".tmp", 'w')
    f.write(content)
    f.close()
    os.rename(path + ".tmp", path)

def hudson_color_to_css_class(color):
    if color.find('anime') > -1:
        if color.find('red') > -1 or color.find('aborted') > -1:
            return "building-from-failure"
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

def get_jobs_and_offline_servers(servers):
    jobs, offline_servers = [], []
    for server in servers:
        try:
            o = json.loads(urllib2.urlopen(urllib2.Request(server['url'] + "/api/json")).read())
            jobs.extend(o['jobs'])
        except:
            offline_servers.append(server['name'])
    return jobs, offline_servers

def append_jobs_html_content(jobs, html_content=""):
    for job in jobs:
        if job['name'] not in exclude_builds and job['color'] not in exclude_colors:
            print job['color']
            html_content += create_html_element(job['name'], job['color'])
    return html_content

def append_offline_servers_html_content(servers, html_content=""):
    for os in offline_servers:
        html_content += create_html_element("OFFLINE: " + os, "offline")
    return html_content
    
def append_generation_time_html_content(html_content=""):
    html_content += create_html_element(
    "Melbourne:<br/>" +
    datetime.datetime.now().strftime("%H:%M:%S") +
    "<br/><br/>" +
    "Xi'an:<br/>" +
    (datetime.datetime.now() - datetime.timedelta(3 * 1.0 / 24)).strftime("%H:%M:%S"), "message")
    return html_content
    
def create_html_element(name, status):
    html = "<article class=\"[class]\" worker=\"[worker]\"><header><h1>[name]</h1></header></article>"
    css_class = hudson_color_to_css_class(status)
    if claims.has_key(name):
        if status.find("red") > -1 or status.find("aborted") > -1:
            css_class = css_class + " workedon"
            html = html.replace("[worker]", claims[name])
        elif status == "blue":
            claims.pop(name)
    return html.replace("[name]", name).replace(" (master)", "").replace("[class]", css_class)

def build_html(jobs, offline_servers):
    html_content = append_jobs_html_content(jobs)
    html_content = append_offline_servers_html_content(offline_servers, html_content)
    html_content = append_generation_time_html_content(html_content)
    return html_content

if __name__ == '__main__':
    try:
        socket.setdefaulttimeout(1)
        template = get_file_content("templates/dash.html")
        jobs, offline_servers = get_jobs_and_offline_servers(servers)
        html_content = build_html(jobs, offline_servers)
        write_file_content('dash.html', template.replace("[content]", html_content).replace("[font-size]", font_size))
        save_claims(claims)
    except Exception, (error):
        traceback.print_exc(file=sys.stdout)
        error_content = get_file_content("templates/error.html")
        write_file_content('dash.html', error_content.replace("[error]", str(error)))
