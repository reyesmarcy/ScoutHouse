import requests
import os
import xmltodict 

# from zillowresults import *

ZWS_ID = os.environ.get("ZILLOW_ID")

BASE_URL = 'http://www.zillow.com/webservice'


def getSearchResults(address, citystatezip):
    
    url = f'{BASE_URL}/GetSearchResults.htm'
    try: 

      parameters = {'zws-id': ZWS_ID,
                    'address': address,
                    'citystatezip': citystatezip}

      response = requests.get(url, params=parameters)
      print("LOOK AT ME!!!!")
      print(response)
      data = response.text
      resp_dict = xmltodict.parse(data)

      results = resp_dict['SearchResults:searchresults']['response']['results']['result']

      return results

    except requests.exceptions.RequestException as e:
        flash('Please enter a valid address.')
        return redirect("/")

def getRegion(state, city):

    url = f'{BASE_URL}/GetRegionChildren.htm'

    parameters = {'zws-id': ZWS_ID,
                  'state': state,
                  'city': city,
                  'childtype': 'neighborhood'}

    response = requests.get(url, params=parameters)

    data = response.text
    results = xmltodict.parse(data, dict_constructor=dict)

    return results['RegionChildren:regionchildren']['response']['list']['region']

# class ZillowApi(object):
#     """ NOTE: to create an instance of the zillowapi.ZillowApi class:
#         >>> import zillowapi
#         >>> api = zillowapi.ZillowApi()
#     """

#     def __init__(self):
#         self.base_url = "http://www.zillow.com/webservice"

#     def getZestimate(self, zws_id, address, citystatezip):

#         url = f'(self.base_url)/GetSearchResults.htm'

#         parameters = {'zws-id': os.environ.get("ZILLOW_ID"),
#                       'address': address,
#                       'citystatezip': citystatezip}

    
#         response = requests.get(url, params=parameters)
#         data = response.text

#         resp_dict = xmltodict.parse(data)

#         place = Place()

#         Place.set_data()



    
#     zest = new_dict['SearchResults:searchresults']['response']['results']['result']['zestimate']['amount']['#text']
#     zestimate = int(zest)


