# Module Imports
from datetime import timedelta
from glob import glob
from telnetlib import GA
import tkinter as tk
import threading
from turtle import bgcolor
from apscheduler.schedulers.background import BlockingScheduler
import os
from PIL import Image, ImageTk

# Fenstereinstellungen
Game = tk.Tk()
Game.wm_title("Cookie Clicker")
Game.geometry("500x700")
Game.iconphoto(False, tk.PhotoImage(file='1.png'))

background_var = "background3.png"


# Variablen Deklarierung
max_clicker = 0
max_money = 0

money = 0
click_reward = 1
clicker_level = 1
console_message = ""

auto_upgrader = False
AU_unlocked = True
auto_prestige = False

# Prestige
prestige_level = 0
prestige_upgrade_price = 1000000
prestige_multiplier = 1

prestige_coins = 0

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

# Free Card Draw (1 per Player)
cards_free_draw = 1

# Timer for Autoclicker    
def subtimer():
    global TimerLabel
    global timer
    print(timer)
    timer -= 1
    TimerLabel.config(text = str(timer))
    Game.after(1000, subtimer)

# Makes Console(Message) possible
def Console(console_message):
    Console_Label.config(text="Console: " + console_message)

def clear_console():
    console_message = ""
    Console_Label.config(text="Console: " + console_message)

def click():
    global money
    money += click_reward * prestige_multiplier
    Money_Label.config(text="Money: " + str(money))

# Defines what happens on prestige Reset
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

        # Reset all the Button Texts
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

# Upgrading the Autoclicker
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

# Buy Auto Upgrader (which buys all available upgrades automatically)
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
            #unlock_AU()
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

# Define what the autoupgrader does (and in which order)
def auto_upgrade():
    if AU_unlocked == True:
        if auto_upgrader == True:
            if auto_prestige:
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
            else:
                if money >= autoclicker1_upgrade_price and autoclicker1_level < 11:
                    autoclicker1_upgrade()
                elif money >= autoclicker2_upgrade_price and autoclicker2_level < 11:
                    autoclicker2_upgrade()
                elif money >= autoclicker3_upgrade_price and autoclicker3_level < 11:
                    autoclicker3_upgrade()
                elif money >= clicker_upgrade_price:
                    max_clicker_upgrade()
    Game.after(100, auto_upgrade)

    
# Calculation how many Clicker Upgrades you can buy with current money
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

# Turn Auto Upgrader ON/OFF
def auto_upgrader_toggle():
    global auto_upgrader
    if AU_unlocked == True:
        if auto_upgrader == True:
            auto_upgrader = False
        elif auto_upgrader == False:
            auto_upgrader = True
    else:
        Console("Not unlocked yet...")

# Include Prestige Level in Autoupgrader
def auto_upgrader_prestige():
    global auto_prestige
    if auto_prestige == True:
        auto_prestige = False
    elif auto_prestige == False:
        auto_prestige = True
    else:
        Console("Not unlocked yet...")

# Upgrade Player Click Power
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

text_card_draw = "Free Card Draw Available!"

# Making the Shop Menu
def shop_popup():

    # Save Prestige Coins
    f = open("prestige_coins.txt", "w")
    f.write(str(prestige_coins))
    f.close()


    shop = tk.Toplevel()
    shop.title("Prestige Coin Shop")

    shop.geometry("400x600")

    bg = tk.PhotoImage(file = "bg4.gif")
    background = tk.Label(shop, image = bg)
    background.place(x = 0, y = 0)

    pc_shop_Label = tk.Label(shop, text = "[[[[[PRESTIGE COIN SHOP]]]]]")
    pc_shop_Label.pack()

    pc_Label = tk.Label(shop, text = "Prestige Coins: " + str(prestige_coins))
    pc_Label.pack()

    cookieWar_Label = tk.Label(shop, text = "[[[[[Cookie War Bet]]]]]")
    cookieWar_Label.pack()

    Bet_Label = tk.Label(shop, text = "Place your bet F(ork), M(ilk), C(ookie): ")
    Bet_Label.pack()
    cW_Bet = tk.Entry(shop)
    cW_Bet.pack()
    Bet_PCs = tk.Label(shop, text = "How many Prestige Coins do you want to bet?")
    Bet_PCs.pack()
    cW_Amount = tk.Entry(shop)
    cW_Amount.pack()

    Last_Bet = tk.Label(shop, text = "")
    Last_Bet.pack()

    # Saving Bet in TXT
    f = open("bet.txt", "w")
    f.write(str(cW_Bet.get()))
    f.close()  

    # Launch Cookie War
    def cookie_war():

        global prestige_coins

        if cW_Bet.get() != "" and cW_Bet.get() != "":

            if prestige_coins < int(cW_Amount.get()):
                PC_Console_Label.config(text = "Console: Not enough prestige coins")
            else:
                
                prestige_coins -= int(cW_Amount.get())
                pc_Label.config(text = str("Prestige Coins: " + str(prestige_coins)))
                Prestige_Coins_Label.config(text = str("Prestige Coins: " + str(prestige_coins)))

                # Saving Bet in TXT
                f = open("bet.txt", "w")
                f.write(str(cW_Bet.get()))
                f.close()

                # Saving Amount in TXT
                f = open("amount.txt", "w")
                f.write(str(cW_Amount.get()))
                f.close()

                os.system('CookieWar\main.py')

                f = open("CookieWar\won.txt", "r")
                content = f.readline()
                f.close() 
                last_bet = str(content)

                if last_bet == "won":
                    Last_Bet.config(text = "You Won (" + str(int(cW_Amount.get()) * 4) + ")!")
                    prestige_coins += int(cW_Amount.get()) * 4
                    pc_Label.config(text = str(prestige_coins))
                    Prestige_Coins_Label.config(text="Prestige Coins: " + str(prestige_coins))
                elif last_bet == "lost":
                    Last_Bet.config(text = "Lost!")

        else:
            PC_Console_Label.config(text = "Console: Please Enter your Bet!")

    cookieWar = tk.Button(shop, text ="Start a Cookie War!", command = cookie_war)  
    cookieWar.pack()

    # Launch Card Drawing
    def cookie_cards():
        pc_path = (os.path.dirname(__file__) + "\\cards/rew_pc.txt")
        money_path = (os.path.dirname(__file__) + "\\cards/cookies.txt")
        global cards_free_draw
        global money
        global prestige_coins
        global text_card_draw
        if cards_free_draw > 0:
            cards_free_draw -= 1
            f = open(money_path, "w")
            f.write(str(int(money)))
            f.close()

            os.system('cards\Karten_Aufdecken.py')

            text_card_draw = "Draw some Cards! (20pc)"

            f = open(money_path)
            new_money = int(f.readline())
            f.close()
            money = new_money

            f = open(money_path, "w")
            f.write(str(0))
            f.close()

            f = open(pc_path)
            content = int(f.readline())
            f.close()
            print("PC TO BE ADDED: " + str(content))
            prestige_coins += content
            print("Current amount of pc: " + str(prestige_coins))

            f = open(pc_path, "w")
            f.write(str(0))
            f.close()

            Money_Label.config(text = "Money: " + str(money))
            Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))
            shop.quit()




        elif prestige_coins >= 20:
            f = open(money_path, "w")
            f.write(str(int(money)))
            f.close()
            prestige_coins -= 20
            pc_Label.config(text = str(prestige_coins))
            Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))

            os.system('cards\Karten_Aufdecken.py')

            f = open(money_path)
            new_money = int(f.readline())
            f.close()
            money = new_money

            f = open(money_path, "w")
            f.write(str(0))
            f.close()

            f = open(pc_path)
            content = int(f.readline())
            f.close()
            print("PC TO BE ADDED: " + str(content))
            prestige_coins += content
            print("Current amount of pc: " + str(prestige_coins))

            f = open(pc_path, "w")
            f.write(str(0))
            f.close()

            Money_Label.config(text = "Money: " + str(money))
            Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))

            shop.destroy()
            shop.update()

        else:
            PC_Console_Label.config(text = "You don't have enough prestige coins!")
    
    # Launch Cookie Collecting Minigame
    def cookie_rain():
        global money
        global prestige_coins 
        if prestige_coins >= 10:
            prestige_coins -= 10
            pc_Label.config(text = str(prestige_coins))
            Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))
            money_path = (os.path.dirname(__file__) + '/cookies.txt')

            f = open("cookies.txt", "w")
            f.write(str(money))
            f.close()

            os.system('Cookierain\cookierain.py')

            f = open(money_path)
            money = int(f.readline())
            f.close()
            Money_Label.config(text = "Money: " + str(money))
        else:
            PC_Console_Label.config(text = "You don't have enough prestige coins!")

    cookieCards = tk.Button(shop, text =text_card_draw, command = cookie_cards)

    if text_card_draw == "Free Card Draw Available!":
        cookieCards.config(bg = "#b1ff00")
    else:
        cookieCards.config(bg = "#F0F0F0")

    #cookieCards = tk.Button(shop, text ="Draw some Cards! (20pc)", command = cookie_cards)  
    cookieCards.pack()
    cookieCards = tk.Button(shop, text ="Catch some Cookies! (10pc)", command = cookie_rain)  
    cookieCards.pack()

    PC_Console_Label = tk.Label(shop, text = "Console: ")
    PC_Console_Label.pack()

    Break_Label = tk.Label(shop, text = "")
    Break_Label.pack()

    auto_upgrader_purchase = tk.Button(shop, text = "Buy Autoupgrader! (100pc)")
    auto_upgrader_purchase.pack()

    def shop_close():
        shop.destroy()
        shop.update()

    shop_exit = tk.Button(shop, text = "Return to Game", command = shop_close)
    shop_exit.pack()  

    cookieCards.pack()

    # Unlock Autoupgrader
    def unlock_AU():
        global prestige_coins 
        global AU_unlocked
        if prestige_coins >= 100:
            prestige_coins -= 100
            Prestige_Coins_Label.config(text = "Prestige Coins: " + str(prestige_coins))
            pc_Label.config(text = str("Prestige Coins: " + str(prestige_coins)))
            AU_unlocked = True
            auto_upgrader_purchase.config(text = "Auto Upgrader unlocked", bg = "#b1ff00")
            AutoUpgrader.config(text = "Auto Upgrader", bg = "#b1ff00")
            print("Auto Upgrader Status: " + str(AU_unlocked))
        else:
            PC_Console_Label.config(text = "You don't have enough prestige coins!")

    auto_upgrader_purchase.config(command = unlock_AU)


    shop.mainloop()

# Setting up the main screen
bg = tk.PhotoImage(file = "bg4.gif")
background = tk.Label( Game, image = bg)
background.place(x = 0, y = 0)

Console_Label = tk.Label(text="Console: " + console_message, width = 45, height = 1, bg = "black", fg="lawn green", anchor = "w")

path = os.getcwd()
pic_path = path + "\\shop3.png"

img2 = tk.PhotoImage(file = pic_path)
shop_btn = tk.Button(Game, image=img2, borderwidth=0, command = shop_popup)
shop_btn.pack(side= "bottom", anchor = "s", pady = 25)

Money_Label = tk.Label(bg = "#cdf9fc", text="Money: " + str(money))
Prestige_Coins_Label = tk.Label(bg = "#cdf9fc", text="Prestige Coins: " + str(prestige_coins))
Break_Label = tk.Label(text="-------------")
Break_Label2 = tk.Label(text="-------------")
Reward_Label = tk.Label(bg = "#cdf9fc", text="Money per click: " + str(int(click_reward * prestige_multiplier)))
Auto_Reward_Label = tk.Label(bg = "#cdf9fc", text="Money per second: " + str(autoclicker_reward))


ClickUpgrade = tk.Button(bg = "#cdf9fc", text = "Upgrade Clicker [1] | Price: " + str(clicker_upgrade_price), command = clicker_upgrade)

AutoUpgrader = tk.Button(bg = "#cdf9fc", text = "Auto Upgrader", command = auto_upgrader_toggle)
AutoPrestige = tk.Button(bg = "#cdf9fc", text = "Include Prestige", command = auto_upgrader_prestige)

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
AutoPrestige.pack()
ClickUpgrade.pack(pady = 5)
MaxClickUpgrade.pack()
Autoclicker1_Upgrade.pack()
Autoclicker2_Upgrade.pack()
Autoclicker3_Upgrade.pack()
Prestige.pack()

# Refreshing all the Shop Elements (Text & Colors)
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

    Money_Label.config(text= "Money: " + "{:,}".format(money))

    global prestige_upgrade_price
    
    global autoclicker1_level
    global autoclicker2_level
    global autoclicker3_level

    global autoclicker1_upgrade_price
    global autoclicker2_upgrade_price
    global autoclicker3_upgrade_price


    if money >= prestige_upgrade_price:
        Prestige.config(bg = "#ffd700", text = "Prestige Level ["+str(int(prestige_multiplier))+"x] | Upgrade for: " + str(prestige_upgrade_price) + " | PC: +" + str(int(money/prestige_upgrade_price)))
    else:
        Prestige.config(bg = "#809597")

    if AU_unlocked == True:
        if auto_upgrader == True:
            AutoUpgrader.config(bg = "#b1ff00", text = "Auto Upgrader [ON]")
        else:
            AutoUpgrader.config(bg = "#fb0808", text = "Auto Upgrader [OFF]")
    else:
        AutoUpgrader.config(bg = "#fb0808", text = "Not unlocked")
    
    if AU_unlocked == True:
        if auto_prestige == True:
            AutoPrestige.config(bg = "#b1ff00", text = "Prestige included")
        else:
            AutoPrestige.config(bg = "#fb0808", text = "Prestige excluded")
    else:
        AutoPrestige.config(bg = "#fb0808", text = "Unlock Auto Upgrader first")

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
    
# This is how the Autoclickers make money
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


# Running all the loops
Game.after(1000, add)
Game.after(100, shop_refresh)
Game.after(100, auto_upgrade)
Game.mainloop()