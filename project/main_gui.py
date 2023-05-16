import wx, os, datetime

class SystemFunctionsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        data_atual = datetime.datetime.today()
        data_atual = data_atual.strftime('%d/%m/%Y')
        # Lista de opções
        opcoes = ['Localizar conversa pelo nome', 'Localizar conversar do dia atual {}', 'Localizar todas as conversas do whatsapp']
        # Criar caixa de diálogo
        vbox = wx.BoxSizer(wx.VERTICAL)

        for opcao in opcoes:
            radio_button = wx.RadioButton(self, label=opcao)
            vbox.Add(radio_button, 0, wx.ALL, 5)

        ok_button = wx.Button(self, wx.ID_OK, 'OK')
        cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancelar')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(ok_button, 1, wx.EXPAND|wx.ALL, 5)
        hbox.Add(cancel_button, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(vbox)
        self.Fit()

    def get_selection(self):
        # Retorna a opção selecionada
        for child in self.GetChildren():
            if isinstance(child, wx.RadioButton) and child.GetValue():
                return child.GetLabel()

        return None

# Criar aplicação wx
app = wx.App()
print(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.normpath('imagens/wapp.png')))

# Criar janela principal
frame = wx.Frame(None, wx.ID_ANY, 'Printando Whatsapp')
icon = wx.Icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.normpath('imagens/wapp.png')), wx.BITMAP_TYPE_PNG)
frame.SetIcon(icon)

# Criar botão para abrir janela de diálogo
button = wx.Button(frame, wx.ID_ANY, 'Selecionar Função do Sistema')
def on_button_click(event):
    # Criar e exibir janela de diálogo
    dialog = SystemFunctionsDialog(frame, 'Selecionar Função do Sistema')
    if dialog.ShowModal() == wx.ID_OK:
        # Obter opção selecionada
        option = dialog.get_selection()

        # Executar função do sistema correspondente
        if option == 'Abrir Terminal':
            os.system('gnome-terminal')
        elif option == 'Abrir Gerenciador de Arquivos':
            os.system('nautilus')
        elif option == 'Abrir Editor de Texto':
            os.system('gedit')

    dialog.Destroy()

button.Bind(wx.EVT_BUTTON, on_button_click)

# Exibir janela principal
frame.Show()

# Executar aplicação wx
app.MainLoop()
