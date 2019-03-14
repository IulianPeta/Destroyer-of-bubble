from tkinter import* #importa toate functiile Tkinter
HEIGHT = 500 #stabileste dimensiunea ferestrei
WIDTH = 800  # IDEM
window = Tk()
window.title('Distrugatorul de bule') #da jocului un titlu de impact
c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
#Canvas creeaza o panza pe care se poate desena
#darkblue stabileste culoare pentru fond (marea)
c.pack()

ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
#desesneaza un triunghi rosu pe post de submarin
ship_id2 = c.create_oval(0,0, 30, 30, outline='red')
#deseneaza un contur rosu pentru cerc
SHIP_R = 15 #raza (deminesiunea) submarinului
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
#variabilele "MID_X" si "MID_Y" ofera cooedonatele pentru mijlocul ecranului
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)
#misca ambele parti ale submarinului catre centrul ecranului

SHIP_SPD = 20 #submarinul se va deplasa pe aceasta distanta when press
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
#misca cele doua parti ale submarinului in sus cand este apasata UP ARROW

    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)
c.bind_all('<Key>', move_ship)
#Keu ruleaza "move_ship" de fiecare data cand este apasata vreo tasta

from random import randint
bub_id = list()
bub_r = list()
bub_speed = list()
#creeaza trei liste goale pentru a stoca nr. de indetificare, raza si viteza

MIN_BUB_R = 10
MAX_BUB_R = 30
#stabileste raza minima a bulei la 10 si pe cea maxima 30

MAX_BUB_SPD = 10
GAP = 100
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    #stabileste pozitia bulei pe panza
    r = randint(MIN_BUB_R, MAX_BUB_R)
    #alege o dimensiune la intamplare pentru bule, max si minim
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
    #forma bulei
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))
    #adauga numarul de identificare, raza si viteza bulei

def move_bubbles():
    for i in range(len(bub_id)): #trece prin fiecare bula de pe lista
        c.move(bub_id[i], - bub_speed[i], 0)
        
def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2 #descopera coordonata x a mijlocului bulei
    y = (pos[1] + pos[3])/2 #descopera coordonata y a mijlocului bulei
    return x, y
def del_bubble(i): #sterge bula cu nr de identificare "i"
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i]) #sterge bula de pe panza
    del bub_id[i] #sterge bula din lista cu numere de identificare
def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1): #aceasta trece de la coarda la cap prin lista de bule, pt. ca bucla
                                           #"for" sa nu provoace o eroare la stergere
        x, y = get_coords(bub_id[i])
        if x < - GAP:
            del_bubble(i)
from math import sqrt
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
def collision():
    points = 0 #puncte inscrise
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub) #sterge bula
    return points #numarul de puncte
c.create_text(50, 30, text='TIME', fill='white')
c.create_text(150, 30, text='SCORE', fill='white')
#creeaza etichete "TIME" si "SCORE" pentru a-i explica jucatorului ce inseamna numerele
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')
#stabileste scorul si timpul ramasa
def show_score(score):
    c.itemconfig(score_text, text=str(score))
def show_time (time_left):
    c.itemconfig(time_text, text=str(time_left))

    

from time import sleep, time #importa functii din biblioteca time
BUB_CHANCE = 10
TIME_LIMIT = 30 #incepe jocul cu o limita de timp de 30 de secunde
BONUS_SCORE = 1000 #stabileste cand este acordat bonusul e timp(1000 de puncte)
score = 0  #seteaza scorul la zero la inceputul jocului
bonus = 0
end = time() + TIME_LIMIT #stocheaza timpul la care se termina jocul intr-o variabila num "end"
#MAIN GAME LOOP


while time() < end: #repeta principala bucla a jocului pana la finalul jocului
    if randint(1, BUB_CHANCE) == 1: #daca numarul aleatoriu este 1, programul creeaza o noua bula
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision() #adauga punctajul bulelor la total
    if (int(score / BONUS_SCORE)) > bonus: #calculeaza cand sa ofere timpul bonus
        bonus += 1
        end += TIME_LIMIT
    show_score(score) #scorul apare in fereastra jocului
    show_time(int(end - time()))  #afiseaza timpul ramas
    window.update()
    sleep(0.001)

c.create_text(MID_X, MID_Y, \
    text='GAME OVER', fill='white', font=('Helvetica', 30))
# pune grafica in centrul ecranului
# "Helvetica" este un font bun pentru litere

c.create_text(MID_X, MID_Y + 30, \
    text='Score: ' + str(score), fill='white')
#iti spune care a fost scorul tau

c.create_text(MID_X, MID_Y + 45, \
    text='Bonus time: ' + str(bonus*TIME_LIMIT), fill='white')
#str bonus arata cat timp in plus ai castigat
