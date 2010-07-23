import urllib2, socket
import json

#CONFIG
servers = ["http://10.112.121.206:9080", "http://ci.dev.int.realestate.com.au:8080"]
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
    "spire (master)"
]


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
			margin: 10px;
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
			background:#63af10;
		}
		
		.building {
			background: blue;
		}
		
		.failure{
			background: #bd2111;
		}

        .undefined {
            background: #BBB;
        }
		
        .offline {
			background: white;
			color: #bd2111;
			border: 5px solid #bd2111;
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
    if color.find("aborted") > -1:
        return "undefined"
    if color == "blue":
        return "success"
    if color == "red":
        return "failure"

def create_html_element(name, status):
    html = "<article class=\"[status]\"><header><h1>[name]</h1></header></article>"
    return html.replace("[name]", name).replace("[status]", hudson_color_to_css(status))

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
                o = json.loads(urllib2.urlopen(urllib2.Request(server + "/api/json")).read())
                jobs.extend(o['jobs'])
            except:
                offline_servers.append(server.replace("http://", "").split(":")[0])

        html_elements = ""
        for job in jobs:
            if job['name'] not in exclude:
                html_elements += create_html_element(job['name'], job['color'])
        for os in offline_servers:
            html_elements += create_html_element("OFFLINE:<br />" + os, "offline")
        write_html_file(template.replace("[content]", html_elements))
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
