"""Graphical User Interface module"""
import textwrap
import PySimpleGUI as sg

class MakeWindow:
    """Classe que cria a tela"""
    def __init__(self, theme=None) -> None:
        self.theme = theme
        self.window = None

    def make_window(self):
        """Create the Graphical User Interface"""
        sg.theme(self.theme)

        text_1 = ("Automatiza o preenchimento das informações pessoais e funcionais do servidor "
                "aposentado no documento 'Declaração de Comprovação de Tempo de Serviço DIVBEN'.")

        layout_l = [[sg.T('Nome do servidor aposentado:       ',font=("", 14), pad=(0,(0,10))),
                     sg.In(key="nome_serv", font=("", 14), pad=(0,(0,10)))],
                    [sg.T('Nome do arquivo de coordenadas: ',font=("", 14), pad=(0,10)),
                     sg.In(default_text='coordenadas_mouse.txt', key="nome_arq_coordenadas",
                           font=("", 14), pad=(0,10))],
                    [sg.T('Nome do arquivo da planilha:           ',font=("", 14), pad=(0,(10,0))),
                     sg.In(default_text='ctc_inss_serv.csv', key="nome_arq_planilha", font=("", 14),
                           pad=(0,(10,0)))],
                    [sg.Button('Executar', font=("", 16), pad=(280,(30,10)), bind_return_key=True)],
                    [sg.T('', key="text_execucao", font=("", 16), justification='c', pad=(200,0))]
                ]
        # Note - LOCAL Menu element is used (see about for how that's defined)
        layout = [
                    [sg.T(textwrap.fill(text_1, 60)
                        ,pad=(0,(0,30)), font='_ 16', justification='c', expand_x=False)],
                    [sg.Col(layout_l, p=0)]
                ]

        self.window = sg.Window('Preenchimento Automático da Declaração de Tempo de Contribuição',
                                layout, finalize=True,
                        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True
                        , element_justification='c', size=(700,350))

        return self.window

class MakePopup:
    """Cria a tela de popup"""
    def __init__(self, title, text, values) -> None:
        self.title = title
        self.text = text
        self.values = values
        self.window_popup = sg.Window(self.title,
            [[sg.Text(self.text)],
            [sg.DropDown(self.values, key='-DROP-')],
            [sg.Button('OK',bind_return_key=True), sg.Cancel()]
        ], size=(300,100), finalize=True)
        self.window_popup['-DROP-'].bind("<Return>", "_Enter")

    def popup_dropdown(self):
        """Popup para dropdown dos nomes de servidores encontrados"""
        event, values = self.window_popup.read()
        if event in ('OK','-DROP-'+'_Enter'):
            return values['-DROP-']
        return None

    def popup_close(self):
        """Fecha a tela de popup"""
        self.window_popup.close()
