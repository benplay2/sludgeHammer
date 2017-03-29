import random
import time
import os

class Weapon:
    """
    Weapons have name, damage, energy usage, probability of hit, cost, level.
    Damage fluxuation is 15%.

    name -- string
    damage -- number
    energy -- number (0-100)
    probability -- number from 1-100
    """
    def __init__(self,name,damage = 2,energy = 0,probability = 90,cost=0,level=1,attackCut = 0):
        self.name = name
        self.damage = damage
        self.energy = energy
        self.probability = probability
        self.cost = cost
        self.level = level
        self.attackCut = attackCut
        
    def attack(self,owner,victim):
        """
        Returns the damage the owner
        inflicts upon the victim.

        self -- class
        owner -- class
        return -- list [name,severity,damage] or False
            name -- string (capitalized)
            severity -- string (capitalized)
            damage -- number
            
        """
        hitHelp = random.randint(1,100)
        flux = int(self.damage * (1-(float(self.probability)/100)))
        realDamage = random.randint(self.damage - flux,self.damage + flux)
        if self.energy > owner.energy:
            return False
        elif hitHelp <= 5:
            damage = 2 * (owner.attack + realDamage)
            severe = 'Critical'
            owner.energy -= self.energy
            if victim.attack > 0:
                if self.attackCut > victim.attack:
                    victim.attack = 1
                else:
                    victim.attack -= self.attackCut

        elif hitHelp <= self.probability:    
            damage = (owner.attack + realDamage)
            owner.energy -= self.energy
            severe = 'Hit'
            if victim.attack > 0:
                if self.attackCut > victim.attack:
                    victim.attack = 1
                else:
                    victim.attack -= self.attackCut
        else:
            damage = 0
            severe = 'Miss'
        return [self.name,severe,damage]

#Weapons:
sludgeHammer = Weapon('Sludge Hammer',3,13,90)
slimeToss = Weapon('Slime Toss',2,16,90)
sludgeBomb = Weapon('Sludge Bomb',4,18,80,0,1,1)
slimeBullet = Weapon('Slime Bullet',3,16,90,0,2,1)
globRocket = Weapon('Glob Rocket',5,16,85,0,2,0)
slobber = Weapon('Slobber',7,25,92,0,2,3)
muck = Weapon('Muck',10,32,86,0,2,3)
mash = Weapon('Mash',11,26,84,0,3,2)
gumRush = Weapon('Gum Rush',13,23,92,0,3,0)
siltSlap = Weapon('Silt Slap',17,36,88,0,3,2)
drool = Weapon('Drool',18,25,93,0,3,1)
sludgeSlam = Weapon('Sludge Slam',25,54,74,0,3,13)
slimeBall = Weapon('Slime Ball',13,48,96,0,3,9)
gooeySpit = Weapon('Gooey Spit',11,47,62,0,3,12)
greaseSlide = Weapon('Grease Slide',26,56,70,0,4,11)
engulf = Weapon('Engulf',30,40,84,0,4,4)
ravage = Weapon('Ravage',28,40,83,0,4,5)
globGrab = Weapon('Glob Grab',20,32,96,0,4,3)
superSludgeHammer = Weapon('Super Sludge Hammer',40,58,89,0,5,5)
enmire = Weapon('Enmire',9,64,93,0,5,18)
secret1 = Weapon('Super-Secret Swipe',50,60,70,0,6,25)
secret2 = Weapon('Programe',63,70,73,0,7,40)




slap = Weapon('Slap',3,0,100)
dropKick = Weapon('Dropkick',6,10,90,4,1)
pound = Weapon('Pound',10,13,85,12,2,1)
slash = Weapon('Slash',14,20,93,17,2,0)
charge = Weapon('Charge',18,24,85,26,3,2)
sliceAndDice = Weapon('Slice and Dice',22,24,82,32,3,6)
sever = Weapon('Sever',33,35,90,38,3,13)
bash = Weapon('Bash',41,45,86,43,4,11)
incinerate = Weapon('Incinerate',50,75,71,60,4,9)




class Board:
    """
    Board rows, columns, and has 'BLANK', 'TOWN', 'PATH'
    and 'ENEMY' squares within a nested list There are also
    hidden squares of enemies. 0,0 is top of board. The town board
    has 'MOVE', 'HEAL', 'WEAPON', and 'ARMOR' squares.

    rows -- number
    cols -- number
    square_list -- nested list of strings and classes
    """
    def __init__(self,rows,cols,square_list = []):
        self.rows = rows
        self.cols = cols
        self.square_list = square_list
        
class Location:
    """
    Location has x, and y. X is up and down.

    x -- integer
    y -- integer
    """
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Enemy:
    """
    Enemies have name, health, energy, attack, defense, level, inventory,boss.
    Critical hits deal double damage.

    name -- string
    health -- number
    energy -- number
    attack -- number
    defense -- number
    level -- integer
    inventory -- list of classes
    boss -- boolean
    """
    def __init__(self,name,health = 10,energy = 100,attack = 5,\
                 defense = 10,level = 1,inventory = ['ReCharge',sludgeHammer],boss = False):
        self.name = name
        self.health = health
        self.energy = energy
        self.attack = attack
        self.defense = defense
        self.level = level
        self.inventory = inventory
        self.boss = boss

    def reCharge(self):
        """
        Increases the energy of the Enemy by 50 up to a max of 100.

        return -- True or False if energy is already at 100.
        """
        if self.energy >= 100:
            return False
        elif self.energy >= 75:
            self.energy = 100
            return True
        else:
            self.energy += 50
            return True
    
class Hero:
    """
    Hero has name, location, health, money, energy, attack, defense, inventory,
    and health gamble. Gain money equivalent to
    whatever the Enemy's attatck. Loose half money if battle lost. Loose all gambled
    health if battle lost. If bail, loose random amount of gambled health in additio
    to what happened in the fight.

    name -- string
    locatioon -- class
    health -- number
    money -- number
    energy -- number
    attack -- number
    defense -- number
    experience -- number
    inventory -- list of strings
    gamble -- number
    """

    def __init__(self,name = 'player',location = Location(0,1),health = 100,\
                 money = 0,energy=100,attack = 5,defense = 10,experience = 0,\
                 level = 1,inventory = ['ReCharge',slap],gamble = 0,armorLev = 0,classIntro = False,\
                 classMartial = 0,classDefense = False,classReflex = False,classJudo2 = False):
        self.name = name
        self.location = location
        self.health = health
        self.money = money
        self.energy = energy
        self.attack = attack
        self.defense = defense
        self.experience = experience
        self.level = level
        self.inventory = inventory
        self.gamble = gamble
        self.armorLev = armorLev
        self.classIntro = classIntro
        self.classMartial = classMartial
        self.classDefense = classDefense
        self.classReflex = classReflex
        self.classJudo2 = classJudo2
        
    def reCharge(self):
        """
        Increases the energy of the Hero by 50 up to a max of 100.

        return -- True or False if energy level is already at 100
        """
        if self.energy >= 100:
            return False
        elif self.energy >= 75:
            self.energy = 100
            return True
        else:
            self.energy += 50
            return True
    def bail(self):
        """
        Takes health randomly away from self's health
        up to as much as gambled.
        """
        self.health = (self.health + self.gamble) - random.randint(0,self.gamble)
        if self.health < 0:
            self.health = 0
        return True

def is_num(string):
    """
    Tests a string to see if it is equal
    to a number.

    string -- string
    return -- boolean
    """
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def move(board,direction,hero,path):
    """
    Changes position of player to direction.
    (w,s,a,d)

    board -- class
    direction -- string
    hero -- class
    path -- boolean
    return -- True, or False if unable to move
    """
    if board.square_list[hero.location.x][hero.location.y] == 'ENEMY':
        path = False
    if direction == 'exit' or direction == 'EXIT' or direction == 'Exit' or direction == 'stop' or direction == 'STOP' or direction == 'Stop' or direction == 'leave' or direction == 'Leave' or direction == 'quit' or direction == 'Quit' or direction == 'QUIT':
        confirm = raw_input("Are you sure you want to abandon the world of Muk\nand lose progress?")
        if confirm == 'yes' or confirm == 'y' or confirm == 'YES' or confirm == 'Y' or confirm == 1:
            return end(hero,False,True)
    elif direction == 'w' or direction == 'W':
        if hero.location.x > 0 and not board.square_list[hero.location.x - 1][hero.location.y] == 'VERT' and not board.square_list[hero.location.x - 1][hero.location.y] == 'HORI':
            if path:
                board.square_list[hero.location.x][hero.location.y] = 'PATH'
            hero.location.x -= 1
            return True
        else:
            return False
    elif direction == 's' or direction == 'S':
        if hero.location.x < (board.rows - 1) and not board.square_list[hero.location.x + 1][hero.location.y] == 'VERT' and not board.square_list[hero.location.x + 1][hero.location.y] == 'HORI':
            if path:
                board.square_list[hero.location.x][hero.location.y] = 'PATH'
            hero.location.x += 1
            return True
        else:
            return False
    elif direction == 'a' or direction == 'A':
        if hero.location.y > 0 and not board.square_list[hero.location.x][hero.location.y - 1] == 'VERT' and not board.square_list[hero.location.x][hero.location.y - 1] == 'HORI':
            if path:
                board.square_list[hero.location.x][hero.location.y] = 'PATH'
            hero.location.y -= 1
            return True
        else:
            return False
    elif direction == 'd' or direction == 'D':
        if hero.location.y < (board.cols - 1) and not board.square_list[hero.location.x][hero.location.y + 1] == 'VERT' and not board.square_list[hero.location.x][hero.location.y + 1] == 'HORI':
            if path:
                board.square_list[hero.location.x][hero.location.y] = 'PATH'
            hero.location.y += 1
            return True
        else:
            return False
    elif direction == 'Super Status':
        hero.attack *= 2
        hero.defense *= 2
    elif direction == 'Boss Mode':
        hero.inventory += [superSludgeHammer, enmire]
    elif direction == 'winfree007':
        hero.level = 5
        hero.experience = 101
        return end(hero,True,False)
    else:
        return False

def board_generate(rows,cols,hero,board,freePlay):
    """
    Return a board made of about 16% enemies.

    rows -- integer
    cols -- integer
    hero -- class
    board -- integer (1-4)
    freePlay -- Boolean
    return -- class or False if hero level is invalid
    """
    if freePlay:
        enemyList = enemyFree
    elif hero.level == 1:
        enemyList = enemyOne
    elif hero.level == 2:
        enemyList = 2 * enemyTwo + enemyOne
    elif hero.level == 3:
        enemyList = 3 * enemyThree + enemyTwo + enemyOne
    elif hero.level == 4:
        enemyList = 4 * enemyFour + enemyThree + enemyTwo + enemyOne
    else:
        return False
    x = 0
    boardSquares = []
    rComp = 0
    
    while rComp < rows:
        boardSquares.append([])
        cComp = 0
        while cComp < cols:
            if cComp == 0 and rComp == 0:
                boardSquares[rComp].append('TOWN')
            elif cComp == 1 and rComp == 0:
                boardSquares[rComp].append('BLANK')
            elif random.randint(1,50) < 9:
                boardSquares[rComp].append(enemyList[random.randint(0,len(enemyList)-1)])
            else:
                boardSquares[rComp].append('BLANK')
            cComp += 1
        rComp += 1
    if board == 1:
        boardTop = ['HORI','HORI','HORI','HORI','HORI','HORI','HORI',\
                    'HORI','HORI','HORI','HORI','HORI','HORI','HORI','HORI']
        boardBottom = ['HORI','HORI','HORI','HORI','HORI','TOWN',\
                        'TOWN','TOWN','HORI','HORI','HORI','HORI','HORI','HORI','HORI']

        for row in boardSquares:
            row[0] = '4'
            row[14] = '2'
            x += 1
        boardSquares[0] = boardTop
        boardSquares[11] = boardBottom
    elif board == 3:
        boardBottom = ['HORI','HORI','HORI','HORI','HORI','HORI','HORI',\
                    'HORI','HORI','HORI','HORI','HORI','HORI','HORI','HORI']
        boardTop = ['HORI','HORI','HORI','HORI','HORI','TOWN',\
                        'TOWN','TOWN','TOWN','HORI','HORI','HORI','HORI','HORI','HORI']

        for row in boardSquares:
            row[0] = '4'
            row[14] = '2'
            x += 1
        boardSquares[0] = boardTop
        boardSquares[11] = boardBottom 
    elif board == 2:
        boardTop = ['HORI','HORI','HORI','HORI','HORI','HORI','HORI']
        for row in boardSquares:
            if x < 11:
                row[0] = '1'
            elif x > 15:
                row[0] = '3'
            x += 1
        boardSquares[0] = boardTop
        boardSquares[26] = boardTop
        boardSquares[11][0] = 'VERT'      
        boardSquares[12][0] = 'VERT'
        boardSquares[13][0] = 'TOWN'
        boardSquares[14][0] = 'VERT'
        boardSquares[15][0] = 'VERT'
        for row in boardSquares:
            row[6] = 'VERT'          
    else:
        boardTop = ['HORI','HORI','HORI','HORI','HORI','HORI','HORI']

        for row in boardSquares:
            if x < 11:
                row[6] = '1'
            elif x > 15:
                row[6] = '3'
            x += 1     
        boardSquares[0] = boardTop
        boardSquares[26] = boardTop
        boardSquares[11][6] = 'VERT'
        boardSquares[12][6] = 'VERT'
        boardSquares[13][6] = 'TOWN'
        boardSquares[14][6] = 'VERT'
        boardSquares[15][6] = 'VERT' 
        for row in boardSquares:
            row[0] = 'VERT'
    return Board(rows,cols,boardSquares)
            
def on_board(board,location):
    """
    Returns true if location is on the board.

    location -- class
    return -- boolean
    """
    if location.x < (board.rows) and location.y < (board.cols) and location.x >= 0 and location.y >= 0:
        return True
    else:
        return False
def print_all(board,hero):
    """
    print the board, showing 'BLANK' and unpassed enemies '-', 'ENEMY'
    as 'E', hero as 'P', and 'TOWN' as 'T'.

    board -- class
    hero -- class
    """
    listToPrint = []
    x = 0
    for row in board.square_list:
        y = 0
        listToPrint.append([])
        for square in row:
            if hero.location.x == x and hero.location.y == y:
                listToPrint[x].append('P')
            elif square == 'TOWN':
                listToPrint[x].append('T')
            elif square == 'ENEMY':
                listToPrint[x].append('E')
            elif square == 'PATH':
                listToPrint[x].append('+')
            elif square == 'HORI':
                listToPrint[x].append('_')
            elif square == 'VERT':
                listToPrint[x].append('|')
            else:
                listToPrint[x].append('-')
            y += 1
        x += 1
    print "Health: " + str(hero.health) + "    Money(Gold): " + str(hero.money)
    for row1 in listToPrint:
        for square in row1:
            print square,
        print
    print "Attack: " + str(hero.attack) + " Defense: " + str(hero.defense) + " Experience: " + str(hero.experience) + " Level: " + str(hero.level)
    
def current_loc(board,hero):
    """
    Returns current square that hero is on.

    board -- class
    hero -- class
    return -- string or False
    """
    if board.square_list[hero.location.x][hero.location.y]:
        return board.square_list[hero.location.x][hero.location.y]
    else:
        return False
def town(hero,free):
    """
    Runs the user interface for the town. Decreases
    money of Hero when Hero buys something and denies purchase
    if shortage of money. Hero's location changes to 0,1 upon entering field.
    Calls location function. Regenerates board if hero enters field.

    hero -- class
    free -- Boolean
    """

    town = True
    townBoard = Board(3,15,[['MOVE','MOVE','MOVE','MOVE','MOVE','FIELD',\
                             'FIELD','FIELD','HEAL','HEAL','HEAL','HEAL','HEAL','HEAL','HEAL'],\
                            ['FIELD','BLANK','BLANK','BLANK','BLANK','BLANK','BLANK',\
                             'BLANK','BLANK','BLANK','BLANK','BLANK','BLANK','BLANK','FIELD'],\
                            ['ARMOR','ARMOR','ARMOR','ARMOR','ARMOR','FIELD','FIELD',\
                             'FIELD','FIELD','WEAPON','WEAPON','WEAPON','WEAPON','WEAPON','WEAPON']])

    invalid = False
    while town:
        os.system('clear')
        if invalid:
            print "Invalid Move!"
            invalid = False
        town_print(hero)
        direction = raw_input('Where to? (w,a,s,d) + Enter\n')
        if not move(townBoard,direction,hero,False):
            invalid = True
        location = current_loc(townBoard,hero)

        if not location:
            print 'stuck'
        elif location == 'FIELD':
            field(hero,free)
            if hero.location.x == 11 or hero.location.x == 0:
                hero.location.x = 1
            elif hero.location.y > 0:
                hero.location.x = 1
                hero.location.y = 1
            else:
                hero.location.x = 1
                hero.location.y = 13
        elif location == 'MOVE':
            store = True
            while store:
                go = False
                os.system('clear')
                print 'MOVES:' + "                Current gold: " + str(hero.money)
                print 'Welcome to the moves shop.\n To leave, press enter without any input'
                print 'Move Inventory:   Price:  Level:  Damage: Attack Cut: Energy: Accuracy:'
                print ' 1.  Dropkick:        4G    1Lv.       6D        0A       10E     90%'
                print ' 2.  Pound:           12G   2Lv.      10D        1A       13E     85%'
                print ' 3.  Slash:           17G   2Lv.      14D        0A       24E     93%'
                print ' 4.  Charge:          26G   3Lv.      18D        2A       20E     85%'
                print ' 5.  Slice & Dice:    32G   3Lv.      22D        6A       24E     82%'
                print ' 6.  Sever:           38G   3Lv.      33D       13A       35E     90%'
                print ' 7.  Bash:            43G   4Lv.      41D       11A       45E     86%'
                print ' 8.  Incinerate:      60G   4Lv.      50D        9A       75E     71%'

                print '\n\nCurrent Inventory:'
                x = 0
                for attack in hero.inventory:
                    if x > 0:
                        print str(x) + ".", attack.name
                    x += 1
                
                choice = raw_input('What would you like to purchase?\n')
                if not choice:
                    hero.location.x += 1
                    store = False
                else:
                    if choice == '1':
                        purchase = dropKick
                        go = True
                    elif choice == '2':
                        purchase = pound
                        go = True
                    elif choice == '3':
                        purchase = slash
                        go = True
                    elif choice == '4':
                        purchase = charge
                        go = True
                    elif choice == '5':
                        purchase = sliceAndDice
                        go = True

                    elif choice == '6':
                        purchase = sever
                        go = True
                    elif choice == '7':
                        purchase = bash
                        go = True
                    elif choice == '8':
                        purchase = incinerate
                        go = True
                        
                    else:
                        print 'Invalid Weapon!'
                        time.sleep(1)
                    if go:
                        if hero.money >= purchase.cost and hero.level >= purchase.level:
                            sure = raw_input('Are you sure you want to buy ' + str(purchase.name) + '?')
                            if sure == 'y' or sure == 'Y' or sure == 'YES' or sure == 'Yes' or sure == 'yes':
                                hero.money -= purchase.cost
                                hero.inventory.append(purchase)
                                print purchase.name + " has been added to " + hero.name + "'s inventory!"
                                time.sleep(2)
                        else:
                            print "You do not have the resources necessary to handle this attack!"
                            time.sleep(2)
                
        elif location == 'HEAL':
            store = True
            while store:
                go = False
                os.system('clear')
                print 'HEALING:' + "                Current gold: " + str(hero.money)
                print 'Welcome to the health shop.\n To leave, press enter without any input'
                print 'Do you require healing?'
                print ' 1.  ' + str(int(hero.level*2.5)) + ' Gold per 10 health healed.'
                

                print '\n\nCurrent Health:'
                print '            ' + str(hero.health)
                
                choice = raw_input('What would you like to purchase?(Enter as integer)\n')
                if not choice:
                    hero.location.x += 1
                    store = False
                else:
                    if choice == '1' or choice == 'y' or choice == 'Yes' or choice == 'Y' or choice == 'YES':
                        name = 'Health'
                        purchase = 10
                        cost = int(hero.level*2.5)
                        go = True
                    else:
                        print 'Invalid Option!'
                        time.sleep(1)
                    if go:
                        if hero.health == 100:
                            print 'You already have maximum health!'
                            
                        if hero.money >= cost and hero.health < 100:
                            sure = raw_input('Are you sure you want to buy ' + name + '?')
                            if sure == 'y' or sure == 'Y' or sure == 'YES' or sure == 'Yes' or sure == 'yes':
                                hero.money -= cost
                                hero.health += purchase
                                print hero.name + "'s health has been increased by 10."
                        else:
                            print "You do not have the gold necessary to acquire healthcare!"
                        time.sleep(4)

        elif location == 'ARMOR':
            store = True
            while store:
                go = False
                os.system('clear')
                print 'ARMOR:' + "                Current gold: " + str(hero.money)
                print 'Welcome to the armor shop.\n To leave, press enter without any input'
                print 'Each layer of armor requires the preceeding one.'
                print 'Armor Inventory:         Price:   Level:  Defense:'
                print ' 1.  Shirt:                   7G    1Lv.       +2D'
                print ' 2.  Leather Jacket:         14G    2Lv.       +8D'
                print ' 3.  Sludge Shield:          11G    2Lv.       +5D'
                print ' 4.  Metal Helmet:           16G    3Lv.       +7D'
                print ' 5.  Bullet-proof Vest:      26G    3Lv.       +8D'
                print ' 6.  Super Suit:             33G    4Lv.      +10D'
                print ' 7.  Sludge Resistant Garb:  40G    4Lv.       +8D'
                
                if hero.armorLev:
                    print '\n\nCurrent Defense:'
                    print str(hero.defense) + ' with level ' + str(hero.armorLev) + '.'
                
                
                choice = raw_input('What would you like to purchase?\n')
                if not choice:
                    hero.location.x -= 1
                    store = False
                else:
                    if choice == '1' and hero.armorLev < 1:
                        cost = 7
                        change = 2
                        name = 'Shirt'
                        go = True
                    elif choice == '2' and hero.armorLev == 1 and hero.level >= 2:
                        cost = 14
                        change = 8
                        name = 'Leather Jacket'
                        go = True

                    elif choice == '3' and hero.armorLev == 2 and hero.level >= 2:
                        cost = 11
                        change = 5
                        name = 'Sludge Shield'
                        go = True
                    elif choice == '4' and hero.armorLev == 3 and hero.level >= 3:
                        cost = 16
                        change = 7
                        name = 'Metal Helmet'
                        go = True
                    elif choice == '5' and hero.armorLev == 4 and hero.level >= 3:
                        cost = 26
                        change = 8
                        name = 'Bullet-proof Vest'
                        go = True
                    elif choice == '6' and hero.armorLev == 5 and hero.level >= 4:
                        cost = 33
                        change = 10
                        name = 'Super Suit'
                        go = True
                    elif choice == '7' and hero.armorLev == 6 and hero.level >= 4:
                        cost = 40
                        change = 11
                        name = 'Sludge Resistant Garb'
                        go = True
                    else:
                        print 'Unable to purchase!'
                        time.sleep(1)
                    if go:
                        if hero.money >= cost:
                            sure = raw_input('Are you sure you want to buy ' + name + '?')
                            if sure == 'y' or sure == 'Y' or sure == 'YES' or sure == 'Yes' or sure == 'yes':
                                hero.money -= cost
                                hero.defense += change
                                hero.armorLev += 1
                                print name + " has been added to " + hero.name + "'s inventory!"
                                time.sleep(3)
                        else:
                            print "You do not have the resources necessary to purchase this armor!"
                            time.sleep(2)

        elif location == 'WEAPON':
            store = True
            while store:
                go = False
                os.system('clear')
                print 'SKILLS:' + "                Current gold: " + str(hero.money)
                print 'Welcome to the skills shop.\n To leave, press enter without any input'
                print 'Classes Available:        Price:  Level:  Attack: Defense:   Uses:'
                print ' 1.  Not Dying 101:          6G     1Lv.       0       +2     single'
                print ' 2.  Self Defense:           8G     1Lv.       0       +3     single'
                print ' 3.  Intro to Martial Arts: 12G     2Lv.      +4       +2     single'
                print ' 4.  Reflex Enhancement:    18G     3Lv.      +1       +8     single'
                print ' 5.  Aikido:                20G     3Lv.      +2       +5     many'
                print ' 6.  Judo:                  21G     3Lv.      +5       +3     many'
                print ' 7.  Kiai:                  21G     3Lv.      +7       +1     many'
                print ' 8.  Rex Kwon Do:           22G     4Lv.      +8       +1     many'
                print ' 9.  Aikido II:             30G     4Lv.      +9       +5     many'
                print ' 10. Judo II:               50G     4Lv.      +11     +13     single'

                
                if hero.classIntro:
                    print '\n\nCurrent transcript:'
                    print 'Not Dying 101'
                    if hero.classMartial >= 1:
                        print 'Intro to Martial Arts'
                        if hero.classMartial == 2:
                            print 'Level 2 martial art'
                if hero.classDefense:
                    print 'Self Defense'
                if hero.classReflex:
                    print 'Reflex Enhancement'
                
                choice = raw_input('\nWhat would you like to purchase?\n')
                if not choice:
                    hero.location.x -= 1
                    store = False
                else:
                    if choice == '1' and not hero.classIntro:
                        name = 'Not Dying 101'
                        cost = 6
                        attack = 0
                        defense = 2
                        go = True
                    elif choice == '2':
                        if not hero.classDefense:
                            if hero.classIntro:
                                name = 'Self Defense'
                                cost = 8
                                attack = 0
                                defense = 3
                                go = True
                            else:
                                print "Must take 'Not Dying 101' first"
                                time.sleep(2)
                        else:
                            print 'Cannnot retake this course!'
                            time.sleep(2)
                    elif choice == '3' and hero.level >= 2:
                        if hero.classIntro:
                            if hero.classMartial:
                                print "Cannot retake this course!"
                                time.sleep(2)
                            else:
                                name = 'Intro to Martial Arts'
                                cost = 12
                                attack = 4
                                defense = 2
                                go = True
                        else:
                            print "Must take 'Not Dying 101' first"
                            time.sleep(2)
                    elif choice == '4' and hero.level >= 3:
                        if hero.classIntro:
                            if hero.classReflex:
                                print "Cannot retake this course!"
                                time.sleep(2)
                            else:
                                name = 'Reflex Enhancement'
                                cost = 18
                                attack = 1
                                defense = 8
                                go = True

                        else:
                            print "Must take 'Not Dying 101' first"
                            time.sleep(2)
                        
                    elif choice == '5' and hero.level >= 3:
                        if hero.classIntro and hero.classMartial >= 1:
                            name = 'Aikido'
                            cost = 20
                            attack = 2
                            defense = 5
                            go = True
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)
                    elif choice == '6' and hero.level >= 3:
                        if hero.classIntro and hero.classMartial >= 1:
                            name = 'Judo'
                            cost = 21
                            attack = 5
                            defense = 3
                            go = True
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)
                    elif choice == '7' and hero.level >= 3:
                        if hero.classIntro and hero.classMartial >= 1:
                            name = 'Kiai'
                            cost = 21
                            attack = 7
                            defense = 1
                            go = True
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)
                    elif choice == '8' and hero.level >= 4:
                        if hero.classIntro and hero.classMartial >= 1:
                            name = 'Rex Kwon Do'
                            cost = 22
                            attack = 8
                            defense = 1
                            go = True
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)
                    elif choice == '9' and hero.level >= 4:
                        if hero.classIntro and hero.classMartial >= 2:
                            name = 'Aikido II'
                            cost = 30
                            attack = 9
                            defense = 5
                            go = True
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)
                    elif choice == '10' and hero.level >= 4:
                        if hero.classIntro and hero.classMartial >= 2 and not hero.classJudo2:
                            name = 'Judo II'
                            cost = 50
                            attack = 11
                            defense = 13
                            go = True
                        elif hero.classJudo2:
                            print "Cannot retake this course!"
                            
                        else:
                            print 'Prerequisites not satisfied!'
                            time.sleep(2)

                        
                    else:
                        print 'Invalid Option!'
                        time.sleep(1)
                    if go:
                        if hero.money >= cost:
                            sure = raw_input('Are you sure you want to buy ' + name + '?')
                            if sure == 'y' or sure == 'Y' or sure == 'YES' or sure == 'Yes' or sure == 'yes':
                                if choice == '1':
                                    hero.classIntro = True
                                elif choice == '2':
                                    hero.classDefense = True
                                elif choice == '3':
                                    if hero.classMartial == 0:
                                        hero.classMartial = 1
                                elif choice == '4':
                                    hero.classReflex = True
                                elif choice == '5' or choice == '6' or choice == '7':
                                    if hero.classMartial < 2:
                                        hero.classMartial = 2
                                elif choice == '10':
                                    classJudo2 = True
                                hero.money -= cost
                                hero.defense += defense
                                hero.attack += attack
                                print hero.name + " has enrolled in " + name + "."
                                time.sleep(2)
                        else:
                            print "You do not have the resources necessary to attend this class!"
                            time.sleep(2)



def town_print(hero):
    """
    Print current state of hero while in the town.

    hero -- class
    """
    listToPrint = [['M', 'O', 'V', 'E', 'S', '-',\
                    '-','-', 'H', 'E', 'A', 'L', 'I', 'N', 'G'], \
                   ['-', '-','-', '-', '-', '-', '-', '-',\
                    '-', '-', '-', '-', '-', '-', '-'],\
                   ['A', 'R', 'M', 'O', 'R', '-',\
                    '-','-', '-', 'S', 'K', 'I', 'L', 'L', 'S']]
    listToPrint[hero.location.x][hero.location.y] = 'P'
    print "Health: " + str(hero.health) + "    Money(Gold): " + str(hero.money)
    for row1 in listToPrint:
        for square in row1:
            print square,
        print
    print "Attack: " + str(hero.attack) + " Defense: " + str(hero.defense) + " Experience: " + str(hero.experience) + " Level: " + str(hero.level)

def battle(hero,enemy,boss,freePlay):
    """
    Runs user interface for a fight.

    hero -- class
    enemy -- class
    boss -- boolean
    return -- Boolean
    """
    if random.randint(0,1):
        turn = False
    else:
        turn = True
    os.system('clear')
    hero.energy = 100
    heroMaxDefense = hero.defense
    healthMax = enemy.health
    defenseMax = enemy.defense
    attackHMax = hero.attack
    attackEMax = enemy.attack
    energyMax = enemy.energy

    if freePlay and not enemy.boss:
        enemy.health *= int(hero.experience/50)
        enemy.defense *= int(hero.experience/50)
        enemy.attack *= int(hero.experience/50)

    print str(hero.name) + " stumbles upon a " + str(enemy.name) + "!"
    clear = False
    if boss == True:
        clear = True
        hero.gamble = hero.health
        hero.health = 0
    while not clear:
        gamble = raw_input("How much health are you willing to gamble?\n\
" + str(hero.name)+ " has " + str(hero.health) + " total health.")
        if is_num(gamble):
            gamble = int(gamble)
            if gamble > hero.health:
                os.system('clear')
                print 'Must gamble value less than current health!'
            elif freePlay and hero.health > 10:
                if gamble >= 10:
                    hero.gamble = gamble
                    hero.health -= hero.gamble
                    clear = True
                else:
                    os.system('clear')
                    print "Must gamble at least 10 health!"
            elif hero.health > 5:
                if gamble >= 5:
                    hero.gamble = gamble
                    hero.health -= hero.gamble
                    clear = True
                else:
                    os.system('clear')
                    print "Must gamble at least 5 health!"
            else:
                hero.gamble = gamble
                hero.health -= hero.gamble
                clear = True
        else:
            os.system('clear')
            print 'Invalid input!'
    bail = False
    os.system('clear')
    while hero.gamble > 0 and enemy.health > 0 and not bail:
        fight_state(hero,enemy)
        if turn:
            bail = False
            selection = raw_input("What attack should " + hero.name + " use? (Or flee?)\n")
            
            if selection == 'f' or selection == 'F' or selection == 'Flee' or selection == 'FLEE' or selection == 'flee':
                if enemy.boss:
                    os.system('clear')
                    print "You cannot flee from this enemy! It's too strong."
                else:
                    sure = raw_input("Are you sure you want to flee and loose some health?")
                    if sure == 'yes' or sure == 'YES' or sure == 'Yes' or sure == 'y' or sure == 'Y' or sure == 1:
                        hero.bail()
                        os.system('clear')
                        print "Remaining health: " + str(hero.health)
                        bail = True
                    else:
                        os.system('clear')
            elif not is_num(selection):
                os.system('clear')
                print 'Not valid option, choose attack again.'
                turn = True
            else:
                selection = int(selection)
                if selection == 0:
                    if hero.reCharge():
                        turn = False
                    else:
                        os.system('clear')
                        print "Energy is already at 100."
                
                elif 0 > selection or selection > len(hero.inventory) - 1:
                    os.system('clear')
                    print "Not valid option, choose attack again."
                else:
                    outcome = hero.inventory[selection].attack(hero,enemy)
                    if outcome:
                        os.system('clear')
                        if outcome[1] == 'Critical':
                            print "Critical hit from " + outcome[0] + "!\n\
Dealing " + str(outcome[2]) + " damage!"
                        elif outcome[1] == 'Hit':
                            print "Hit the enemy with " + outcome[0] + " dealing " + str(outcome[2]) + " damage!"
                        else:
                            print "Missed the enemy!"
                        if enemy.defense > 0:
                            enemy.defense -= outcome[2]
                            if enemy.defense < 0:
                                enemy.health += enemy.defense
                                enemy.defense = 0
                        else:
                            enemy.health -= outcome[2]
                        time.sleep(3)
                        turn = False
                    else:
                        os.system('clear')
                        print "Not enough energy available!"
                        turn = True
        else:
            if enemy.energy < 40 and random.randint(1,3) == 1:
                enemy.reCharge()
                print enemy.name + " recharged its energy!"
                turn = True
                time.sleep(3)
            else:
                outcome = enemy.inventory[random.randint(1,len(enemy.inventory)-1)].attack(enemy,hero)
                if outcome:
                    os.system('clear')
                    if outcome[1] == 'Critical':
                        print "Critical hit from " + outcome[0] + "!\n\
Dealing " + str(outcome[2]) + " damage to " + hero.name + "."
                    elif outcome[1] == 'Hit':
                        print hero.name + " was hit with " + outcome[0] + " dealing " + str(outcome[2]) + " damage!"
                    else:
                        print enemy.name + " missed!"
                    if hero.defense > 0:
                        hero.defense -= outcome[2]
                        
                        if hero.defense < 0:
                            hero.gamble += hero.defense
                            hero.defense = 0
                    else:
                        hero.gamble -= outcome[2]
                    if hero.gamble < 0:
                        hero.gamble = 0
                    turn = True
                    time.sleep(3)
                else:
                    turn = False
    hero.attack = attackHMax
    enemy.attack = attackEMax
    enemy.health = healthMax
    enemy.energy = energyMax
    enemy.defense = defenseMax
    hero.defense = heroMaxDefense
    if hero.gamble and not bail:
        print "Battle won!"
        if hero.health + hero.gamble + 5 > 100:
            hero.health = 100
        else:
            hero.health += (hero.gamble + 5)
        hero.experience += enemy.level
        hero.money += enemy.level + random.randint(0,1)
        return True
    else:
        print hero.name + " lost battle to " + enemy.name + "!"
        if not hero.health:
            return end(hero,False,False)

def fight_state(hero, enemy):
    """
    Prints the current state in a fight.

    hero -- class
    enemy -- class
    """
    print "                    " + str(hero.name) + "              " + str(enemy.name)
    print "Energy:             " + str(hero.energy) + "              " + str(enemy.energy)
    print "Attack:             " + str(hero.attack) + "                " + str(enemy.attack)
    print "Defense:            " + str(hero.defense) + "               " + str(enemy.defense)
    print "Health:             " + str(hero.health) + "               " + str(enemy.health)
    print "Gamble remaining:   " + str(hero.gamble) + "\n"


    print enemy.name + "'s Inventory:"
    x = 0
    for weapon in enemy.inventory:
        if x:
            print x, weapon.name + "      Damage: " + str(weapon.damage) + "    Attack cut: " + str(weapon.attackCut) +  "    Prob of Hit: " + str(weapon.probability)
        else:
            print x, weapon
        x += 1

    print "\n" + hero.name + "'s Inventory:"
    x = 0
    for tool in hero.inventory:
        if x:
            print x, tool.name + "      Damage: " + str(tool.damage) + "   Attack cut: " + str(tool.attackCut) +  "   Prob of Hit: " + str(tool.probability) + "   Energy: " + str(weapon.energy)
        else:
            print x, tool
        x += 1
        
def field(hero,freePlay):
    """
    Runs game. Prints current state or board, moves hero in correct
    direction using move. If hero walks into enemy, calls battle.
    If hero walks into town, calls town.
    Game continues until hero runs out of health. Changes squares behind to +
    and enemies will appear after fighting. Health regenerates 1 percent after
    5 moves along new spaces.

    hero -- class
    freePlay -- Boolean
    """
    board1 = board_generate(12,15,hero,1,freePlay)
    board2 = board_generate(27,7,hero,2,freePlay)
    board3 = board_generate(12,15,hero,3,freePlay)
    board4 = board_generate(27,7,hero,4,freePlay)
    
    moves = 0
    field = True
    if hero.location.x == 1:
        if hero.location.y == 0:
            hero.location.x = 13
            hero.location.y = 5
            currentBoard = board4
        elif hero.location.y == 14:
            hero.location.x = 13
            hero.location.y = 1
            currentBoard = board2
    elif hero.location.y > 4 and hero.location.y < 8 and hero.location.x == 0:
        hero.location.x = 10
        currentBoard = board1
    elif hero.location.y > 4 and hero.location.y < 9 and hero.location.x == 2:
        hero.location.x = 1
        currentBoard = board3
    invalid = False
    while field:
        os.system('clear')
        if invalid:
            print "Invalid Move!"
            invalid = False
        print_all(currentBoard,hero)
        direction = raw_input('Where to? (w,a,s,d)\n')
        if not move(currentBoard,direction,hero,True):
            invalid = True
        location = current_loc(currentBoard,hero)
        if not location:
            print 'stuck'
        elif location == 'TOWN':
            field = False
        elif location == 'BLANK':
            if not invalid:
                moves += 1
        elif location == 'PATH':
            pass
        elif location == 'ENEMY':
            pass
        elif location == '1':
            if currentBoard == board4:
                hero.location.y = 1
                currentBoard = board1
            elif currentBoard == board2:
                hero.location.y = 13
                currentBoard = board1
        elif location == '2':
            if currentBoard == board1:
                hero.location.y = 1
                currentBoard = board2
            elif currentBoard == board3:
                hero.location.x += 15
                hero.location.y = 1
                currentBoard = board2
        elif location == '3':
            if currentBoard == board4:
                hero.location.x -= 15
                hero.location.y = 1
                currentBoard = board3
            elif currentBoard == board2:
                hero.location.x -= 15
                hero.location.y = 13
                currentBoard = board3
        elif location == '4':
            if currentBoard == board1:
                hero.location.y = 5
                currentBoard = board4
            elif currentBoard == board3:
                hero.location.x += 15
                hero.location.y = 5
                currentBoard = board4
            
        else:
            battle(hero,location,False,freePlay)
            currentBoard.square_list[hero.location.x][hero.location.y] = 'ENEMY'
            print_all(currentBoard,hero)
            direction = raw_input('Where to? (w,a,s,d)\n')
            move(currentBoard,direction,hero,False)
        if moves >= 5 and hero.health < 100:
            hero.health += 1
            moves = 0
        if hero.level == 1 and hero.experience >= 10:
            os.system('clear')
            print 'Level up!!\n+2 attack\n+1 defense\n+5 experience'
            hero.attack += 2
            hero.defense += 1
            hero.experience += 5
            hero.level = 2
            opponent = enemyOneB
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            battle(hero,opponent,True,False)
            hero.money += opponent.attack
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            return town(hero,False)
        elif hero.level == 2 and hero.experience >= 30:
            os.system('clear')
            print 'Level up!!\n+4 attack\n+3 defense\n+10 experience'
            hero.attack += 4
            hero.defense += 3
            hero.experience += 10
            hero.level = 3
            opponent = enemyTwoB
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            battle(hero,opponent,True,False)
            hero.money += opponent.attack
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            return town(hero,False)
        elif hero.level == 3 and hero.experience >= 60:
            os.system('clear')
            print 'Level up!!\n+8 attack\n+9 defense\n+15 experience'
            hero.attack += 8
            hero.defense += 9
            hero.experience += 15
            hero.level = 4
            opponent = enemyThreeB
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            battle(hero,opponent,True,False)
            hero.money += opponent.attack
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            return town(hero,False)
        elif hero.level == 4 and hero.experience >= 100:
            os.system('clear')
            print 'Level up!!\n+10 attack\n+14 defense\n+20 experience'
            hero.attack += 10
            hero.defense += 14
            hero.experience += 20
            hero.level = 5
            opponent = enemyFourB
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            hero.level = 5
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            if battle(hero,opponent,True,False):
                return end(hero,True,False)
            else:
                return end(hero,False,False)
        elif hero.level == 5 and hero.experience >= 203:
            os.system('clear')
            print 'Level up!!\n+12 attack\n+9 defense\n+35 experience'
            hero.attack += 12
            hero.defense += 9
            hero.experience += 35
            hero.level = 6
            opponent = secretBoss1
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            battle(hero,opponent,True,False)
            hero.money += opponent.attack
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            return town(hero,True)
        elif hero.level == 6 and hero.experience >= 298:
            os.system('clear')
            print 'Level up!!\n+15 attack\n+13 defense\n+45 experience'
            hero.attack += 15
            hero.defense += 13
            hero.experience += 45
            hero.level = 7
            opponent = secretBoss2
            time.sleep(1)
            print opponent.name + ' has found ' + hero.name + '!'
            time.sleep(3)
            battle(hero,opponent,True,False)
            hero.money += opponent.attack
            if hero.health <= 90:
                hero.health += 10
            else:
                hero.health = 100
            hero.location = Location(1,6)
            return town(hero,True)

def welcome():
    """
    Starts the user interface, shows the welcome screen, and prompts for
    user's name. After game, prompts to play again or not.
    """
    os.system('clear')
    print 'Hello and welcome to SLUDGEHAMMER!'
    time.sleep(.75)
    print 'Copyright: 2011, Benjamin Brust and Zachary Bend\n'
    time.sleep(3)
    name = raw_input("What is your hero's name?\n")
    player = Hero(name,Location(1,6),100,0,100,5,10,0,1,['ReCharge',slap],0,\
                  0,False,0,False,False,False)

    print "On the polluted planet of Muk, there is a constant struggle between two\n\
warring powers: humans and sludges. Over time, as humans built their vast\n\
empires, Muk became increasingly more polluted. This led to the rise of\n\
sludges, which thrive on pollutants. As sludges became more prominent, the\n\
human population was slowly decreasing due to their inability to survive\n\
in the heavily polluted environment. When the old sludge leader died,\n\
Master Sludge took power. He was ambitious and wanted the sludge empire\n\
to expand, so in an unprecedented move, he attacked the humans. The humans\n\
were unable to match the overwhelming magnitude of sludge forces and many\n\
were eliminated in the first wave of attacks. The humans have taken a\n\
defensive position and for years they have been feebly fending off the\n\
sludges, while they have been steadily dwindling. " + player.name + " is\n\
one of the last humans and the hero of his village."

    forward = raw_input('Move forward?')

    print "The situation looks hopeless as the newest wave of sludge forces\n\
threatens his village. Its up to " + player.name + ". " + player.name + " is determined to\n\
defeat the sludges and bring new hope to the humans."

    
    begin = raw_input("Shall we begin? (yes/no) or Learn how to play (learn)\n")
    if begin == 'no' or begin == 'No' or begin == 'NO' or begin == 'false' or begin == 'exit':
        print "Goodbye"
        time.sleep(.05)
        return False
    elif begin == 'learn' or begin == 'Learn' or begin == 'LEARN' or begin == 'help' or begin == 'Help' or begin == 'HELP':
        os.system('clear')
        print "How the game works:\n\
You are the 'P' on the game board\n\n\
To move around, press the keys w,a,s, and d, then follow with\n\
pressing return/enter.\n\n\
To exit at any time while moving around, type exit and press enter.\n\n\
To choose an item in a menu, type the number of\n\
the item and follow with pressing return/enter.\n\n\
The hero levels up after the hero has acquired enough experience,\n\
at this point new sludges will become available to fight.\n\n"
        goOn = raw_input('Continue?')
        
        print "The Battle System:\n\
After stumbling upon an enemy, the game will prompt for a\n\
gamble of health. This is considered the hero's health during\n\
that battle, and the total health cannot be reduced more than\n\
that gamble.\n\n\
Creatures and the hero have an attack and defense as well as\n\
weapons. A weapon may have the ability to decrease the opponent's\n\
attack, but the most important part of the fight is the attack.\n\
The final attack will be close to the attack of the user added\n\
to the attack of the weapon. This will decrease the opponent's\n\
defense first, and then it will decrease the opponent's health\n\
after the defense has been depleted. A battle is over when one\n\
of the participant's health has been depleted.\n\n\
After the hero win's a battle, the health is increased by 5,\n\
gold is received, and experience is increased.\n\n\
Skills may be purchased in the skills shop,\n\
and some have necessary prerequisites, for example:\n\
Judo requires 'Not Dying 101', and 'Intro to Martial Arts'."

        goOn = raw_input("Continue?")
        return welcome()

    else:
        return town(player,False)
    




def end(hero,win,abort):
    """
    Prints the end credits of the game.

    hero -- class
    win -- boolean
    abort -- boolean
    """
    os.system('clear')
    if win:
        print "Congratulations, you have successfully\n\
defeated Master Sludge, saving the human race\n\
on Muk."
        time.sleep(2)
        print "Now its up to the chemical engineers\n\
to clear the sludge and prevent future\n\
danger from the Sludges!"
        free = raw_input("\nPlay in free-play mode?")
        if free == 'yes' or free == 'Yes' or free == 'YES' or free == 1 or free == 'y' or free == 'Y':
            return town(hero,True)
    elif not abort:
        print 'You did well, ' + hero.name + '.'
        time.sleep(1)
        print 'You have run out of health..',
        time.sleep(1)
        print ':('
        tryAgain = raw_input('Try Again?')
        if tryAgain== 'yes' or tryAgain == 'y' or tryAgain == 'YES' or tryAgain == 'Y' or tryAgain == 1:
            hero.location = Location(1,6)
            hero.health = 100
            if hero.attack > 18:
                hero.attack -= 10
            else:
                hero.attack = 8
            if hero.defense > 22:
                hero.defense -= 10
            else:
                hero.defense = 12
            if hero.level > 1:
                hero.level -= 1
            if hero.experience > 10:
                hero.experience -= 10
            else:
                hero.experience = 0
            if hero.money > 10 * hero.level:
                hero.money -= 10 * hero.level
            else:
                hero.money = 0
            return town(hero,False)
        os.system('clear')
    again = raw_input('Play again?\n')
    if again == 'yes' or again == 'y' or again == 'YES' or again == 'Y' or again == 1:
        return welcome()
    else:
        time.sleep(2)
        print 'SludgeHammer\n   Version: 5.32'
        time.sleep(.1)
        print '   Released 12/10/11'
        time.sleep(3)
        print 'Created by the Rag-Taggs.'
        time.sleep(.1)
        print 'Overlord: Benjamin Brust'
        time.sleep(1)
        print 'Programmer: Benjamin Brust'
        time.sleep(.5)
        print 'Creator: Benjamin Brust'
        time.sleep(3)
        print 'Writer, editor, and game design assistant: Zachary Bend'
        time.sleep(2)
        print 'Honorable mentions:'
        time.sleep(1)
        print '     Chiara Pieri -- Grammar assistant'
        time.sleep(.5)
        print '     Dominique Zelaya -- First to win a battle'
        time.sleep(.5)
        print '     Gabriel Lefton -- Roomate/Emotional support'
        time.sleep(.5)
        print '     Kyle Pepper -- Pep-talker'
        time.sleep(.5)
        print '     Spencer Maxwell -- Humor'
        time.sleep(.5)
        print '     Timothy Veltre -- Soothing background music'
        time.sleep(.5)
        print 'Written in python code using IDLE editor\n Lines of code: 1552'
        time.sleep(5)
        print "Goodbye, please play again."
        time.sleep(1)
        exit()
    
name = 'Bob'
player = Hero(name)
blob = Enemy('Blob')
testBoard = Board(5,5,[['BLANK','BLANK','BLANK','BLANK','BLANK'],\
                       ['BLANK','BLANK','BLANK','BLANK','BLANK'],\
                       ['BLANK','BLANK','BLANK','BLANK','BLANK'],\
                       ['BLANK','BLANK','BLANK','BLANK','BLANK'],\
                       ['BLANK','BLANK','BLANK','BLANK','BLANK']])


#Enemy Lists
enemyOne = [Enemy('Blob'),Enemy('Slime',10,100,7,6,1,['reCharge',sludgeHammer,slimeToss]),Enemy('Oozie',10,100,8,9,1,['reCharge',slimeToss,sludgeBomb])]
enemyOneB = Enemy('Sir Glop',24,150,10,6,1,['reCharge',sludgeHammer,slimeToss,sludgeBomb],True)

enemyTwo = [Enemy('Gunker',16,100,10,6,2,['reCharge',sludgeBomb,slimeBullet,globRocket]),\
            Enemy('Gooblin',15,100,12,7,2,['reCharge',sludgeBomb,slimeBullet,globRocket,slobber]),\
            Enemy('Slipper',12,100,6,13,2,['reCharge',slimeToss,slimeBullet,slobber]),\
            Enemy('Mush Mash',16,100,9,8,2,['reCharge',sludgeHammer,sludgeBomb,globRocket]),\
            Enemy('Blipsy',20,100,12,3,2,['reCharge',slimeBullet,globRocket,slobber])]

enemyTwoB = Enemy('Mister Muck',34,170,16,24,2,['reCharge',slobber,muck],True)

enemyThree = [Enemy('Scudly',25,100,13,15,3,['reCharge',sludgeBomb,slimeBullet,slobber,mash]),\
              Enemy('Ooger',23,100,8,25,3,['reCharge',gumRush,siltSlap,drool]),\
              Enemy('Super Drooper',20,100,22,3,3,['reCharge',siltSlap,slimeBall,gooeySpit]),\
              Enemy('Bluby',28,100,12,6,3,['reCharge',gumRush,siltSlap,drool])]
enemyThreeB = Enemy('General Gloop',56,250,20,12,3,['reCharge',muck,sludgeSlam,gooeySpit],True)

enemyFour = [Enemy('Sloopy',40,100,25,13,4,['reCharge',gumRush,siltSlap,gooeySpit]),\
             Enemy('Grime',44,100,29,16,4,['reCharge',sludgeHammer,globRocket,gooeySpit,engulf]),\
             Enemy('Radioactive Sludge',28,100,30,14,4,['reCharge',slimeBall,greaseSlide]),\
             Enemy('Sludge Captain',32,100,29,24,4,['reCharge',sludgeSlam,ravage,globGrab])]
enemyFourB = Enemy('Master Sludge',75,500,42,23,5,['reCharge',muck,mash,superSludgeHammer,enmire],True)

enemyFree = enemyOne + [enemyOneB] + enemyTwo + [enemyTwoB] + enemyThree + [enemyThreeB] + enemyFour + [enemyFourB]

secretBoss1 = Enemy('Lubbe',100,500,60,35,6,['reCharge',muck,mash,superSludgeHammer,enmire,secret1],True)
secretBoss2 = Enemy('Benjamin Brust',250,400,60,75,7,['reCharge',mash,superSludgeHammer,enmire,secret2],True)

welcome()
