from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
import datetime

# Configurações
SUBSCRIPTION_ID = "xxxx-xxxx-xxxx-xxxx"  # Substitua pelo ID da sua assinatura
BUDGET_LIMIT = 50  # Defina um limite de custo (exemplo: 50 dólares)

# Autenticação na Azure
credential = DefaultAzureCredential()
client = CostManagementClient(credential)

# Define o período para consulta (últimos 30 dias)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Consulta os custos do Data Factory
cost_request = {
    "type": "Usage",
    "timeframe": "Custom",
    "time_period": {
        "from": start_date.strftime('%Y-%m-%d'),
        "to": end_date.strftime('%Y-%m-%d')
    },
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum"
            }
        }
    }
}

# Obter os custos
response = client.query.usage(f"/subscriptions/{SUBSCRIPTION_ID}", cost_request)
total_cost = sum(item["totalCost"] for item in response.rows)

print(f"💰 Custo total nos últimos 30 dias: ${total_cost:.2f}")

# Verifica se o custo ultrapassou o limite
if total_cost > BUDGET_LIMIT:
    print("⚠️ ALERTA: O custo ultrapassou o limite definido!")
else:
    print("✅ Tudo certo! O custo está dentro do orçamento.")
