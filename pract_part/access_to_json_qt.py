import json

with open('объемы_продукции.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Доступ к данным
project1_commodity = data['project_1']['commodity_output']
total_realized = data['total']['total_realized_output']