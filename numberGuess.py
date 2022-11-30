from tkinter import *
import random
from network import connect, send
from tkinter import simpledialog, Tk

local_user: str = None
remote_user: str = None
ws = Tk()
ws.title('Welcome to Number Guessing Game')
ws.geometry('600x400')
ws.config(bg='#F7F0AE')

ranNum = random.randint(0, 10)
chance = 5
var = IntVar()
disp = StringVar()
game_details = StringVar()


def main():
    global local_user

    local_user = simpledialog.askstring(
        'Input', 'Your username'
    )

    channel = 'unique-channel-prefix' + simpledialog.askstring(
        'Input', 'channel to join'
    )
    game_details.set(f'{local_user} vs {remote_user}')
    print(game_details)
    connect(channel=channel, user=local_user, handler=on_network_message)
    send('hello')


def on_network_message(timestamp, user: str, message: str):
    global disp, remote_user, game_details
    print(message)
    print(message == 'win')
    print(message == 'win' and user == remote_user)
    if message == 'win' and user == remote_user:
        disp.set('Opponent Won')
        print('opponent won')
    if message == 'win' and user != remote_user:
        disp.set(f'You won! {ranNum} is the right answer.')
        print('writing')
    if message == 'loss' and user == remote_user:
        disp.set(f'You won! {ranNum} is the right answer.')
    if message == 'loss' and user != remote_user:
        disp.set('Opponent Won')
    if 'created' not in message:
        if message.split(" ")[1] != local_user and remote_user is None:
            remote_user = message.split(" ")[1]
            game_details.set(f'{local_user} vs {remote_user}')


def check_guess():
    global ranNum
    global chance
    usr_ip = var.get()
    if chance > 0:
        if usr_ip == ranNum:
            msg = f'You won! {ranNum} is the right answer.'
            disp.set(msg)
            send('win')
        elif usr_ip > ranNum:
            chance -= 1
            msg = f'{usr_ip} is greater. You have {chance} attempt left.'
            disp.set(msg)
        elif usr_ip < ranNum:
            chance -= 1
            msg = f'{usr_ip} is smaller. You have {chance} attempt left.'
            disp.set(msg)
        else:
            msg = 'Something went wrong!'
            disp.set(msg)

    else:
        msg = f'You Lost! you have {chance} attempt left.'
        disp.set(msg)
        send('loss')


Label(
    ws,
    text='Number Guessing Game',
    font=('sans-serif', 20),
    relief=SOLID,
    padx=10,
    pady=10,
    bg='#BEBAD3'
).pack(pady=(10, 0))

Label(
    ws,
    textvariable=game_details,
    bg='#5671A6',
    font=('sans-serif', 14)
).pack(pady=(20, 0))

Entry(
    ws,
    textvariable=var,
    font=('sans-serif', 18)
).pack(pady=(60, 10))

Button(
    ws,
    text='Guess',
    font=('sans-serif', 18),
    command=check_guess
).pack()

Label(
    ws,
    textvariable=disp,
    bg='#5671A6',
    font=('sans-serif', 14)
).pack(pady=(20, 0))
main()
ws.mainloop()
