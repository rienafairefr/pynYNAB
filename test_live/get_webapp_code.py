import os
import re
from lxml import html
import requests
import jsbeautifier
response = requests.get('http://app.youneedabudget.com')
with open('index.html', 'w', encoding='utf-8') as file_before:
    file_before.write(response.text)
parsed = html.fromstring(response.text)
for src in parsed.xpath('//script/@src'):
    url_src = str(src)
    file = url_src.rsplit('/',1)[-1]
    if file.startswith('before.'):
        before_response = requests.get(str(src))
        before_script = jsbeautifier.beautify(before_response.text)
        with open(os.path.join('web_app','before.js'),'w+',encoding='utf-8') as file_before:
            file_before.write(before_script)
        regex1 = re.compile('\s*(\d)\:\s\"appmain\"')

        regex2=None
        for line in before_script.split('\n'):
            if regex1.match(line):
                idx = regex1.match(line).groups()[0]
                regex2 = re.compile('\s*%s\:\s\"(.*)\"' % idx)
            if regex2 is not None and regex2.match(line):
                test = regex2.match(line).groups()[0]
                if test!='appmain':
                    random_id = test
                    break
        url_appmain = '/'.join(url_src.rsplit('/',1)[:-1]+['appmain.'+random_id+'.js'])
        appmain_response = requests.get(url_appmain)
        appmain_script = jsbeautifier.beautify(appmain_response.text)
        with open(os.path.join('web_app','appmain.js'),'w+',encoding='utf-8') as file_appmain:
            file_appmain.write(appmain_script)

    if file.startswith('index.'):
        script_response = requests.get(str(src))
        index_script = jsbeautifier.beautify(script_response.text)
        with open(os.path.join('web_app','index.js'),'w+',encoding='utf-8') as file_before:
            file_before.write(index_script)


pass