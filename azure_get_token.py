import os
import urllib.parse
import requests
from config import UserConfig
from fastapi import APIRouter
from fastapi.requests import Request
router = APIRouter()

client_id = UserConfig.client_id
tenant_id = UserConfig.tenant_id
redirect_uri = UserConfig.redirect_uri
authorization_code = UserConfig.authorization_code
client_secret = UserConfig.client_secret

@router.get('/get-authority')
def get_authority_url():
    redirect_uri = 'http://localhost'
    scope = 'https://graph.microsoft.com/.default offline_access'
    authorization_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'response_mode': 'query',
        'scope': scope,
        'state': '654321'  # Optional parameter, used to prevent Cross-Site Request Forgery (CSRF) attacks
    }

    auth_url = f'{authorization_url}?{urllib.parse.urlencode(params)}'
    print('open the following URL in browser and authorize:', auth_url)
    return {
        'auth_url':auth_url 
    } 

@router.get('/get_token')
def get_token():
    scope = 'https://graph.microsoft.com/.default'
    authorization_code = ''

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'scope': scope
    }

    response = requests.post(token_url, data=data)
    token_response = response.json()
    refresh_token=""

    if 'access_token' in token_response:
        access_token = token_response['access_token']
        refresh_token = token_response.get('refresh_token')
        print('Access Token:', access_token)
        print('Refresh Token:', refresh_token)
    else:
        print('Error:', token_response.get('error_description'))

    return {
        'access_token':access_token,
        'refresh_token':refresh_token
    }

@router.get('/update_refresh_token')
def update_refresh_token(requset: Request):
    refresh_token = requset.query_params['refresh_token']
    scope = 'https://graph.microsoft.com/.default offline_access'

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': scope
    }

    response = requests.post(token_url, data=data)
    token_response = response.json()

    if 'access_token' in token_response:
        new_access_token = token_response['access_token']
        new_refresh_token = token_response.get('refresh_token')
        print('New Access Token:', new_access_token)
        print('New Refresh Token:', new_refresh_token)
    else:
        print('Error:', token_response.get('error_description'))

    return {
        'access_token':new_access_token,
        'refresh_token':new_refresh_token
    }