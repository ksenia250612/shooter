#Создай собственный Шутер!

from pygame import *
import random
from time import time as timer
window = display.set_mode((700, 500))#создания игрового окна
display.set_caption('шутер')#устанавливаем название окну
background = transform.scale(image.load('fon.jpg'),(700, 500))


clock = time.Clock()#создаем игровой таймер 
FPS = 60#частотa обновления экрана

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()#Вызов конструктора супер класса для активации функций спрайта
        self.image = transform.scale(image.load(player_image),(w, h))#открываем картинку и скейлим под нужные нам размеры
        self.speed = player_speed
        self.rect = self.image.get_rect()# Получение прямоугольника границ из картинки игрока для управления его позицией
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):#отобразить на экране
        window.blit(self.image,(self.rect.x, self.rect.y))#размещаешь на окне картинку и указываем в каких координатах она должна находиться

class Player(GameSprite):
    def update(self):#update нужен для того, чтобы обновлять состояние персонажа (его координаты и действия) на каждом кадре игры.
        keys_pressed = key.get_pressed()#сохраняет состояние всех клавиш 
        if keys_pressed[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        
        if keys_pressed[K_RIGHT]and self.rect.x <= 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 30)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.y = -100
            self.rect.x = random.randint(0, 610)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



class Zombi(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = random.randint(0, 610)

    
# Создаем группу монстров и добавляем в неё 5 вампиров со случайными координатами X и скоростью
monsters = sprite.Group()
for i in range(5):
    vamp = Enemy('vamp.png', random.randint(0, 610), -100, random.randint(1,3) , 90, 90 )
    monsters.add(vamp)
bullets = sprite.Group()

zombii = sprite.Group()
for i in range(3):
    zomb = Zombi('zombb.png',random.randint(0, 610), -100, random.randint(1,3) , 60, 60 )
    zombii.add(zomb)



player = Player('player.png', 200, 410, 6 , 70, 90 )#экземпляр класса


mixer.init()#подключаем и настраиваем звуковую систему
mixer.music.load('vmprr.mp3')#Загружает файл jungles.ogg в память как фоновую музыку
mixer.music.play()#Сразу начинает играть загруженную музыку
fire_ = mixer.Sound('fire.ogg')#Эта строка загружает короткий звук удара в память, чтобы его можно было быстро запустить в любой момент

font.init()
font1 = font.SysFont('Arial', 70)#Font нужен для того, чтобы выводить текст на игровой экран
font2 = font.SysFont('Arial', 30)
lost = 0 
catch = 0
num_fire = 0 
rel_time = False
finish = False
game = True#переключатель который удерживает игру в активном состоянии
while game:#отвечает за непрерывную отрисовку графики на экране, пока игра активна
    for e in event.get():#для каждого события в списке событий совершаемых пользователем
        if e.type == QUIT:#проверяет нажал ли игрок на крестик 
            game = False#если да, меняет флаг game на False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rel_time == False and num_fire <= 5:
                    player.fire()
                    num_fire += 1
                    fire_.play()
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start = timer()


    if finish != True:
        window.blit(background,(0,0))#рисует фоновое изображение 
        player.update()
        player.reset()#рисует игрока на экране в нужных координатах
        monsters.draw(window)#Рисуем всю группу монстров на игровом окне
        monsters.update()
        bullets.update()
        bullets.draw(window)
        zombii.update()
        zombii.draw(window)
        text_lose = font2.render('Пропущено:' + str(lost), 1 ,(255, 255, 255))#Создание белого текста "Пропущено: число" со сглаживанием
        text_catch = font2.render('Счёт:' + str(catch), 1 ,(255, 255, 255))
        window.blit(text_lose,(10,5))
        window.blit(text_catch,(10,25))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            catch += 1
            vamp = Enemy('vamp.png', random.randint(0, 610), -100, random.randint(1,3) , 90, 90 )
            monsters.add(vamp)
        if catch >= 10:
            finish = True
            text_win = font1.render('You win!', 1 ,(0, 255, 0))#Создание белого текста "Пропущено: число" со сглаживанием
            window.blit(text_win,(300,200))
        if lost >= 3 or sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, zombii, False):
            finish = True
            text_losse = font1.render('You lose!', 1 ,(255, 0, 0))#Создание белого текста "Пропущено: число" со сглаживанием
            window.blit(text_losse,(300,200))

        if rel_time == True:
            new = timer()
            if new - start < 3:
                text_wait = font2.render(' Wait reload!', 1 ,(255, 0, 0))#Создание белого текста "Пропущено: число" со сглаживанием
                window.blit(text_wait,(300,470))
            else:
                num_fire = 0
                rel_time = False

    clock.tick(FPS)#цикл вайл выполнился 60 раз за секунду
    display.update()#обновляем содержимое окна
