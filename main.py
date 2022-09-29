from datetime import timedelta
from glob import glob
from telnetlib import GA
import tkinter as tk
import threading
from turtle import bgcolor
from apscheduler.schedulers.background import BlockingScheduler
import os
from PIL import Image, ImageTk
import platform


Game = tk.Tk()
Game.wm_title("Cookie Clicker")
Game.geometry("500x700")
Game.iconphoto(False, tk.PhotoImage(file='1.png'))

background_var = "background3.png"

max_clicker = 0
max_money = 0

money = 1000000
click_reward = 1
clicker_level = 1
console_message = ""

auto_upgrader = False
AU_unlocked = False

# Prestige
prestige_level = 0
prestige_upgrade_price = 1000000
prestige_multiplier = 1

prestige_coins = 105

# Autoclicker 1
autoclicker1_level = 1
autoclicker1_reward = 0
autoclicker1_upgrade_price = 100
# Autoclicker 2
autoclicker2_level = 1
autoclicker2_reward = 0
autoclicker2_upgrade_price = 5000

# Autoclicker 3
autoclicker3_level = 1
autoclicker3_reward = 0
autoclicker3_upgrade_price = 250000

# Autoclickers
autoclick_timer = 0
autoclicker_reward = autoclicker1_reward + autoclicker2_reward

def autoclicker_reward_refresh():
    global autoclicker_reward
    global autoclicker1_reward
    global autoclicker2_reward
    global autoclicker3_reward
    autoclicker_reward = prestige_multiplier * (autoclicker1_reward + autoclicker2_reward + autoclicker3_reward)

# Pricing
clicker_upgrade_price = 10

timer = 60



def boss1():
    boss1_area = tk.Tk()
    Game.after(1000, subtimer)


def bosses_popup():
    top = tk.Toplevel(Game)
    top.geometry("400x400")
    top.title("Boss List")
    #tk.Label(top, text= "Bosses", font=('Serial')).place(x=175,y=10)

    BossesLabel = tk.Label(top, text = "Bosses")
    BossesLabel.pack()  

    TimerLabel = tk.Label(top, text = str(timer))
    TimerLabel.pack()

    Boss1 = tk.Button(top, text = "Boss Level 1, 10k in 60s", command = boss1)
    Boss1.pack()

def subtimer():
    global TimerLabel
    global timer
    print(timer)
    timer -= 1
    TimerLabel.config(text = str(timer))
    Game.after(1000, subtimer)

def Console(console_message):
    Console_Label.config(text="Console: " + console_message)

def clear_console():
    console_message = ""
    Console_Label.config(text="Console: " + console_message)

def click():
    global money
    money += click_reward * prestige_multiplier
    Money_Label.config(text="Money: " + str(money))

def prestige_upgrade():
    global prestige_upgrade_price
    global prestige_level
    global prestige_multiplier
    global prestige_coins
    global money
    if money >= prestige_upgrade_price:
        prestige_coins += int(money / prestige_upgrade_price)
        money -= prestige_upgrade_price
        prestige_multiplier += 1 + int(prestige_level / 5)
        Console("Congratulation! Multiplier: " + str(prestige_multiplier) + "x")
        Prestige_Label.config(text="Prestige Multiplier: " + str(prestige_multiplier))
        prestige_upgrade_price += int(prestige_upgrade_price / 4)

        # Reset other stats
        global autoclicker1_level
        global autoclicker1_reward
        global autoclicker1_upgrade_price

        global autoclicker2_level
        global autoclicker2_reward
        global autoclicker2_upgrade_price

        global autoclicker3_level
        global autoclicker3_reward
        global autoclicker3_upgrade_price

        global clicker_level
        global click_reward

        global clicker_upgrade_price 

        global autoclicker_reward

        clicker_upgrade_price = 10
        clicker_level = 1
        click_reward = 1

        money = 0
        autoclicker1_level = 1
        autoclicker2_level = 1
        autoclicker3_level = 1

        autoclicker1_reward = 0
        autoclicker2_reward = 0
        autoclicker3_reward = 0

        autoclicker1_upgrade_price = 100
        autoclicker2_upgrade_price = 5000
        autoclicker3_upgrade_price = 250000

        autoclicker_reward = 0

        ClickUpgrade.config(text = "Upgrade Clicker [1] | Price: " + str(clicker_upgrade_price))
        Money_Label.config(text = "Money: 0" )
        Reward_Label.config(text = "Money per click: " + str(int(click_reward * prestige_multiplier)))
        Auto_Reward_Label.config(text = "Money per second: 0")
        Autoclicker1_Upgrade.config(text = "Upgrade Autoclicker1 [0] | Price: " + str(autoclicker1_upgrade_price))
        Autoclicker2_Upgrade.config(text = "Upgrade Autoclicker2 [0] | Price: " + str(autoclicker2_upgrade_price))
        Autoclicker3_Upgrade.config(text = "Upgrade Autoclicker3 [0] | Price: " + str(autoclicker3_upgrade_price))

        Prestige_Coins_Label.config(text="Prestige Coins: " + str(prestige_coins))

        Prestige.config(text = "Prestige Level ["+ str(prestige_multiplier) +"x] | Upgrade for: " + str(prestige_upgrade_price))
        MaxClickUpgrade.config(text = "Max Upgrade Clicker [+" + str(0)  + "] | Price: " + str(0))
    else:
        Console("You don't have enough money to do that!")


def autoclicker1_upgrade():
    global shop_menu
    global autoclick_timer
    global money
    global autoclicker_reward
    global autoclicker1_reward
    global autoclicker1_upgrade_price
    global autoclicker1_level
    if autoclicker1_level <= 10:
        if money >= autoclicker1_upgrade_price:
            autoclicker1_level += 1
            money -= autoclicker1_upgrade_price
            autoclicker1_upgrade_price += int(autoclicker1_upgrade_price / 2)
            Money_Label.config(text="Money: " + str(money))
            autoclicker1_reward += 2 * autoclicker1_level + int((autoclicker1_level / 10) + 1 * 5)
            autoclicker_reward_refresh()
            Auto_Reward_Label.config(text="Money per second: " + str(autoclicker_reward))
            if autoclicker1_level < 11:
                Autoclicker1_Upgrade.config(text = "Upgrade Autoclicker1 [" + str(autoclicker1_level - 1) + "] | Price: " + str(autoclicker1_upgrade_price))
            else:
                Autoclicker1_Upgrade.config(text = "Autoclicker1 [Max]")
        else:
            Console("You don't have enough money to do that!")
    else:
        Console("Autoclicker1 already maxed out!")

def autoclicker2_upgrade():
    global shop_menu
    global autoclick_timer
    global money
    global autoclicker_reward
    global autoclicker2_reward
    global autoclicker2_upgrade_price
    global autoclicker2_level
    if autoclicker2_level <= 10:
        if money >= autoclicker2_upgrade_price:
            autoclicker2_level += 1
            money -= autoclicker2_upgrade_price
            autoclicker2_upgrade_price += int(autoclicker2_upgrade_price / 2)
            Money_Label.config(text="Money: " + str(money))
            autoclicker2_reward += 100 * autoclicker2_level + int((autoclicker2_level / 10) + 1 * 250)
            autoclicker_reward_refresh()
            Auto_Reward_Label.config(text="Money per second: " + str(autoclicker_reward))
            if autoclicker2_level < 11:
                Autoclicker2_Upgrade.config(text = "Upgrade Autoclicker2 [" + str(autoclicker2_level - 1) + "] | Price: " + str(autoclicker2_upgrade_price))
            else:
                Autoclicker2_Upgrade.config(text = "Autoclicker2 [Max]")
        else:
            Console("You don't have enough money to do that!")
    else:
        Console("Autoclicker2 already maxed out!")

def autoclicker3_upgrade():
    global shop_menu
    global autoclick_timer
    global money
    global autoclicker_reward
    global autoclicker3_reward
    global autoclicker3_upgrade_price
    global autoclicker3_level
    if autoclicker3_level <= 10:
        if money >= autoclicker3_upgrade_price:
            autoclicker3_level += 1
            money -= autoclicker3_upgrade_price
            autoclicker3_upgrade_price += int(autoclicker3_upgrade_price / 2)
            Money_Label.config(text="Money: " + str(money))
            autoclicker3_reward += 4000 * autoclicker3_level + int((autoclicker3_level / 10) + 1 * 2500)
            autoclicker_reward_refresh()
            Auto_Reward_Label.config(text="Money per second: " + str(autoclicker_reward))
            if autoclicker3_level < 11:
                Autoclicker3_Upgrade.config(text = "Upgrade Autoclicker3 [" + str(autoclicker3_level - 1) + "] | Price: " + str(autoclicker3_upgrade_price))
            else:
                Autoclicker3_Upgrade.config(text = "Autoclicker3 [Max]")
        else:
            Console("You don't have enough money to do that!")
    else:
        Console("Autoclicker3 already maxed out!")

def unlock_AU():
    Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))
    AutoUpgrader.config(text = "Auto Upgrader", bg = "#b1ff00")
    AU_unlocked == True
    print("Auto Upgrader Status: " + str(AU_unlocked))

def buy_auto_upgrader():
    global prestige_coins
    global AU_unlocked
    Console("Current pc: " + str(prestige_coins))
    print(prestige_coins)
    affordable = prestige_coins > 100
    print(affordable)
    if affordable == True:
        if AU_unlocked != True:
            prestige_coins -= 100
            unlock_AU()
            #print(AU_unlocked)
            #Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))
            #AutoUpgrader.config(text = "Auto Upgrader", bg = "#b1ff00")
            #AU_unlocked == True
        else:
            Console("Already unlocked!")
            timer = threading.Timer(5.0, clear_console)
            timer.start()
    else:
        Console("You don't have enough money to do that!")
        timer = threading.Timer(5.0, clear_console)
        timer.start()
    print("Auto Upgrader Status: " + str(AU_unlocked))
    shop_refresh()

def auto_upgrade():
    if AU_unlocked == True:
        if auto_upgrader == True:
            if money >= prestige_upgrade_price:
                prestige_upgrade()
            elif money >= autoclicker1_upgrade_price and autoclicker1_level < 11:
                autoclicker1_upgrade()
            elif money >= autoclicker2_upgrade_price and autoclicker2_level < 11:
                autoclicker2_upgrade()
            elif money >= autoclicker3_upgrade_price and autoclicker3_level < 11:
                autoclicker3_upgrade()
            elif money >= clicker_upgrade_price:
                max_clicker_upgrade()
    Game.after(100, auto_upgrade)

def max_clicker_upgrade():
    global click_reward
    global clicker_level
    global clicker_upgrade_price
    global money
    while money >= clicker_upgrade_price:
        money -= clicker_upgrade_price
        Money_Label.config(text="Money: " + str(money))
        # int(clicker_level/ int) defines an additionon extra after hitting level 10 so level / 10 = 1
        click_reward += 2 * clicker_level + int(clicker_level / 5) * 5 + int(clicker_level / 10 * 100 + int(clicker_level / 20) * 500) 
        clicker_level += 1
        clicker_upgrade_price += clicker_level * clicker_level + clicker_level * 20
        Reward_Label.config(text="Money per click: " + str(int(click_reward * prestige_multiplier)))
        ClickUpgrade.config(text = "Upgrade Clicker [" + str(clicker_level) + "] | Price: " + str(clicker_upgrade_price))
    Console("Clicker Upgrade bought! Money per click: " + str(int(click_reward * prestige_multiplier)))
    timer = threading.Timer(5.0, clear_console)
    timer.start()
    MaxClickUpgrade.config(text = "Max Upgrade Clicker [+" + str(0)  + "] | Price: " + str(0))
    
def auto_upgrader_toggle():
    global auto_upgrader
    if AU_unlocked == True:
        if auto_upgrader == True:
            auto_upgrader = False
        elif auto_upgrader == False:
            auto_upgrader = True
    else:
        Console("Not unlocked yet...")

def clicker_upgrade():
    global click_reward
    global clicker_level
    global clicker_upgrade_price
    global money
    if money >= clicker_upgrade_price:
        money -= clicker_upgrade_price
        Money_Label.config(text="Money: " + str(money))
        # int(clicker_level/ int) defines an additionon extra after hitting level 10 so level / 10 = 1
        click_reward += 2 * clicker_level + int(clicker_level / 5) * 5 + int(clicker_level / 10 * 100 + int(clicker_level / 20) * 500) 
        clicker_level += 1
        clicker_upgrade_price += clicker_level * clicker_level + clicker_level * 20
        Console("Clicker Upgrade bought! Money per click: " + str(int(click_reward * prestige_multiplier)))
        timer = threading.Timer(5.0, clear_console)
        timer.start()
        Reward_Label.config(text="Money per click: " + str(int(click_reward * prestige_multiplier)))
        ClickUpgrade.config(text = "Upgrade Clicker [" + str(clicker_level) + "] | Price: " + str(clicker_upgrade_price))
    else: 
        print("You don't have enough money to do that!")
        console_message = "You don't have enough money to do that!"
        Console_Label.config(text="Console: " + console_message)
        timer = threading.Timer(5.0, clear_console)
        timer.start()


def prestige_shop():
    print("Heyo")


bg = tk.PhotoImage(file = "bg4.gif")
background = tk.Label( Game, image = bg)
background.place(x = 0, y = 0)

Console_Label = tk.Label(text="Console: " + console_message, width = 45, height = 1, bg = "black", fg="lawn green", anchor = "w")

img = tk.PhotoImage(file = "1.png")
homebtn = tk.Button(Game, image=img, borderwidth=0, command = prestige_shop)

path = os.getcwd()
if platform.system() == "Darwin":
    pic_path = path + "/auto.png"
else:
    pic_path = path + "\\auto.png"

img2 = tk.PhotoImage(file = pic_path)
autoupgrade_btn = tk.Button(Game, image=img2, borderwidth=0, command = buy_auto_upgrader)
auto_upgrade_lbl = tk.Label(text = "Buy Auto Upgrade [100pc]")
autoupgrade_btn.pack(side= "bottom", anchor = "s", pady = 25)
auto_upgrade_lbl.pack(side = "bottom", anchor = "s", pady = 3)


Money_Label = tk.Label(bg = "#cdf9fc", text="Money: " + str(money))
Prestige_Coins_Label = tk.Label(bg = "#cdf9fc", text="Prestige Coins: " + str(prestige_coins))
Break_Label = tk.Label(text="-------------")
Break_Label2 = tk.Label(text="-------------")
Reward_Label = tk.Label(bg = "#cdf9fc", text="Money per click: " + str(int(click_reward * prestige_multiplier)))
Auto_Reward_Label = tk.Label(bg = "#cdf9fc", text="Money per second: " + str(autoclicker_reward))


ClickUpgrade = tk.Button(bg = "#cdf9fc", text = "Upgrade Clicker [1] | Price: " + str(clicker_upgrade_price), command = clicker_upgrade)

AutoUpgrader = tk.Button(bg = "#cdf9fc", text = "Auto Upgrader", command = auto_upgrader_toggle)

MaxClickUpgrade = tk.Button(bg = "#cdf9fc", text = "Max Upgrade Clicker [+" + str(max_clicker)  + "] | Price: " + str(money - max_money), command = max_clicker_upgrade)
Autoclicker1_Upgrade = tk.Button(bg = "#cdf9fc", text = "Upgrade Autoclicker1 [0] | Price: " + str(autoclicker1_upgrade_price), command = autoclicker1_upgrade)
Autoclicker2_Upgrade = tk.Button(bg = "#cdf9fc", text = "Upgrade Autoclicker2 [0] | Price: " + str(autoclicker2_upgrade_price), command = autoclicker2_upgrade)
Autoclicker3_Upgrade = tk.Button(bg = "#cdf9fc", text = "Upgrade Autoclicker3 [0] | Price: " + str(autoclicker3_upgrade_price), command = autoclicker3_upgrade)
Prestige = tk.Button(bg = "#ffd700", text = "Prestige Level ["+str(int(prestige_multiplier))+"x] | Upgrade for: " + str(prestige_upgrade_price), command = prestige_upgrade)



Prestige_Label = tk.Label(bg = "#cdf9fc", text="Prestige Multiplier: " + "None")


im = Image.open("2-2.png")
ph = ImageTk.PhotoImage(im)


ClickMe = tk.Button(image = ph , bg = "#cdf9fc", text = "Click Me", command = click, borderwidth = 0, border = -1)

Money_Label.pack()
Reward_Label.pack()
Auto_Reward_Label.pack()
Prestige_Label.pack()
Prestige_Coins_Label.pack()
ClickMe.pack(padx = 75, pady = 20)

AutoUpgrader.pack()
ClickUpgrade.pack(pady = 5)
MaxClickUpgrade.pack()
Autoclicker1_Upgrade.pack()
Autoclicker2_Upgrade.pack()
Autoclicker3_Upgrade.pack()
Prestige.pack()

ShopButton = tk.Button(text = "Boss Levels", command = bosses_popup)
ShopButton.pack()

def shop_refresh():
    global max_clicker
    max_clicker = 0
    global clicker_upgrade_price
    global click_reward
    global clicker_level
    t_clicker_level = clicker_level
    t_click_reward = click_reward
    
    t_clicker_upgrade_price = clicker_upgrade_price
    global money
    global max_money
    max_money = money
    while max_money >= t_clicker_upgrade_price:
        max_money -= t_clicker_upgrade_price
        t_click_reward += 2 * t_clicker_level + int(t_clicker_level / 5) * 5 + int(t_clicker_level / 10 * 100 + int(t_clicker_level / 20) * 500) 
        t_clicker_level += 1
        t_clicker_upgrade_price += t_clicker_level * t_clicker_level + t_clicker_level * 20
        max_clicker += 1
        MaxClickUpgrade.config(text = "Max Upgrade Clicker [+" + str(max_clicker)  + "] | Price: " + str(money - max_money))

    else: 
        pass

    global prestige_upgrade_price
    
    global autoclicker1_level
    global autoclicker2_level
    global autoclicker3_level

    global autoclicker1_upgrade_price
    global autoclicker2_upgrade_price
    global autoclicker3_upgrade_price


    if money >= prestige_upgrade_price:
        Prestige.config(bg = "#ffd700")
    else:
        Prestige.config(bg = "#809597")

    if AU_unlocked == True:
        if auto_upgrader == True:
            AutoUpgrader.config(bg = "#b1ff00", text = "Auto Upgrader [ON]")
        else:
            AutoUpgrader.config(bg = "#fb0808", text = "Auto Upgrader [OFF]")
    else:
        AutoUpgrader.config(bg = "#fb0808", text = "Not unlocked")

    if money >= clicker_upgrade_price:
        ClickUpgrade.config(bg = "#cdf9fc")
        MaxClickUpgrade.config(bg = "#cdf9fc")
    else:
        ClickUpgrade.config(bg = "#809597")
        MaxClickUpgrade.config(bg = "#809597")

    if money >= autoclicker1_upgrade_price and autoclicker1_level < 11:
        Autoclicker1_Upgrade.config(bg = "#cdf9fc")
    else:
        Autoclicker1_Upgrade.config(bg = "#809597")

    if money >= autoclicker2_upgrade_price and autoclicker2_level < 11:
        Autoclicker2_Upgrade.config(bg = "#cdf9fc")
    else:
        Autoclicker2_Upgrade.config(bg = "#809597")

    if money >= autoclicker3_upgrade_price and autoclicker3_level < 11:
        Autoclicker3_Upgrade.config(bg = "#cdf9fc")
    else:
        Autoclicker3_Upgrade.config(bg = "#809597")


    if autoclicker1_level >= 11:
        Autoclicker1_Upgrade.config(bg= "#ffd700")
    if autoclicker2_level >= 11:
        Autoclicker2_Upgrade.config(bg= "#ffd700")
    if autoclicker3_level >= 11:
        Autoclicker3_Upgrade.config(bg= "#ffd700")
    


    Game.after(100, shop_refresh)
    

def add():
    global Money_Label
    global money
    global autoclicker_reward
    global prestige_upgrade_price
    if money >= prestige_upgrade_price:
        Prestige.config(bg = "#ffd700")
    else:
        Prestige.config(bg = "#808080")
    money += autoclicker_reward
    Money_Label.config(text="Money: " + str(money))
    Game.after(1000, add)


Console_Label.pack(pady = 10)


Game.after(1000, add)
Game.after(100, shop_refresh)
Game.after(100, auto_upgrade)
Game.mainloop()