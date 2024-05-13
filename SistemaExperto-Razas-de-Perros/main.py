from ctypes import sizeof
from lib2to3.pgen2.token import LEFTSHIFT
from logging import RootLogger
from operator import length_hint
from select import select
from tkinter import *
from tkinter import filedialog as fd
import shutil
import copy
import os
import tkinter
from turtle import width  
from PIL import ImageTk,Image
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import threading
import os
import random
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Frame utilizado para mostrar los graficos
class graph_frame(Frame):
    def __init__(self):
        Frame.__init__(self,root)
    
    
    def add_graph(self,fig):
        self.mpl_canvas=FigureCanvasTkAgg(fig,self)
        
        self.mpl_canvas.get_tk_widget().pack(fill=BOTH,expand=True)
        self.mpl_canvas._tkcanvas.pack( fill=BOTH, expand=True)
    def remove_graph(self):
        self.mpl_canvas.get_tk_widget().pack_forget()
        self.mpl_canvas._tkcanvas.pack_forget()
        del self.mpl_canvas

class dog:
    def __init__(self)->None:
        self.name = ""
        self.origin = ""
        self.description = ""
        self.temperament = ""
        self.breed_size = ""
        self.life_expectancy = ""
        self.health_issues = ""
        self.size = ""
        self.image="sources/default.jpeg"

        #Caracteristics
        self.caracteristics={}
        
##############################################################################################################################################################################
class visualizer:
    def __init__(self,menu,frame1,dog,rules,clasifier)->None:
        self.frame1=frame1
        self.clasifier=clasifier
        self.name=Label(self.frame1,text="PERRO",background='#353437')
        self.name.configure(font=("Arial",50))
        
        openImage=Image.open(dog.image)
        img=openImage.resize((200,300))
        self.photo=ImageTk.PhotoImage(img)
        self.image=Label(self.frame1,image=self.photo)

        self.size=Label(self.frame1,text="PERRO",background='#353437')
        self.size.configure(font=("Arial",40))
        self.description=Label(self.frame1,text="PERRO",background='#353437')
        self.description.configure(font=("Arial",40))
        self.habitat=Label(self.frame1,text="PERRO",background='#353437')
        self.habitat.configure(font=("Arial",40))
        self.comments=Label(self.frame1,text="PERRO",background='#353437')
        self.comments.configure(font=("Arial",40))
        self.explanation=Label(self.frame1,text="PERRO",background='#353437')
        self.explanation.configure(font=("Arial",40))
        self.menu_window=menu
        self.dog=dog
        self.rules=rules
        self.addButton=Button(self.frame1,text="Agregar Perro",command=self.add_dog,bg="#7a7b7c", fg="white")
        self.addButton.config(height=2,width=15)
        self.menuButton=Button(self.frame1,text="Menu Principal",command=self.main_window,bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2,width=15)
        self.showDog()


    def add_dog(self):
        self.addfunction=addDog(self.menu_window,self.frame1,self.clasifier)
        self.hide()
        self.addfunction.show()
#######################################################################################
    def show(self):
        self.name.pack()
        self.image.pack()
        self.breed_size.pack()
        self.description.pack()
        self.temperament.pack()
        self.origin.pack()
        self.life_expectancy.pack()
        self.health_issues.pack()

        self.explanation.pack()

        if(self.dog.name=="Desconocida"):
            self.addButton.pack(side=TOP)
        self.menuButton.pack(side=TOP)
#######################################################################################

    #Oculta la vista de la descripción del ave
    def hide(self):
        self.name.pack_forget()
        self.image.pack_forget()
        self.breed_size.pack_forget()
        self.description.pack_forget()
        self.temperament.pack_forget()
        self.origin.pack_forget()
        self.life_expectancy.pack_forget()
        self.health_issues.pack_forget()

        self.explanation.pack_forget()

        if(self.dog.name=="Desconocida"):
            self.addButton.pack_forget()
        self.menuButton.pack_forget()
#######################################################################################
    def showDog(self):
        self.name=Label(self.frame1,text=self.dog.name,background='#353437',fg="white")
        self.name.configure(font=("Arial",35))

        openImage=Image.open(self.dog.image)
        img=openImage.resize((200,200))
        self.photo=ImageTk.PhotoImage(img)       
        self.image=Label(self.frame1,image=self.photo)

        self.size=Label(self.frame1,text=self.dog.size,wraplength=1200,background='#353437',fg="white")
        self.size.configure(font=("Arial",14))

        self.breed_size = Label(self.frame1, text=self.dog.breed_size, wraplength=1200, background='#353437', fg="white")
        self.breed_size.configure(font=("Arial", 14))

        self.description = Label(self.frame1, text=self.dog.description, wraplength=1200, background='#353437', fg="white")
        self.description.configure(font=("Arial", 14))

        self.temperament = Label(self.frame1, text=self.dog.temperament, wraplength=1200, background='#353437', fg="white")
        self.temperament.configure(font=("Arial", 14))

        self.origin = Label(self.frame1, text=self.dog.origin, wraplength=1200, background='#353437', fg="white")
        self.origin.configure(font=("Arial", 14))

        self.life_expectancy = Label(self.frame1, text=self.dog.life_expectancy, wraplength=1200, background='#353437', fg="white")
        self.life_expectancy.configure(font=("Arial", 14))

        self.health_issues = Label(self.frame1, text=self.dog.health_issues, wraplength=1200, background='#353437', fg="white")
        self.health_issues.configure(font=("Arial", 14))


        exp="\n\n\nLa Raza de Perro fue encontrada en base a las siguientes características:\n"
        for key in self.rules.keys():
            exp+=key+":"+self.rules[key]+"\n"

        self.explanation=Label(self.frame1,text=exp,wraplength=1200,background='#353437',fg="white")
        self.explanation.configure(font=("Arial",14))
#######################################################################################
    

    #Muestra la vista principal
    def main_window(self):
        self.hide()
        self.menu_window.show()
    
    def closing(self):
        del self

##############################################################################################################################################################################
class addDog:
    def __init__(self,menu,frame1,clasifier)->None:
        self.frame1=frame1
        self.main_menu=menu
        self.clasifier=clasifier
        self.load_caracteristics()
        self.labels = []
        self.entries = []

        for caracteristic in self.caracteristics:
            self.labels.append(Label(self.frame1,text=caracteristic.capitalize(),background='#353437',fg="white"))
            if(caracteristic=="descripcion" or caracteristic=="origen" or caracteristic=="temperamento"):
                self.entries.append(Text(self.frame1, height=2, width=45))
            else:
                self.entries.append(Entry(self.frame1,width=60))

#######################################################################################        

    def load_caracteristics(self):
        self.caracteristics = []
        self.caracteristics.append("nombre")
        self.caracteristics.append("descripcion")
        self.caracteristics.append("origen")
        self.caracteristics.append("temperamento")

        self.caracteristics.append("color_principal")
        self.caracteristics.append("color_secundario")
        self.caracteristics.append("marcas")
        self.caracteristics.append("nariz")
        self.caracteristics.append("ojos")
        self.caracteristics.append("orejas")
        self.caracteristics.append("patas")
        self.caracteristics.append("cola")
        self.caracteristics.append("pecho")


#######################################################################################    
    def show(self):
        self.title=Label(self.frame1,text="Agregar Perro",background='#353437',fg="white")
        self.title.configure(font=("Arial",20))
        self.title.grid(column=1,row=1,columnspan=5)
        self.currentpos=3
        for i in range(len(self.labels)):
            self.labels[i].configure(font=("Arial",15))
            self.labels[i].grid(column=1,row=self.currentpos)
            self.entries[i].grid(column=2, row=self.currentpos)
            if(self.caracteristics[i]=="temperamento"):
                self.currentpos+=1
                self.instructions=Label(self.frame1,text="Indique los colores de las siguientes caracteristicas",background='#353437',fg="white")
                self.instructions.configure(font=("Arial",20))
                self.instructions.grid(column=1, row=self.currentpos,columnspan=2)
            self.currentpos+=1

        self.filename=StringVar()
        self.image=Label(self.frame1,text="Imagen",background='#353437',fg="white")
        self.image.configure(font=("Arial",15))
        self.image.grid(column=1,row=23)
        self.showRute=Entry(self.frame1,textvariable=self.filename)
        self.showRute.config(state='disabled',width=60)
        self.showRute.grid(column=2,row=23)
        self.chooseImage=Button(self.frame1,text="Seleccionar Imagen",command=self.selectImage,bg="#7a7b7c",fg="white")
        self.chooseImage.config(height=1,width=15)
        self.chooseImage.grid(column=3,row=23)
        self.saveButton=Button(self.frame1,text="Guardar",command=self.save,bg="#7a7b7c",fg="white")
        self.saveButton.config(height=2,width=15)
        self.saveButton.grid(column=2,row=27)
        self.menuButton=Button(self.frame1,text="Menu Principal",command=self.main_window,bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2,width=15)
        self.menuButton.grid(column=1,row=27)

#######################################################################################

    def selectImage(self):
        self.filename.set(fd.askopenfilename(initialdir = "/",title = "Seleccionar imagen",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
        

    def hide(self):
        self.title.grid_remove()
        for i in range(len(self.labels)):
            self.labels[i].grid_remove()
            self.entries[i].grid_remove()
        self.chooseImage.grid_remove()
        self.instructions.grid_remove()
        self.image.grid_remove()
        self.showRute.grid_remove()
        self.saveButton.grid_remove()
        self.menuButton.grid_remove()

#######################################################################################

    def save(self):
        self.aux = dog()
        for i in range(len(self.entries)):
            if(self.caracteristics[i]=="descripcion" or self.caracteristics[i]=="origen" or self.caracteristics[i]=="temperamento"):
                if(self.caracteristics[i]=="descripcion"):
                    self.aux.description=self.entries[i].get(1.0,"end-1c")
                elif(self.caracteristics[i]=="origen"):
                    self.aux.habitat=self.entries[i].get(1.0,"end-1c")
                elif(self.caracteristics[i]=="temperamento"):
                    self.aux.comments=self.entries[i].get(1.0,"end-1c")
            else:
                if(self.entries[i].get()!=""):
                    if(self.caracteristics[i]=="nombre"):
                        self.aux.name=self.entries[i].get()
                    else:
                        self.aux.caracteristics[self.caracteristics[i]]=self.entries[i].get()
        self.currentpath = os.getcwd()
        self.currentpath+="\\sources\\"
        shutil.copy(self.filename.get(),self.currentpath)
        self.words=self.filename.get().split("/")
        self.aux.image="sources/"+self.words[-1]
        self.clasifier.perros.append(self.aux)
        self.hide()
        self.main_menu.show()
    
    def main_window(self):
        self.hide()
        self.main_menu.show()

#######################################################################################

#En esta clase se tienen los metodos para clasificar
class clasifier:
    #Constructor de la clase
    def __init__(self,menu,frame1) -> None:
        self.menu_window=menu
        self.frame1=frame1
        self.title=Label(self.frame1,text="Clasificador de perros",background='#353437',fg="white")
        self.title.configure(font=("Arial",35))

        self.menuButton=Button(self.frame1,text="Main Menu",command=self.main_window,bg="#7a7b7c",fg="white")
        self.menuButton.config(height=10,width=50)
        self.perros=[]
        self.default_perro=dog()
        self.load_dogs()
        self.loadall()
#######################################################################################

    def loadall(self):
        
        self.good=False
        self.doing=True
        
        
        self.rules={}
        self.decition=self.perros[0]
        self.visual=visualizer(self.menu_window,self.frame1,self.decition,self.rules,self)
        self.possible_rules={}
        self.possible_perros=[]
#######################################################################################
        
        
    def load_dogs(self):
        self.default_perro.name="Desconocida"
        self.default_perro.image="sources/default.jpeg"


        """
        self.aux=dog()
        self.aux.name=""
        self.aux.origin=""
        self.aux.description=""
        self.aux.temperament=""
        self.aux.breed_size=""
        self.aux.life_expectancy=""
        self.aux.health_issues=""
        self.aux.caracteristics["color_principal"] = ""
        self.aux.caracteristics["color_secundario"] = ""
        self.aux.caracteristics["marcas"] = ""
        self.aux.caracteristics["nariz"] = ""
        self.aux.caracteristics["ojos"] = ""
        self.aux.caracteristics["orejas"] = ""
        self.aux.caracteristics["patas"] = ""
        self.aux.caracteristics["cola"] = ""
        self.aux.caracteristics["pecho"] = ""
        self.aux.image="sources/name_dog.jpg"
        self.perros.append(self.aux)
        """


        self.aux = dog()
        self.aux.name = "Labrador Retriever"
        self.aux.origin = "Originario de Canadá, desarrollado inicialmente como perro de pesca y caza."
        self.aux.description = "Labrador Retriever, conocido por su inteligencia y adaptabilidad, es ideal para roles de rescate y como perro de compañía."
        self.aux.temperament = "Extremadamente amigable y sociable, es conocido por su disposición amable y su paciencia."
        self.aux.breed_size = "Grande, con machos que suelen pesar entre 29 y 36 kg."
        self.aux.life_expectancy = "Vida promedio de 10 a 12 años, con buena salud y cuidado adecuado."
        self.aux.health_issues = "Susceptible a problemas de cadera y codo, así como a obesidad si no se mantiene activo."
        self.aux.caracteristics["color_principal"] = "chocolate"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "ninguna"
        self.aux.caracteristics["nariz"] = "marrón"
        self.aux.caracteristics["ojos"] = "avellana"
        self.aux.caracteristics["orejas"] = "chocolate"
        self.aux.caracteristics["patas"] = "chocolate"
        self.aux.caracteristics["cola"] = "chocolate"
        self.aux.caracteristics["pecho"] = "chocolate"
        self.aux.image = "sources/labrador_retriever.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Bulldog Francés"
        self.aux.origin = "Originario de Francia, popularizado por su encanto en la sociedad parisina del siglo XIX."
        self.aux.description = "Compacto y muscular, el Bulldog Francés es valorado por su personalidad afectuosa y su naturaleza juguetona."
        self.aux.temperament = "Afectuoso y vivaz, es conocido por su lealtad y su comportamiento vigilante."
        self.aux.breed_size = "Pequeño, ideal para la vida en apartamento."
        self.aux.life_expectancy = "Típicamente vive entre 10 y 12 años."
        self.aux.health_issues = "Sensibles a las temperaturas extremas; problemas respiratorios comunes debido a su hocico corto (braquicefálico); susceptibles a enfermedades de la piel y alergias; propensos a problemas de columna y articulaciones debido a su estructura compacta."
        self.aux.caracteristics["color_principal"] = "brindle"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "rayas"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "oscuro"
        self.aux.caracteristics["orejas"] = "negro"
        self.aux.caracteristics["patas"] = "brindle"
        self.aux.caracteristics["cola"] = "brindle"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/bulldog_frances.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Husky Siberiano"
        self.aux.origin = "Originario de Siberia, criado por la tribu Chukchi para tirar de trineos."
        self.aux.description = "El Husky Siberiano destaca por su impresionante resistencia y capacidad para trabajar en equipos, ideal para climas fríos."
        self.aux.temperament = "Energético y amistoso, posee una notable capacidad de adaptación y resistencia."
        self.aux.breed_size = "De tamaño mediano, bien proporcionado y ágil."
        self.aux.life_expectancy = "Vive entre 12 y 15 años, con un cuidado y ejercicio adecuados."
        self.aux.health_issues = "Generalmente saludable pero puede desarrollar problemas oculares como cataratas y glaucoma, además de displasia de cadera; algunos ejemplares pueden sufrir de hipotiroidismo."
        self.aux.caracteristics["color_principal"] = "gris"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "máscara"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "azul"
        self.aux.caracteristics["orejas"] = "gris"
        self.aux.caracteristics["patas"] = "blanco"
        self.aux.caracteristics["cola"] = "gris"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/husky_siberiano.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Beagle"
        self.aux.origin = "Originario de Inglaterra, utilizado históricamente para la caza menor debido a su agudo sentido del olfato."
        self.aux.description = "Pequeño y ágil, el Beagle es célebre por su capacidad para seguir rastros y su naturaleza entusiasta."
        self.aux.temperament = "Extremadamente sociable y enérgico, disfruta de la compañía y es ideal para familias."
        self.aux.breed_size = "De tamaño pequeño, perfecto para hogares activos."
        self.aux.life_expectancy = "Generalmente saludable, con una esperanza de vida de 12 a 15 años."
        self.aux.health_issues = "Propenso a problemas de obesidad si no se mantiene activo; comunes las infecciones de oído debido a sus orejas caídas y largas; enfermedades cardíacas y epilepsia también son preocupaciones en la raza."
        self.aux.caracteristics["color_principal"] = "tricolor"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "manchas"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "marrón"
        self.aux.caracteristics["orejas"] = "marrón"
        self.aux.caracteristics["patas"] = "blanco"
        self.aux.caracteristics["cola"] = "marrón"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/beagle.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Dálmata"
        self.aux.origin = "Originario de Croacia, históricamente usado como perro de carruaje."
        self.aux.description = "El Dálmata es reconocido por su distintivo pelaje moteado y su capacidad para realizar tareas extenuantes."
        self.aux.temperament = "Muy sociable e inteligente, se destaca en actividades que requieren resistencia y agilidad."
        self.aux.breed_size = "De tamaño mediano, atlético y elegante."
        self.aux.life_expectancy = "Tiene una vida útil de 10 a 13 años con el cuidado adecuado."
        self.aux.health_issues = "Tiene una alta incidencia de sordera, tanto parcial como total; propenso a formaciones de cálculos urinarios y problemas renales; puede desarrollar alergias de piel y displasia de cadera."
        self.aux.caracteristics["color_principal"] = "blanco"
        self.aux.caracteristics["color_secundario"] = "negro"
        self.aux.caracteristics["marcas"] = "manchas"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "marrón"
        self.aux.caracteristics["orejas"] = "negro"
        self.aux.caracteristics["patas"] = "blanco"
        self.aux.caracteristics["cola"] = "blanco"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/dalmata.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Golden Retriever"
        self.aux.origin = "Originario de Escocia, desarrollado para la caza de aves acuáticas."
        self.aux.description = "El Golden Retriever es apreciado por su amigable disposición y su pelo dorado brillante, perfecto tanto para la compañía como para el trabajo."
        self.aux.temperament = "Extremadamente amable y paciente, es excelente con niños y otros animales."
        self.aux.breed_size = "De tamaño grande, fuerte y musculoso."
        self.aux.life_expectancy = "Vive entre 10 y 12 años, disfrutando generalmente de buena salud."
        self.aux.health_issues = "Puede padecer de problemas cardiacos y articulares, incluyendo displasia de cadera y de codo."
        self.aux.caracteristics["color_principal"] = "dorado"
        self.aux.caracteristics["color_secundario"] = "crema"
        self.aux.caracteristics["marcas"] = "ninguna"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "marrón"
        self.aux.caracteristics["orejas"] = "dorado"
        self.aux.caracteristics["patas"] = "dorado"
        self.aux.caracteristics["cola"] = "dorado"
        self.aux.caracteristics["pecho"] = "dorado"
        self.aux.image = "sources/golden_retriever.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Boxer"
        self.aux.origin = "Originario de Alemania, criado inicialmente como perro de trabajo y guarda."
        self.aux.description = "El Boxer es conocido por su estructura musculosa y su expresión alerta, siendo un protector leal y un compañero juguetón."
        self.aux.temperament = "Energético y valiente, pero también increíblemente dulce con su familia."
        self.aux.breed_size = "De tamaño mediano a grande, con un físico robusto."
        self.aux.life_expectancy = "Generalmente vive entre 10 y 12 años."
        self.aux.health_issues = "Susceptible a problemas cardiacos, cáncer y problemas respiratorios."
        self.aux.caracteristics["color_principal"] = "marrón"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "máscara negra"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "oscuro"
        self.aux.caracteristics["orejas"] = "marrón"
        self.aux.caracteristics["patas"] = "blanco"
        self.aux.caracteristics["cola"] = "marrón"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/boxer.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Poodle"
        self.aux.origin = "Originario de Francia, aunque algunos creen que es de Alemania, popularizado por su habilidad en la caza de aves acuáticas."
        self.aux.description = "El Poodle es famoso por su inteligencia y su pelaje rizado que viene en varios tamaños y colores."
        self.aux.temperament = "Extremadamente inteligente y fácil de entrenar, ideal para competiciones y como perro de terapia."
        self.aux.breed_size = "Disponible en tamaños estándar, miniatura y toy."
        self.aux.life_expectancy = "Puede vivir entre 12 y 15 años dependiendo del tamaño."
        self.aux.health_issues = "Propenso a problemas genéticos como displasia de cadera y enfermedades oculares."
        self.aux.caracteristics["color_principal"] = "blanco"
        self.aux.caracteristics["color_secundario"] = "negro"
        self.aux.caracteristics["marcas"] = "uniforme"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "oscuro"
        self.aux.caracteristics["orejas"] = "blanco"
        self.aux.caracteristics["patas"] = "blanco"
        self.aux.caracteristics["cola"] = "blanco"
        self.aux.caracteristics["pecho"] = "blanco"
        self.aux.image = "sources/poodle.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Cocker Spaniel"
        self.aux.origin = "Originario de España, popularizado en Inglaterra y conocido por su habilidad en la caza de aves."
        self.aux.description = "El Cocker Spaniel es apreciado por su dulce expresión y sus largas orejas, ideal tanto para la caza como para ser un compañero de familia."
        self.aux.temperament = "Amistoso, alegre y adaptable, se lleva bien con niños y otros animales."
        self.aux.breed_size = "De tamaño pequeño a mediano, con un cuerpo compacto."
        self.aux.life_expectancy = "Vive entre 12 y 15 años con los cuidados adecuados."
        self.aux.health_issues = "Propenso a infecciones de oído y problemas oculares."
        self.aux.caracteristics["color_principal"] = "dorado"
        self.aux.caracteristics["color_secundario"] = "blanco"
        self.aux.caracteristics["marcas"] = "ninguna"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "marrón"
        self.aux.caracteristics["orejas"] = "dorado"
        self.aux.caracteristics["patas"] = "dorado"
        self.aux.caracteristics["cola"] = "dorado"
        self.aux.caracteristics["pecho"] = "dorado"
        self.aux.image = "sources/cocker_spaniel.jpg"
        self.perros.append(self.aux)


        self.aux = dog()
        self.aux.name = "Rottweiler"
        self.aux.origin = "Originario de Alemania, utilizado históricamente como perro de ganado y protección."
        self.aux.description = "El Rottweiler es robusto y poderoso, conocido por su lealtad y coraje."
        self.aux.temperament = "Confiable y protector, pero necesita una socialización y entrenamiento adecuados."
        self.aux.breed_size = "Grande, con una estructura sólida y musculosa."
        self.aux.life_expectancy = "Vive entre 8 y 10 años."
        self.aux.health_issues = "Puede sufrir de problemas articulares y cardiacos, requiere manejo cuidadoso de su dieta y ejercicio."
        self.aux.caracteristics["color_principal"] = "negro"
        self.aux.caracteristics["color_secundario"] = "marrón"
        self.aux.caracteristics["marcas"] = "máscara"
        self.aux.caracteristics["nariz"] = "negro"
        self.aux.caracteristics["ojos"] = "oscuro"
        self.aux.caracteristics["orejas"] = "negro"
        self.aux.caracteristics["patas"] = "marrón"
        self.aux.caracteristics["cola"] = "negro"
        self.aux.caracteristics["pecho"] = "marrón"
        self.aux.image = "sources/rottweiler.jpg"
        self.perros.append(self.aux)







        #self.aves.append(self.aux)

#######################################################################################

    def question(self,q,opt):
        options=[]
        options.append("Otro")
        for key in opt.keys():
            options.append(key)
        self.selection=StringVar()
        self.chooses=StringVar()
        self.chooses.set("Otro")
        self.instructions=Label(self.frame1,text="Seleccione el color de las siguientes caracteristicas del perro:\n\n",background='#353437',fg="white")
        self.instructions.configure(font=("Arial",25))
        self.instructions.pack()
        
        self.caracteristica=Label(self.frame1,text=q,background='#353437',fg="white")
        self.caracteristica.configure(font=("Arial",25))
        self.caracteristica.pack()
        self.drop=OptionMenu(self.frame1,self.chooses,*options)
        self.drop.config(height=1,width=20)
        self.drop.pack()
        self.button=Button(self.frame1,text="Siguiente",command=self.clicked,bg="#7a7b7c",fg="white")
        self.button.config(height=2,width=10)
        self.button.pack()
        self.button.wait_variable(self.selection)
        self.cont = 0
        self.listo = False

        self.instructions.pack_forget()
        self.drop.pack_forget()

        self.button.pack_forget()
        self.caracteristica.pack_forget()
        return self.selection

#######################################################################################

    def clicked(self):
        print(self.chooses.get())
        self.selection.set(self.chooses.get())

#######################################################################################

    def clasify(self):

        self.loadall()
        self.possible_perros=copy.copy(self.perros)
        self.possible_rules={}
        self.rules={}
        other=True
        while(other):
            self.possible_rules={}
            for perro in self.possible_perros:
                for key in perro.caracteristics.keys():
                    if(key not in self.rules):
                        if(key not in self.possible_rules):
                            self.possible_rules[key]={}
                        if(perro.caracteristics[key] not in self.possible_rules[key]):
                            self.possible_rules[key][perro.caracteristics[key]]=1
                        else:
                            self.possible_rules[key][perro.caracteristics[key]]+=1
                        
            color=StringVar()
            caracteristic=""
            for key in self.possible_rules.keys():
                color.set(self.question(key,self.possible_rules[key]).get())
                caracteristic=key
                self.rules[key]=color.get()
                print(color.get())
                break
            index=0
            elements=len(self.possible_perros)
            while index < elements:
                print(self.possible_perros[index].name)
                if(caracteristic not in self.possible_perros[index].caracteristics):
                    self.possible_perros[index].caracteristics[caracteristic]="otro"
                if(self.possible_perros[index].caracteristics[caracteristic]!=color.get()):
                    del self.possible_perros[index]
                    elements-=1
                else:
                    index+=1
            
            
            if(len(self.possible_perros)<2):
                other=False
            
        
        if(len(self.possible_perros)==1):
            perrotoshow=self.possible_perros[0]

            self.visual=visualizer(self.menu_window,self.frame1,perrotoshow,self.rules,self)
        else:
            self.visual=visualizer(self.menu_window,self.frame1,self.default_perro,self.rules,self)
        
        self.visual.show()

#######################################################################################

    def show(self):
        self.title.pack()
        self.clasify()
        

    #Oculta la vista del apartado de clasificación
    def hide(self):
        self.title.pack_forget()
        self.menuButton.pack_forget()
        

    #Muestra la vista principal
    def main_window(self):
        self.hide()
        
        self.menu_window.show()

    def closing(self):
        self.visual.closing()
        del self

##############################################################################################################################################################################

class main_menu:
    def __init__(self) -> None:
        
        
        openImage=Image.open("sources/dog.jpg")
        img=openImage.resize((1550,800))

        self.frame1 = Frame(root,background='#353437')
        self.title=Label(self.frame1, text="Clasificador de razas de perros\n\n\n",font=("Arial",25),background='#353437',fg="white")
        self.clasifier_button=Button(self.frame1,text="Encontrar perro",command=self.show_clasifier_window,bg="#7a7b7c",fg="white")
        self.clasifier_button.config(height=5,width=30)
        self.clasifier_window = clasifier(self,self.frame1)

#######################################################################################

    #Muestra la vista principal
    def show(self):
        
        self.frame1.pack(pady = 20 )
        self.title.pack()
        self.clasifier_button.pack()
    
    #Oculta la vista principal
    def hide(self):
        self.title.pack_forget()
        self.clasifier_button.pack_forget()

    #Muestra la vista del clasificador
    def show_clasifier_window(self):
        self.hide()
        
        self.clasifier_window.clasify()

    #Funcion para terminar los procesos 
    def closing(self):
        self.clasifier_window.closing()
        del self

#######################################################################################

if __name__ == "__main__":
    try:
        root = Tk()
        def on_closing():
            program.closing()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.title("Sistema experto")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d" % (w, h))
        root.configure(bg='#353437')
        program=main_menu()
        program.show()
        root.mainloop()
    except:
        quit()