from os import environ

import pandas as pd
import requests
import xmltodict


def fetch_reference_code(token: str, query_id: str) -> str:
    '''Requests for a reference code that is required to get the data of a specified flex query.

    Args:
        token (str): Token generated in web portal settings.
        query_id (str): Query ID generated when the flex query is created in the web portal.

    Returns:
        str: Reference code 
    '''
    url = ('https://gdcdyn.interactivebrokers.com'
           f'/Universal/servlet/FlexStatementService.SendRequest?'
           f't={token}&q={query_id}&v=3')

    response = requests.get(url)
    xml_dict = xmltodict.parse(response.text)
    reference_code = xml_dict['FlexStatementResponse']['ReferenceCode']
    return reference_code


def fetch_data(token: str, reference_code: str) -> pd.DataFrame:
    '''Returns the trade data in a form of pandas dataframe.

    Args:
        token (str): Token generated in web portal settings.
        reference_code (str): Reference code provided after the initial response.

    Returns:
        pd.DataFrame: Trades data
    '''
    url = ('https://ndcdyn.interactivebrokers.com'
           f'/AccountManagement/FlexWebService/GetStatement?'
           f't={token}&q={reference_code}&v=3')

    response = requests.get(url)
    xml_dict = xmltodict.parse(response.text)
    query = xml_dict['FlexQueryResponse']
    statement = query['FlexStatements']['FlexStatement']
    trades = statement['Trades']['Trade']
    df = pd.DataFrame(trades)
    return df


if __name__ == '__main__':
    # Go to web portal settings to generate flex token
    # Query Id is available when Flex Query is created
    token = environ['FLEX_TOKEN']
    query_id = environ['FLEX_QUERY_ID']

    # Reference code is generated upon successful request
    reference_code = fetch_reference_code(token, query_id)
    trades_df = fetch_data(token, reference_code)

    # Exclude entries where subcategory is empty
    trades_df = trades_df[trades_df['@subCategory'] != '']

    if trades_df is not None:
        print(trades_df)
    else:
        print('Failed to retrieve data from the API.')
