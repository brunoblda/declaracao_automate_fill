"""Modulo de funcoes uteis"""
import csv
import datetime
import os.path
import requests

def spreadsheet_to_list_dict(name_file):
    """Transforma a planilha csv em uma lista de dicionarios"""
    # with open(name_file, "r", encoding="utf-16 LE") as f:
    with open(name_file, "r", encoding="utf-16") as file:
        file_dict = csv.DictReader(file)
        list_file_dict = list(file_dict)
    return list_file_dict

def mouse_coordenates_to_list(name_file):
    """Transforma o arquivo de coordenadas do 
    mouse em uma lista"""
    with open(name_file, "r", encoding="utf-8") as file:
        file_list = file.readlines()
        file_list = [line.rstrip() for line in file_list]
        file_list = [line.split(". ") for line in file_list]
        file_list = [line[1].split(",") for line in file_list]
        file_list = [(int(line[0][1:]),int(line[1][1:-1])) for line in file_list]
    return file_list

def find_servidor(name, spread_sheet):
    """Encontra servidor na planilha"""
    names_list = []
    for line in spread_sheet:
        if name.lower() in line["NOME SERVIDOR"].lower():
            names_list.append(line)
    return names_list 

def find_servidor_exactily(name, spread_sheet):
    """Encontra servidor na planilha"""
    for line in spread_sheet:
        if name.lower() == line["NOME SERVIDOR"].lower():
            return line
    return None

def cpf_mask(cpf):
    """Retorna um cpf formatado"""
    cpf_formated = cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]
    return cpf_formated

def nit_mask(nit):
    """Retorna um nit formatado"""
    nit_formated = nit[:1] + "." + nit[1:4] + "." + nit[4:7] + "." + nit[7:10] + "-" + nit[10:]
    return nit_formated

def eleitor_mask(eleitor):
    """Retorna um titulo de eleitor formatado"""
    eleitor_formated = eleitor[1:5] + " " + eleitor[5:9] + " " + eleitor[9:]
    return eleitor_formated

def cep_mask(cep):
    """Retorna um titulo de eleitor formatado"""
    cep_formated = cep[:5] + "-" + cep[5:]
    return cep_formated

def date_mask(date_input):
    """Retorna a data formatada em dd/MM/aaaa"""
    date_format = datetime.datetime.strptime(date_input,'%d/%m/%Y').date()
    date_formated = date_format.strftime('%d/%m/%Y')
    return date_formated

def validate_file_exist(file_name):
    """Valida se o arquivo da planilha existe"""
    if os.path.isfile(f"./{file_name}"):
        return True
    return False

def get_uf_api(cep):
    """Retorna a UF do cep da api dos correios"""
    cep_response = requests.get(f"https://viacep.com.br/ws/{cep}/json/",timeout=3)
    cep_response_json = cep_response.json()
    uf_cep = cep_response_json["uf"]
    return uf_cep

def compare_date_orgao_spub(data_orgao, data_spub):
    """Compara a data de entrada no orgao com a data de entrada no servico publico."""
    mes_nomes = { "Jan": "1", "Fev": "2", "Mar": "3", "Abr": "4", "Mai": "5", "Jun": "6",
                "Jul": "7", "Ago": "8", "Set": "9", "Out": "10", "Nov": "11", "Dez": "12"
                }
    data_spub_split = data_spub.split(" ")
    mes_escrito_spub = data_spub_split[0]
    ano_spub = data_spub_split[1]
    data_orgao_split = data_orgao.split("/")
    mes_orgao = data_orgao_split[1]
    ano_orgao = data_orgao_split[2]
    if mes_nomes[mes_escrito_spub] == mes_orgao and ano_spub == ano_orgao:
        return True
    return False
