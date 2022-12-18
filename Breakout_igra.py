import pygame
from pygame.locals import *

pygame.init()

zaslon_širina = 600
zaslon_višina = 600

zaslon = pygame.display.set_mode((zaslon_širina, zaslon_višina))
pygame.display.set_caption('Breakout')

# nastavi pisavo
pisava = pygame.font.SysFont("Ariel", 30)

# barva ozadja
ozadje = (128, 138, 135)
# barve brickov
brick_oranžen = (255, 97, 3)
brick_zelen = (0, 100, 30)
brick_moder = (69, 177, 232)
# barva odbijača
odbijač_barva = (0, 0, 0)
# barva teksta
tekst_barva = (78, 81, 139)

# spremenljivke igre
stolpci = 6
vrste = 6
fps = 60
ura = pygame.time.Clock()
igra_teče = False
konec_igre = 0


# funkcija za risanje teksta na zaslon
def nariši_tekst(tekst, pisava, tekst_barva, x, y):
    slika = pisava.render(tekst, True, tekst_barva)
    zaslon.blit(slika, (x, y))


# zid iz brickov
class zid():
    def __init__(self):
        self.širina = zaslon_širina // stolpci
        self.višina = 50

    def naredi_zid(self):
        self.bricks = []
        # prazna lista za posamezen brick
        brick_individualen = []
        for vrsta in range(vrste):
            # resetira vrsto
            brick_vrsta = []
            # gre čez vsak stolpec v tisti vrsti
            for stolpec in range(stolpci):
                # x in y pozicije, kreiranje kvadra
                brick_x = stolpec * self.širina
                brick_y = vrsta * self.višina
                kvader = pygame.Rect(brick_x, brick_y, self.širina, self.višina)
                # moč bricka glede na število vrste v kateri je
                if vrsta < 2:
                    moč = 3
                elif vrsta < 4:
                    moč = 2
                elif vrsta < 6:
                    moč = 1
                # lista, ki shrani kvader in njegovo barvo
                brick_individualen = [kvader, moč]
                # dodajanje tega bricka k vrsti
                brick_vrsta.append(brick_individualen)
            # doda vrsto k celi listi brickov
            self.bricks.append(brick_vrsta)

    def nariši_zid(self):
        for vrsta in self.bricks:
            for brick in vrsta:
                # doda barvo bricku glede na moč
                if brick[1] == 3:
                    brick_stolpec = brick_moder
                elif brick[1] == 2:
                    brick_stolpec = brick_zelen
                elif brick[1] == 1:
                    brick_stolpec = brick_oranžen
                pygame.draw.rect(zaslon, brick_stolpec, brick[0])
                pygame.draw.rect(zaslon, ozadje, (brick[0]), 2)


# kreiranje spodnjega kvadra (od katerega se žoga odbija)
class odbijač():
    def __init__(self):
        self.reset()


    def premikanje(self):
        # resetira smer premikanja
        self.smer = 0
        tipka = pygame.key.get_pressed()
        if tipka[pygame.K_LEFT] and self.kvader.left > 0:
            self.kvader.x -= self.hitrost
            self.smer = -1
        if tipka[pygame.K_RIGHT] and self.kvader.right < zaslon_širina:
            self.kvader.x += self.hitrost
            self.smer = 1

    def nariši(self):
        pygame.draw.rect(zaslon, odbijač_barva, self.kvader)

    def reset(self):
        # spremenljivke odbijača
        self.višina = 20
        self.širina = zaslon_širina // stolpci
        self.x = zaslon_širina // 2 - self.širina // 2
        self.y = zaslon_višina - (self.višina * 2)
        self.hitrost = 8
        self.kvader = Rect(self.x, self.y, self.širina, self.višina)
        self.smer = 0


# žoga
class žoga_igra():
    def __init__(self, x, y):
        self.reset(x, y)

    def premikanje(self):

        # prag za stik (5 pikslov)
        prag_stika = 5

        # začnemo s tem, da je zid uničen
        zid_uničen = 1
        št_vrst = 0
        for vrsta in zid.bricks:
            št_stvari = 0
            for stvar in vrsta:
                # pogleda, če je stik
                if self.kvader.colliderect(stvar[0]):
                    # pogleda, če je stik od zgoraj
                    if abs(self.kvader.bottom - stvar[0].top) < prag_stika and self.hitrost_y > 0:
                        self.hitrost_y *= -1
                        self.točke += 1
                    # pogleda, če je stik od spodaj
                    if abs(self.kvader.top - stvar[0].bottom) < prag_stika and self.hitrost_y < 0:
                        self.hitrost_y *= -1
                        self.točke += 1
                    # pogleda, če je stik iz leve strani
                    if abs(self.kvader.right - stvar[0].left) < prag_stika and self.hitrost_x > 0:
                        self.hitrost_x *= -1
                        self.točke += 1
                    # pogleda, če je stik iz desne strani
                    if abs(self.kvader.left - stvar[0].right) < prag_stika and self.hitrost_x < 0:
                        self.hitrost_x *= -1
                        self.točke += 1
                    # zmanjša moč bricka, ki je bil zadet
                    if zid.bricks[št_vrst][št_stvari][1] > 1:
                        zid.bricks[št_vrst][št_stvari][1] -= 1
                    else:
                        zid.bricks[št_vrst][št_stvari][0] = (0, 0, 0, 0)
                # pogleda, če brick še vedno obstaja (v tem primeru zid še obstaja)
                if zid.bricks[št_vrst][št_stvari][0] != (0, 0, 0, 0):
                    zid_uničen = 0
                # poveća št_stvari
                št_stvari += 1
            # Poveča št. vrst
            št_vrst += 1
        # ko pogleda vse bricke, pogleda, če je zid uničen
        if zid_uničen == 1:
            self.konec_igre = 1

        # pogleda, če se žoga stika z zidom
        if self.kvader.left < 0 or self.kvader.right > zaslon_širina:
            self.hitrost_x *= -1

        # pogleda, če se žoga dotika dna ali stropa
        if self.kvader.top < 0:
            self.hitrost_y *= -1
        if self.kvader.bottom > zaslon_višina:
            self.konec_igre = -1

        # pogleda, če se žoga stika z odbijačem
        if self.kvader.colliderect(igra_odbijač.kvader):
            # pogleda, če se stika z vrhom
            if abs(self.kvader.bottom - igra_odbijač.kvader.top) < prag_stika and self.hitrost_y > 0:
                self.hitrost_y *= -1
                self.hitrost_x += igra_odbijač.smer
                if self.hitrost_x > self.hitrost_max:
                    self.hitrost_x = self.hitrost_max
                elif self.hitrost_x < 0 and self.hitrost_x < -self.hitrost_max:
                    self.hitrost_x = -self.hitrost_max
            else:
                self.hitrost_x *= -1

        self.kvader.x += self.hitrost_x
        self.kvader.y += self.hitrost_y

        return self.konec_igre

    def nariši(self):
        pygame.draw.circle(zaslon, odbijač_barva, (self.kvader.x + self.žoga_premer, self.kvader.y + self.žoga_premer), self.žoga_premer)

    def reset(self, x, y):
        self.žoga_premer = 10
        self.x = x - self.žoga_premer
        self.y = y
        self.kvader = Rect(self.x, self.y, self.žoga_premer * 2, self.žoga_premer * 2)  # kvader bo bil samo "hitbox"
        self.hitrost_x = 4
        self.hitrost_y = -4  # -4 je zaradi tega, ker hočemo, da na začetku žogo vrže gor, ne dol
        self.hitrost_max = 5
        self.konec_igre = 0
        self.točke = 0      # št točk je mišljeno kot koliko skupne moči je bilo zbito brickom


# kreira zid
zid = zid()
zid.naredi_zid()

# kreiraj odbijač
igra_odbijač = odbijač()

# kreiraj žogo
žoga = žoga_igra(igra_odbijač.x + (igra_odbijač.širina // 2), igra_odbijač.y - igra_odbijač.višina)

izvajanje = True
while izvajanje:

    ura.tick(fps)
    zaslon.fill(ozadje)

    # nariše vse
    zid.nariši_zid()
    igra_odbijač.nariši()
    žoga.nariši()
    if igra_teče:
        # nariše odbijač
        igra_odbijač.premikanje()

        # nariše žogo
        konec_igre = žoga.premikanje()
        if konec_igre != 0:
            igra_teče = False

    # napiše instrukcije za igralca
    if not igra_teče:
        if konec_igre == 0:
            nariši_tekst("Klikni kjerkoli, da se igra začne", pisava, tekst_barva, 100, zaslon_višina // 2 + 100)
        elif konec_igre == 1:
            nariši_tekst("Zmagal si!", pisava, tekst_barva, 100, zaslon_višina // 2 + 50)
            nariši_tekst("Klikni kjerkoli, da se igra začne", pisava, tekst_barva, 100, zaslon_višina // 2 + 100)
            nariši_tekst("Št. doseženih točk: " + str(žoga.točke), pisava, tekst_barva, 100, zaslon_višina // 2 + 150)
        elif konec_igre == -1:
            nariši_tekst("Izgubil si!", pisava, tekst_barva, 100, zaslon_višina // 2 + 50)
            nariši_tekst("Klikni kjerkoli, da se igra začne", pisava, tekst_barva, 100, zaslon_višina // 2 + 100)
            nariši_tekst("Št. doseženih točk: " + str(žoga.točke), pisava, tekst_barva, 100, zaslon_višina // 2 + 150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            izvajanje = False
        if event.type == pygame.MOUSEBUTTONDOWN and igra_teče == False:
            igra_teče = True
            žoga.reset(igra_odbijač.x + (igra_odbijač.širina // 2), igra_odbijač.y - igra_odbijač.višina)
            igra_odbijač.reset()
            zid.naredi_zid()

    nariši_tekst(str(žoga.točke), pisava, tekst_barva, zaslon_širina - 75, zaslon_višina // 2 + 150)
    pygame.display.update()

pygame.quit()
