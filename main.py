import requests
import json
import sys

# url https://arcssotest33.tcheetah09.com -d "nd=get_opportunity_detail&key=W3xhAVpaYhCcpOHYewHT6pEvWxtvAoHW&position_id=156643" -H "Content-Type: application/x-www-form-urlencoded"

def simpleGet(url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.get(url, {'headers': headers})

def getDetails(id):

    url = f'https://arcssotest33.tcheetah09.com?position_id={id}&nd=get_opportunity_detail'
    url += '&key=W3xhAVpaYhCcpOHYewHT6pEvWxtvAoHW'
    return simpleGet(url)

def getFromZipCode(zipCode):
    query = {
        'key':'W3xhAVpaYhCcpOHYewHT6pEvWxtvAoHW',
        'zip_code' : zipCode
    }
    url = 'https://arcssotest33.tcheetah09.com/?nd=get_opportunities&json_req=' + json.dumps(query)
    return simpleGet(url)

def iterateZipCodes(startZip, endZip):

    finalJson = []

    for i in range(startZip, endZip + 1):
        print(f'area code{i}')
        resp = getFromZipCode(i)
        if 'Server Error' not in resp.text:
            jsonResp = json.loads(resp.text)
            oppCount = 0
            if 'opportunities' in jsonResp:

                for opp in jsonResp['opportunities']:
                    oppCount += 1
                    print(f'Opp count: {oppCount}')
                    detResp = getDetails(opp['position_id'])
                    detJson = json.loads(detResp.text)
                    detJsonToWrite = detJson['detail']
                    detJsonToWrite['zip_code'] = i
                    finalJson.append(detJson)
    return finalJson


        

def main():
    if len(sys.argv) < 3:
        raise Exception('Not enough args. Enter start zipcode and end zipcode to iterate over.')
    startZip = int(sys.argv[1])
    endZip = int(sys.argv[2])
    finalJson = iterateZipCodes(startZip, endZip)
    outfile = open('outfile.json', 'w+')
    outfile.write(json.dumps(finalJson))
    outfile.close()


if __name__ == "__main__":
    main()


#  url = 'https://arcssotest33.tcheetah09.com?nd=get_opportunity_detail&key=W3xhAVpaYhCcpOHYewHT6pEvWxtvAoHW' # &position_id=156643'