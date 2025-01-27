import configuration
import requests
import data

def service_CardList_post(data, token):
    url = configuration.url_baas+configuration.url_CardList
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def service_getList_get(data, token):
    url = configuration.url_baas+configuration.url_getList
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def service_getListBalance_get(data, token):
    url = configuration.url_baas+configuration.url_getListBalance
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def service_deposits_get(params, token):
    url = configuration.url_baas+configuration.url_deposits
    headers = {"Authorization": f"Bearer {token}",
        "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return response

def service_Accounts_get(params, token):
    url = configuration.url_baas+configuration.url_Accounts
    headers = {"Authorization": f"Bearer {token}",
        "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return response

def service_clientsFull_get(params, token):
    url = configuration.url_baas+configuration.url_clientsFull
    headers = {"Authorization": f"Bearer {token}",
        "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return response