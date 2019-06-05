import urllib.request
import urllib.parse
import re
import json

def translate(keyword):

    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    data = {}
    data['i'] = keyword
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CL1CKBUTTON'
    data['typoResult'] = 'true'

    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url,data=data,method='POST')
    response = urllib.request.urlopen(req)

    result =  response.read().decode('utf-8')
    myjson = json.loads(result)
    # print(myjson)


    print("the translation is: ", myjson["translateResult"][0][0]["tgt"])


if '__main__' == __name__:
    while True:
        keyword = input("please insert the word: ")
        if keyword == 'q':
            break
        else:
            try:
                translate(keyword)
            except Exception as e:
                print("please enter again.....")
