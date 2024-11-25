import requests
import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

# Pegar o token do arquivo .env
hubspot_token = os.getenv('HUBSPOT_TOKEN')

# Configurações gerais
HEADERS = {
    "Authorization": f"Bearer {hubspot_token}",
    "Content-Type": "application/json"
}
PROPERTY_NAME = "today_s_date"


# Função para atualizar registros de um objeto
def update_hubspot_object(object_type, use_iso_datetime=False):
    SEARCH_URL = f"https://api.hubapi.com/crm/v3/objects/{object_type}/search"
    UPDATE_URL = f"https://api.hubapi.com/crm/v3/objects/{object_type}/"

    # Definir o formato da data com base no objeto
    if use_iso_datetime:
        current_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    else:
        current_date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    # Buscar registros do objeto
    search_payload = {
        "limit": 100,  # Máximo de registros por chamada
        "properties": [PROPERTY_NAME]  # Apenas a propriedade que será atualizada
    }

    response = requests.post(SEARCH_URL, headers=HEADERS, json=search_payload)

    if response.status_code == 200:
        data = response.json()
        total_records = data.get("total", 0)
        records = data.get("results", [])

        print(f"Total de registros encontrados no objeto {object_type}: {total_records}")

        # Atualizar cada registro
        for record in records:
            record_id = record["id"]
            update_payload = {
                "properties": {
                    PROPERTY_NAME: current_date
                }
            }
            update_response = requests.patch(f"{UPDATE_URL}{record_id}", headers=HEADERS, json=update_payload)

            if update_response.status_code == 200:
                print(f"Propriedade {PROPERTY_NAME} atualizada com sucesso para o ID {record_id}")
            else:
                print(f"Erro ao atualizar o ID {record_id}: {update_response.status_code}, {update_response.text}")

    else:
        print(f"Erro ao buscar os registros do objeto {object_type}: {response.status_code}, {response.text}")


# Executar atualizações para cada objeto
if __name__ == "__main__":
    # Atualizar `customers` com data no formato ISO
    update_hubspot_object("customers", use_iso_datetime=True)

    # Atualizar `squads` com data no formato YYYY-MM-DD
    update_hubspot_object("squads", use_iso_datetime=False)

    # Atualizar `p6884828_purchased_services` com data no formato YYYY-MM-DD
    update_hubspot_object("p6884828_purchased_services", use_iso_datetime=False)
