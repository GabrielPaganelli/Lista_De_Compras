import PySimpleGUI as sg
import smtplib
import email.message

# Main Program
layout = [
    [sg.Text("Quantidade"), sg.Text("       "), sg.Text("Produto")],
    [sg.InputText(size=(15, 15), key="TextQnt"),
     sg.InputText(key="TextProduto")],
    [sg.Button("Adicionar"), sg.Button("Enviar"), sg.Button(
        "Visualizar lista"), sg.Button("Apagar")],
    [sg.Text(key="Aviso")],
    [sg.Listbox(values=[], size=(60, 10), key="ListaDeCompras")],
]

Layout_envio = [
    [sg.Text("Digite seu email")],
    [sg.InputText(key="emailEnviar")],
    [sg.Text(key='Aviso2')],
    [sg.Button("Concluido"), sg.Button("Cancelar")]
    ]

janela = sg.Window("Lista de compras", layout)

while True:
    evento, valores = janela.read()

    if evento == sg.WIN_CLOSED:
        break

    if evento == "Adicionar":
        with open('ListaCompras.txt', 'a') as arquivo:
            QntProd = valores["TextQnt"]
            Prod = valores["TextProduto"]
            if QntProd and Prod:  # Verifica se os campos não estão vazios
                arquivo.write(QntProd + " " + Prod + "\n")
                janela["TextQnt"].update("")
                janela["TextProduto"].update("")
                janela["Aviso"].update("Item adicionado com sucesso!")
            else:
                janela["Aviso"].update("Por favor, preencha todos os campos.")

    if evento == "Visualizar lista":
        try:
            with open('ListaCompras.txt', 'r') as arquivo:
                linhas = arquivo.readlines()
                linhas = [linha.strip() for linha in linhas if linha.strip()]
                janela["ListaDeCompras"].update(linhas)  # Atualiza a chave correta
        except FileNotFoundError:
            janela["Aviso"].update("Arquivo de lista não encontrado.")
        except:
            janela["Aviso"].update("Erro ao carregar a lista.")

    if evento == "Apagar":
        with open ('ListaCompras.txt', 'w') as arquivo:
            arquivo.write("")
        janela["ListaDeCompras"].update("")
    
    if evento == "Enviar":
        #janela["Aviso"].update("No momento esta opção está indisponivel :(")
        janela2 = sg.Window("Envio de e-mail", Layout_envio)

        while True:
            
            eventos, valores = janela2.read()

            if eventos == sg.WIN_CLOSED or eventos == "Cancelar":
                break

            if eventos == "Concluido":

                destinatario = valores["emailEnviar"]

                with open('ListaCompras.txt', 'r') as arquivo:
                    lista_compras = arquivo.readlines()
                    lista_compras = [linha.strip() for linha in lista_compras if linha.strip()]  # Remove linhas vazias
                    corpo_email = "<p>Lista de Compras:</p><ul>" + "".join(f"<li>{item}</li>" for item in lista_compras) + "</ul>"

                msg = email.message.Message()
                msg['Subject'] = "Lista de compras"
                msg['From'] = 'enviodeemailteste33@gmail.com'           
                msg['To'] = destinatario
                password = 'hjayluzdlseptcex' 
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(corpo_email )

                try:
                    # Envio do e-mail
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login(msg['From'], password)
                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
                    s.quit()
                    janela2["Aviso2"].update("E-mail enviado com sucesso!")
                except Exception as e:
                    janela2["Aviso2"].update(f"Erro ao enviar o e-mail: {e}")

        janela2.close()

janela.close()
