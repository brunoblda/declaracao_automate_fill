"""Classe responsavel pela automacao"""
import time
import pyautogui
import requests
from utils_layer import utils


class DeclaracaoCtcAutomate:
    """Classe responsavel pela automacao"""

    def __init__(self, dict_person, mouse_coordenates) -> None:
        self.mouse_coordenates = mouse_coordenates
        self.dict_person = dict_person
        self.coordenates_mouse_list = utils.mouse_coordenates_to_list(
            self.mouse_coordenates
        )

    def printar(self):
        """Printa as variaveis iniciais"""
        print(self.dict_person)
        print(self.coordenates_mouse_list)

    def execute_substitution(self, index, frase):
        """Realiza a substituicao dos campos"""
        pyautogui.click(
            self.coordenates_mouse_list[index][0], self.coordenates_mouse_list[index][1]
        )
        pyautogui.press("enter")
        pyautogui.tripleClick(
            self.coordenates_mouse_list[index][0], self.coordenates_mouse_list[index][1]
        )
        pyautogui.write(frase)

    def execute_automate(self):
        """Executa a automacao na declaracao no SEI"""
        try:
            self.dict_person["END RESID-UF"] = utils.get_uf_api(
                self.dict_person["END RESID-CEP"]
            )
        except requests.exceptions.Timeout:
            self.dict_person["END RESID-UF"] = "NF"
        except KeyError:
            self.dict_person["END RESID-UF"] = "NF"
        except requests.exceptions.ConnectionError:
            self.dict_person["END RESID-UF"] = "NF"

        date_orgao_spub_equal = utils.compare_date_orgao_spub(
            self.dict_person["DIA OCOR INGR ÓRGÃO EV"], self.dict_person["MÊS ING SPUB"]
        )
        if date_orgao_spub_equal:
            self.dict_person["DIA OCOR INGR ÓRGÃO EV"] = utils.date_mask(
                self.dict_person["DIA OCOR INGR ÓRGÃO EV"]
            )
        else:
            self.dict_person["DIA OCOR INGR ÓRGÃO EV"] = "XX/XX/XXXX"
        time.sleep(5)
        index_coordenates_mouse_initial = 1
        pyautogui.PAUSE = 1
        pyautogui.click(
            self.coordenates_mouse_list[0][0], self.coordenates_mouse_list[0][1]
        )
        frases = [
            f"NOME DO(A) SERVIDOR(A): {self.dict_person['NOME SERVIDOR']}",
            self.dict_person["IDENTIDADE-NÚMERO"],
            f"{self.dict_person['IDENTIDADE-ÓRGÃO EXP']}-"
            f"{self.dict_person['IDENTIDADE-UF ÓRGÃO EXP']}",
            self.dict_person["IDENTIDADE-DATA EXP"],
            utils.cpf_mask(self.dict_person["CPF SERVIDOR"]),
            utils.eleitor_mask(self.dict_person["TÍTULO ELEITOR"]),
            self.dict_person["VÍNCULO SERVIDOR"][6:],
            utils.date_mask(self.dict_person["DATA NASCIMENTO SERVIDOR"]),
            self.dict_person["NOME MÃE"],
            f"{self.dict_person['END RESID-LOGRADOURO']} NUMERO: "
            f"{self.dict_person['END RESID-NÚMERO']} COMPLEMENTO: "
            f"{self.dict_person['END RESID-COMPLEMENTO']}",
            f"{self.dict_person['END RESID-BAIRRO']} - "
            f"{self.dict_person['END RESID-MUNICÍPIO']} - "
            f"{self.dict_person['END RESID-UF']}",
            f"CEP: {utils.cep_mask(self.dict_person['END RESID-CEP'])}",
            f"Cargo em que se aposentou: {self.dict_person['CARGO']}",
            f"Data de Ingresso no servico publico (sem interrupcao): "
            f"{self.dict_person['DIA OCOR INGR ÓRGÃO EV']}",
            f"Data da Aposentadoria: {utils.date_mask(self.dict_person['DIA APOSENTADORIA'])}",
            f"NIT: {utils.nit_mask(self.dict_person['PIS PASEP'])}",
        ]
        for i, frase in enumerate(frases):
            self.execute_substitution(i + index_coordenates_mouse_initial, frase)
