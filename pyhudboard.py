import urllib2, socket, random
import json, datetime, os, sys

#CONFIG
servers = [{"url" : "http://10.112.121.206:9080", "name" : "Product"} , {"url" : "http://10.112.120.57:8080", "name" : "ci.dev.int"}]
exclude = [
    "appcmd (master)", 
    "customsearch (master)", 
    "librea (master)", 
    "libspe (master)", 
    "psadmin", 
    "reaxml (master)", 
    "rsearch (master)", 
    "rsearch (project rea1)", 
    "rsearch (quagmire)", 
    "rsearch (build2.0)",
    "spire (master)"
]

voices = ['Zarvox', 'Trinoids', 'Fred', 'Ralph', 'Princess', 'Victoria']

template = """
<!DOCTYPE html> 
<html lang="en"> 
  	<head> 
  		<meta charset="utf-8" /> 
  		<title>Build Dashboard</title> 
        <script type="text/javascript">
        setTimeout('window.location.reload()', 20000)
        </script>
  		<style>
		body {  
		  padding: 10px;  
		  margin: 0;
		  font: bold 3.5em Helvetica, Arial, sans-serif;
		  background-color: #FFF;
		}  

		/* Tell the browser to render HTML 5 elements as block */  
		section, header, footer, aside, nav, article, figure {  
		  display: block;  
		}

		/* Builds
		--------------------------------------------------------------------- */
		article {
			color: #FFF;
			float: left;
			margin: 30px;
		  	-moz-box-shadow: 5px 5px 5px #333333;
		  	-webkit-box-shadow: 5px 5px 11px #333333;
		  	-o-box-shadow: 5px 5px 11px #333333;
		  	-ms-box-shadow: 5px 5px 11px #333333;
		  	box-shadow: 5px 5px 11px #333333;
		}
		
		h1, h2, p {
			margin: 50px;
		}
		
		.success {
			background:#608204;
		}
		
		.building {
			background: #3861b6;
		}
		
		.failure{
			background: #a01208;
		}

        	.undefined {
            		background: #BBB;
        	}
		
        	.offline {
			background: white;
			color: #a01208;
			border: 15px solid #a01208;
		}
		
		.message {
            position: absolute;
            bottom: 0px;
            right: 0px;
			background: white;
			color: black;
			-moz-box-shadow: none;
                        -webkit-box-shadow: none;
                        -o-box-shadow: none;
                        -ms-box-shadow: none;
                        box-shadow: none;
			font: bold 20px Helvetica, Arial, sans-serif;
		}
		
		</style>
  </head> 
<body> 
	<section id="content">
    [content]
  	</section> 
</body>  
</html>
"""


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
    html = "<article class=\"[status]\"><header><h1>[name]</h1></header></article>"
    color = hudson_color_to_css(status)
    if color == "failure":
        if len(sys.argv) == 2 and sys.argv[1] == "voice":
            voice = voices[random.randrange(0, len(voices))]
            formatted_name = name.replace('_', ' ').replace('(', '').replace(')', '')
            os.system("say -v " + voice + " " + formatted_name + " is broken")
    return html.replace("[name]", name).replace("[status]", color)

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
	
        html_elements += create_html_element(datetime.datetime.now().strftime("%A %d/%m/%Y - %H:%M"), "message")
        write_html_file(template.replace("[content]", html_elements))
    except ValueError, (error):
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
