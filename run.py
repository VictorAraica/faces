from urllib.request import urlretrieve
import json
import requests
import time
import os


lastrun = int(time.time()) - os.path.getmtime("./site/index.html")
print(lastrun)

if lastrun < 73000:
    gsearch = 'https://api.github.com/search/users?q=followers:1..10000000&per_page=100'
    searches = [gsearch, '%s%s' % (gsearch, '&page=2')]
    loads = []
    for x in searches:
        page = requests.get(x)
        loads.append(json.loads(page.content))

    #
    page = """<!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>Top Github Faces</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
        <style>
            .container {max-width: 1900px;}      
            .row {float: left;}
            body {line-height: 0;}
            col-md-4 {width: 374px; height: 374px;}
            div.row {width: 374px; height: 374px;}
            img {width: 374px; height: 374px;}
        </style>
         <!-- Global Site Tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-106852135-1"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments)};
          gtag('js', new Date());        
          gtag('config', 'UA-106852135-1');
        </script>
      </head>
      <body>
        <div class="container">"""
    for i, x in enumerate(loads):
        for j, person in enumerate(x['items']):
            k = i * 100 + j
            print(k, person)

            localtime = os.path.getmtime("./site/images/faces/%s.png" % person['login'])
            remotetime = os.system("curl --silent --head %s | awk '/^Last-Modified/{print $0}' | sed 's/^Last-Modified: //'" % (person['avatar_url']))

            if localtime - remotetime < 0:
                print('remote newer')
                urlretrieve(person['avatar_url'], "./site/images/faces/%s.png" % person['login'])

            page += """<div class="row">
               <div class="col-md-4">
                <div class="thumbnail">
                  <a href="{profile}" target="_blank">
                    <img src="{filename}" alt="{user}" title="{user}">
                  </a>
                </div>
              </div>      
            </div>
            """.format(profile=person['html_url'], filename="./images/faces/%s.png" % person['login'],
                       user=person['login'], )
    page += """
        </div>       
        <!-- Latest compiled and minified JavaScript -->
        <script src="bootstrap/js/jquery.min.js"></script>
        <script src="bootstrap/js/popper.min.js"></script> 
        <script src="bootstrap/js/bootstrap.min.js"></script>    
      </body>
    </html>
    """
    target = open('site/index.html', 'w')
    target.write(page)
    target.close()

else:
    print("wait")


