from pygame import*
import random
# фонова музика
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')

#шрифти і написи
font.init()
font2 = font.Font(None, 36)

#змінні для лічильників
lost = 0 #пропущено тарілок
score = 0 #збито тарілок

#картинки
img_back = "cosmos.jpg"  # фон гри
img_hero = "rocket.png"  # герой
img_bullet = "bullet.png" # куля
img_enemy = "ufo.png"  # ворог

#клас-батько (суперклас) для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale( image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.y, 5, 20, 15)
        Bullets.add(bullet)

#клас спрайта-ворога
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.y=0
            self.rect.x = random.randint(0, win_width - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


Bullets = sprite.Group()



# створюємо віконце
win_width = 1000
win_height = 800
display.set_caption("Shooter")

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy(img_enemy, random.randint(0, win_width - 80), -40, 80, 50, random.randint(1, 5))
    enemies.add(enemy)


#Ігровий цикл
finish = False
game = True 
while game:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key ==K_SPACE:
                ship.fire()
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        #пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), True, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render("Пропущено: " + str(lost), True, (255,255,255))
        window.blit(text_lose, (10,50))
         
        win = font2.render('YOU WIN!', True, (0, 255, 0))
        lose = font2.render('YOU LOSE!', True, (180, 0, 0))
        
        # рухи спрайтів
        ship.update()
        enemies.update()
        Bullets.update()
        Bullets.draw(window)
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.draw()
        enemies.draw(window)

        if lost >= 3 or sprite.spritecollide(ship,enemies, False):
            finish = True
            window.blit(lose,(425,400))

        if score == 10:
            finish = True
            window.blit(win,(425,400))
        killed_enemy = sprite.groupcollide(enemies, Bullets, True,True)
        for k in killed_enemy:
            score+= 1
            enemy = Enemy("ufo.png", random.randint(0,920), -20, 100, 60, random.randint(1,4))
            enemies.add(enemy)
        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(20)
