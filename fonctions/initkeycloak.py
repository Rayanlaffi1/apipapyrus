import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")
CLIENT_NAME = os.getenv("KEYCLOAK_CLIENT_NAME")
ADMIN_USERNAME = os.getenv("KEYCLOAK_USER")
ADMIN_PASSWORD = os.getenv("KEYCLOAK_PASSWORD")

# /auth/admin/realms/papyrus/clients?clientId=papyrus-client
# /auth/admin/realms/papyrus/clients/158bd3ea-1a00-4314-98f3-ecf57028b1c4/client-secret

def get_access_token(username, password, client_id, client_secret):
    url = f"{KEYCLOAK_URL}/auth/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status() 
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print("Failed to get access token:", e)
        return None
    

def get_client_id(access_token):
    url = f"{KEYCLOAK_URL}/auth/admin/realms/{REALM_NAME}/clients?clientId="+CLIENT_NAME
    try:
        headers = {'Content-Type': 'application/json'}
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url,None, headers=headers)
        response.raise_for_status() 
        return response.json()[0]["id"]
    except requests.exceptions.RequestException as e:
        print("Failed to get client id:", e)
        return None
    
def get_client_secret(access_token,client_id):
    url = f"{KEYCLOAK_URL}/auth/admin/realms/{REALM_NAME}/clients/{client_id}/client-secret"
    try:
        headers = {'Content-Type': 'application/json'}
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url,None, headers=headers)
        response.raise_for_status() 
        return response.json()['value']
    except requests.exceptions.RequestException as e:
        print("Failed to get client id:", e)
        return None    

def keycloak_post(path, data=None):
    url = f"{KEYCLOAK_URL}/auth{path}"
    headers = {'Content-Type': 'application/json'}
    access_token = get_access_token(ADMIN_USERNAME, ADMIN_PASSWORD, "admin-cli", "")
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.post(url, json=data, headers=headers)
        try:
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None
    else:
        return None

def create_realm():
    realm_data = {
        "realm": REALM_NAME,
        "enabled": True
    }
    response = keycloak_post("/admin/realms", realm_data)
    print(response)

def create_client():
    client_data = {
        "clientId": CLIENT_NAME,
        "enabled": True,
        "redirectUris": ["*"],
        "serviceAccountsEnabled": True,
        "accessToken" : {
            "accessTokenTtl": 3600
        }
    }
    response = keycloak_post(f"/admin/realms/{REALM_NAME}/clients", client_data)
    print(response)

create_realm()
create_client()

access_token = get_access_token(ADMIN_USERNAME, ADMIN_PASSWORD, "admin-cli", "")
client_id = get_client_id(access_token)
client_secret = get_client_secret(access_token,client_id)
os.environ['KEYCLOAK_CLIENT_SECRET'] = client_secret