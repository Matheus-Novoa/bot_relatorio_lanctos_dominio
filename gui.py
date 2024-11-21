import customtkinter as ctk
from bot import main



# ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('dark-blue')

janela = ctk.CTk()
janela.geometry('370x170')
janela.title('Imprimir relatórios')

padx = 10
pady= 5
entryWidth = 180

#--------------- Número do Lote Inicial ------------------------
textoLoteInicial = ctk.CTkLabel(janela, text='Número do Lote')
textoLoteInicial.grid(row=0, column=0, padx=padx, pady=pady)

textPlaceholderLote = 'Insira o número do lote'
numeroLoteInicial = ctk.CTkEntry(janela,
                                 placeholder_text=textPlaceholderLote,
                                 width=entryWidth)
numeroLoteInicial.grid(row=0, column=1, padx=padx, pady=pady)
#-----------------------------------------------------------------------
#------------------ Mês -------------------------------
textoMes = ctk.CTkLabel(janela, text='Mês')
textoMes.grid(row=1, column=0, padx=padx, pady=pady)

textPlaceholderMes = 'Insira o mês de exercício'
mes = ctk.CTkEntry(janela,
                   placeholder_text=textPlaceholderMes,
                   width=entryWidth)
mes.grid(row=1, column=1, padx=padx, pady=pady)
#-------------------------------------------------------------
#-------------------- Quantidade -----------------------------------
textoQuantidade = ctk.CTkLabel(janela, text='Quantidade de Lotes')
textoQuantidade.grid(row=2, column=0, padx=padx, pady=pady)

textPlaceholderQuant = 'Insira a quantidade de lotes'
quantLotes = ctk.CTkEntry(janela,
                          placeholder_text=textPlaceholderQuant,
                          width=entryWidth)
quantLotes.grid(row=2, column=1, padx=padx, pady=pady)
#-------------------------------------------------------------------
def gatilho():
    janela.iconify()
    main(int(numeroLoteInicial.get()), mes.get(), int(quantLotes.get()))
    janela.destroy()

botao = ctk.CTkButton(janela, text='Iniciar', command=gatilho)
botao.grid(row=3, column=1, padx=padx, pady=20)

janela.mainloop()