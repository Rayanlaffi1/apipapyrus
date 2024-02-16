# from keycloak import KeycloakAdmin
from keycloak.keycloak_admin import KeycloakAdmin
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

keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/auth/",
    username=ADMIN_USERNAME,
    password=ADMIN_PASSWORD,
    realm_name='master',
    client_id='admin-cli',
    client_secret_key=None
)
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
    

def get_client_id():
    client_id = keycloak_admin.get_client_id(CLIENT_NAME)
    return client_id
    
def get_client_secret():
    client_id = keycloak_admin.get_client_id(CLIENT_NAME)
    clients_secret = keycloak_admin.get_client_secrets(client_id)['value']
    return clients_secret

# keycloak_admin.delete_realm(REALM_NAME)
realm_data = {
    "realm": REALM_NAME,
    "enabled": True
}
keycloak_admin.create_realm(realm_data)
client_data = {
    "clientId": CLIENT_NAME,
    "enabled": True,
    "redirectUris": ["*"],
    "publicClient": True,
    "standardFlowEnabled": True,
    "implicitFlowEnabled": False,
    "directAccessGrantsEnabled": True,
    "serviceAccountsEnabled": False,
}

try:
    keycloak_admin.change_current_realm(REALM_NAME)
    client = keycloak_admin.create_client(payload=client_data)
    client_id = keycloak_admin.get_client_id(CLIENT_NAME)
    new_secret = keycloak_admin.generate_client_secrets(client_id)
    clients_secret = keycloak_admin.get_client_secrets(client_id)['value']
except Exception as e:
    print("Une erreur s'est produite lors de l'interaction avec Keycloak :", e)