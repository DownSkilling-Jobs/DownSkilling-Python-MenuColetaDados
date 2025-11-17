import regex as re
import datetime as dt

regex_pattern_date01 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
regex_pattern_date04 = r'[0-9]{4}/[0-9]{2}/[0-9]{2}'
regex_pattern_date02 = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'
regex_pattern_date03 = r'[0-9]{2}-[0-9]{2}-[0-9]{4}'

dias_da_semana = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

def request_date(texto):
    date_input = input(f"\nInsira a data de {texto} (no formato AAAA-MM-DD): ")

    try:
        if re.fullmatch(regex_pattern_date01, date_input):
            print(f"Data '{date_input}' está no formato AAAA-MM-DD.")
            data = dt.datetime.strptime(date_input, "%Y-%m-%d").date()
        elif re.fullmatch(regex_pattern_date04, date_input):
            print(f"Data '{date_input}' está no formato AAAA/MM/DD.")
            data = dt.datetime.strptime(date_input, "%Y/%m/%d").date()
        elif re.fullmatch(regex_pattern_date02, date_input):
            print(f"Data '{date_input}' está no formato DD/MM/AAAA.")
            data = dt.datetime.strptime(date_input, "%d/%m/%Y").date()
        elif re.fullmatch(regex_pattern_date03, date_input):
            print(f"Data '{date_input}' está no formato DD-MM-AAAA.")
            data = dt.datetime.strptime(date_input, "%d-%m-%Y").date()
        else:
            print("Valor inserido Invalido. Tente novamente.\n")
            return request_date(texto)
    except ValueError as e:
        print('Valor inserido invalido. Tente novamente.\n')
        print(f"Error parsing date: {e}")
        return request_date(texto)
    else:
        weekday = dias_da_semana[data.weekday()]
        print(f"O dia da semana é: {weekday}")
        return data

if __name__ == "__main__":
    dataE = request_date('emissão')