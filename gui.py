import customtkinter as ctk
from bot import main



ctk.set_appearance_mode('system')

janela = ctk.CTk()
janela.geometry('500x200')

textoLoteInicial = ctk.CTkLabel(janela, text='Número do Lote').pack()
numeroLoteInicial = ctk.CTkEntry(janela, placeholder_text='lote')
numeroLoteInicial.pack()

textoMes = ctk.CTkLabel(janela, text='Mês').pack()
mes = ctk.CTkEntry(janela, placeholder_text='mes')
mes.pack()

textoQuantidade = ctk.CTkLabel(janela, text='Quantidade de Lotes').pack()
quantLotes = ctk.CTkEntry(janela)
quantLotes.pack()

def gatilho():
    janela.iconify()
    main(int(numeroLoteInicial.get()), mes.get(), int(quantLotes.get()))
    janela.destroy()

botao = ctk.CTkButton(janela, text='Iniciar', command=gatilho)
botao.pack()

janela.mainloop()