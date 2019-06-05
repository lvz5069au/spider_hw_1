import requests
import json

def translate(keyword):
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

    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    res = requests.post(url,data=data)
    str_json = res.content.decode('utf-8')
    result = json.loads(str_json)

    print("The translation is: ", result['translateResult'][0][0]['tgt'] )


if __name__ == '__main__':
    while True:
        keyword = input("Please input the word: ")
        if keyword == 'q':
            break
        else:
            translate(keyword)
