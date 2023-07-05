from datetime import datetime

data_atual = datetime.now().date()
dia_atual = data_atual.day

if dia_atual <= 25:
    if data_atual.month == 1:
        data_limite = datetime(data_atual.year - 1, 12, 26).date()
    else:
        data_limite = datetime(data_atual.year, data_atual.month - 1, 26).date()
else:
    data_limite = datetime(data_atual.year, data_atual.month, 26).date()


data_atual = datetime.now().date()

mes_atual = data_atual.month
ano_atual = data_atual.year
print(mes_atual)
print(ano_atual)
print(data_limite.month)
if mes_atual == 1:
    mes_anterior = 12
    ano_anterior = ano_atual - 1
else:
    mes_anterior = mes_atual - 1
    ano_anterior = ano_atual
if mes_anterior == data_limite.month:
    mes_anterior -=1
    mes_atual -=1

data_inicio = datetime(ano_anterior, mes_anterior, 26).date()
data_fim = datetime(ano_atual, mes_atual, 25).date()

print(mes_anterior)
print(mes_atual)
print('data inicio ',data_inicio)
print('data_fim ',data_fim)