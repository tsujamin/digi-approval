import json
import os
import subprocess

pages = []
count = 1
for root, dirs, files in os.walk('.'):
    for page in files:
        if os.path.splitext(page)[1] != '.md':
            continue

        name = os.path.splitext(page)[0]
        result = {'pk': count,
                  "model": "flatpages.flatpage", 
                  "fields": {
                      "registration_required": False, 
                      "title": name.replace('_', ' '), 
                      "url": os.path.normpath('/' + root + '/' + name).lower() + '/',
                      "template_name": "", 
                      "sites": [1], 
                      "enable_comments": False
                    }
                  }

        count = count + 1

        generated_content = subprocess.check_output(['markdown', root + '/' + page],
                                                    stderr=subprocess.STDOUT)

        content = ("<!-- generated from %s/%s by makedocs.py. Don't edit me in flatpages! -->\n" % (root, page)) + \
          generated_content

        result['fields']['content']=content

        pages.append(result)

with open('../../src/digiapproval_project/digiapproval_project/fixtures/initial_data.json', 'w') as f:
    f.write(json.dumps(pages))
