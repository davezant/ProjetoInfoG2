import os
import yaml
from fastapi import APIRouter, Request
from typing import Optional

router = APIRouter()

def load_credentials():
    cred_path = os.path.join(os.path.dirname(__file__), "credentials.yaml")
    if not os.path.exists(cred_path):
        raise FileNotFoundError("credentials.yaml not found in WhatsApp plugin directory.")
    with open(cred_path, "r") as f:
        creds = yaml.safe_load(f)
    return creds

def init_plugin(app):
    """
    Plugin de integração com WhatsApp.
    Espera um arquivo credentials.yaml na pasta do plugin com as credenciais necessárias.
    """
    app.include_router(router, prefix="/whatsapp", tags=["whatsapp"])

@router.get("/send")
def send_message(to: str, message: str):
    """
    Envia uma mensagem de texto via WhatsApp usando as credenciais do credentials.yaml.
    """
    try:
        creds = load_credentials()
        # Exemplo com WhatsApp Cloud API (ajuste conforme sua plataforma)
        import requests

        api_url = creds.get("api_url")
        token = creds.get("token")
        phone_number_id = creds.get("phone_number_id")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        resp = requests.post(
            f"{api_url}/v17.0/{phone_number_id}/messages",
            headers=headers,
            json=data,
            timeout=15,
        )
        return {
            "status": resp.status_code,
            "response": resp.json()
        }
    except Exception as e:
        return {"error": str(e)}
