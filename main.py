"""Automatiza o preenchumento de alguns campos da declaração de cts do inss"""
import PySimpleGUI as sg
import logical_layer.automation as aut
from utils_layer import utils
from gui_layer import gui

def execute_automatization(window_show):
    """Funcao que executa a automacao"""

    if not utils.validate_file_exist(window_show['nome_arq_coordenadas'].get()):
        window_show["text_execucao"].update("Coordenadas não encontradas.")

    elif not utils.validate_file_exist(window_show['nome_arq_planilha'].get()):
        window_show["text_execucao"].update("Planilha não encontrada.")

    else:
        window_show["text_execucao"].update("             Em execução.")
        window_show.minimize()
        name_servidor = window_show['nome_serv'].get()
        people_list = None
        list_person_dict = utils.spreadsheet_to_list_dict(
            window_show['nome_arq_planilha'].get())
        people_list = utils.find_servidor(name_servidor, list_person_dict)
        person_dict = None
        if people_list:
            if len(people_list) > 1:
                people_list_name = [person["NOME SERVIDOR"] for person in people_list]
                popup_select_serv = gui.MakePopup("Selecionar Servidor",
                                                    "Selecionar Servidor", people_list_name)
                name_servidor_popup = popup_select_serv.popup_dropdown()
                if name_servidor_popup:
                    person_dict = utils.find_servidor_exactily(
                        name_servidor_popup, list_person_dict)
                    popup_select_serv.popup_close()
            else:
                person_dict = people_list[0]
            if person_dict:
                automation = aut.DeclaracaoCtcAutomate(person_dict,
                                                    window_show['nome_arq_coordenadas'].get())
                automation.execute_automate()
                # automation.printar()
                window_show["nome_serv"].update(person_dict["NOME SERVIDOR"])
                window_show["text_execucao"].update("             Executado.")
            else:
                popup_select_serv.popup_close()
                window_show["text_execucao"].update("")
        else:
            window_show["text_execucao"].update("Servidor não encontrado.")

def main():
    """Funcao principal"""
    window_started = gui.MakeWindow()
    window_show = window_started.make_window()
    while True:
        # event, values = window_show.read()
        tuple_response = window_show.read()
        event = tuple_response[0]
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == "Executar":
            execute_automatization(window_show)
            window_show.TKroot.deiconify()
    window_show.close()

if __name__ == "__main__":
    main()
