# -*- coding: utf-8 -*-
"""
Created on Wed Oct 08 15:18:12 2014

@author: Talmo
"""

import requests
import json
import urllib2

# Base API URL
API_URL = 'http://api.metagenomics.anl.gov'


def validate_mg_id(mg_id):
    """
    This function ensures that the metagenome ID follows a standard MG-RAST
    format, including the mgm prefix.
    
    Args:
        mg_id: MG-RAST metagenome ID to be tested
        
    Returns:
        mg_id: Validated ID of the format 'mgm#######.#'
    """
    if type(mg_id) != str:
        mg_id = str(mg_id)
    if mg_id[0:3] != 'mgm':
        mg_id = 'mgm' + mg_id
    return mg_id


def get_download_links(mg_id, query=True):
    """
    Returns the links to download files associated with a metagenome.
    
    Args:
        mg_id: The MG-RAST ID of the metagenome
        query: If True, queries the API for the links, otherwise returns the
            links without querying. If False, the returned links may not
            actually exist (default = True).
            
    Returns:
        links: dictionary of 'file_id': 'url' pairs. The file_id is usually
            the stage #.1
            
    Example:
        >>> links = get_download_links('mgm4508947.3')
        >>> links
        {'050.1': 'http://api.metagenomics.anl.gov/download/mgm4508947.3?file=050.1',
         ...
         '700.1': 'http://api.metagenomics.anl.gov/download/mgm4508947.3?file=700.1'}

    """
    
    # Make sure we have the correct format of the ID ('mgm...')
    mg_id = validate_mg_id(mg_id)
    
    if query:
        # Query the API for the links
        query_url = API_URL + '/download/' + mg_id;
        r = requests.get(query_url)
        data = json.loads(r.content)['data']
        links = {str(link['file_id']): str(link['url']) for link in data}

    else:
        # Assume the links follow a format
        file_ids = ['050.1', '100.1', '100.2', '150.1', '150.2', '299.1', '350.1', '425.1', '440.1', '440.2', '450.1', '550.1', '550.2', '650.1', '700.1']
        links = {file_id: API_URL + '/download/' + mg_id + '?file=' + file_id for file_id in file_ids}
        
    return links


def download(url, destination):
    req = urllib2.Request(url)
    #req.add_header("Referer", best_sub["url"])
    file_data = urllib2.urlopen(req).read()
    return file_data