import tkinter as tk
import random

ventana = tk.Tk()
ventana.title("Ping-Pong Retro")

#Configuracion depantalla
ancho_pantalla = 800
alto_pantalla = 600
canvas = tk.Canvas(ventana, width = ancho_pantalla, height = alto_pantalla, bg= "black")
canvas.pack()

raqueta = canvas.create_rectangle(350,580,450,590, fill = "white")

#pelota

pelota = canvas.create_oval(390,290,410,310, fill = "red")

#Asignar velocidad a la pelota.
velocidad_x = random.choice([6, -6])
velocidad_y = -6



#Contador para rebote y marcador.
rebotes = 0
marcador = 0

#Crear etiqueta para el marcador
marcador_label = canvas.create_text(70, 30, text = f'Marcador: {marcador}', fill='white', font=('Arial', 18))

#Funcion para mover la raqueta

def mover_raqueta(event):
  tecla = event.keysym
  raqueta_pos = canvas.coords(raqueta)
  
  if tecla == "Left" and raqueta_pos[0] > 0:
    canvas.move(raqueta, -20,0)
    
  elif tecla == "Right" and raqueta_pos[2] < ancho_pantalla:
    canvas.move(raqueta, 20, 0)
  
#Vincular el evento de teclado con el movimiento de la raqueta.     
canvas.bind_all("<KeyPress-Left>", mover_raqueta)
canvas.bind_all("<KeyPress-Right>", mover_raqueta)

def reiniciar_juego():
  global velocidad_x, velocidad_y, pelota, marcador, rebotes

  #Reiniciar posicion de la raqueta y de la pelota.
  canvas.coords(raqueta, 350,580,450,590)

  #Eliminamos la pelota anterior para que no la detecte.
  canvas.delete(pelota)

  #Iniciamos una pelota nueva.
  pelota = canvas.create_oval(390,290,410,310, fill = "red")

  #Reiniciar el movimiento de la pelota. 
  velocidad_x = random.choice([6, -6])
  velocidad_y = -6

  #Resetear marcador y rebotes
  rebotes = 0
  marcador = 0
  actualizar_marcador()


  #Quitar mensaje Game Over.
  canvas.delete('game_over')
  
  #Desactivar el boton de reinicio.
  reiniciar_btn.config(state=tk.DISABLED)

  #Reiniciamos juego
  actualizar_juego()


#Funcion para actualizar el marcador
def actualizar_marcador():
  canvas.itemconfig(marcador_label, text = f'Marcador: {marcador}')


#Creando un boton de reinicio
reiniciar_btn = tk.Button(ventana, text = "Reiniciar Juego", command=reiniciar_juego, state=tk.DISABLED)
reiniciar_btn.pack()


def actualizar_juego():
  global velocidad_x, velocidad_y, rebotes, marcador
  
  #Obtener las coordenadas de la pelota.
  pelota_pos = canvas.coords(pelota)
  
  if pelota_pos[0] <=0 or pelota_pos[2] >= ancho_pantalla:
    velocidad_x *= -1
    
  if pelota_pos[1] <= 0:
    velocidad_y *= -1
    
  if canvas.coords(raqueta)[0] <=pelota_pos[2] <= canvas.coords(raqueta)[2] and canvas.coords(raqueta)[1] <= pelota_pos[3] <= canvas.coords(raqueta)[3]:
    velocidad_y *= -1
    
  if pelota_pos[3] >= alto_pantalla:
    canvas.create_text(ancho_pantalla / 2, alto_pantalla /2 , text = 'GAME OVER', fill = 'orange', font = ('Arial', 36), tags='game_over')
    reiniciar_btn.config(state=tk.ACTIVE)
    
  else:
    #Mover la pelota
    canvas.move(pelota, velocidad_x, velocidad_y)
    ventana.after(10, actualizar_juego)
    #Contar los rebotes
    if pelota_pos[3] >= alto_pantalla -20:
      rebotes += 1
      if rebotes == 5:
        if velocidad_y > 0:
          velocidad_y += 5
        else:
          velocidad_y -= 5
        rebotes = 0
      marcador += 1
      actualizar_marcador()
      

actualizar_juego()
ventana.mainloop()