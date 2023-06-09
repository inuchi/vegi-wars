import pygame
import numpy as np
import random
import time
import math
import sys


#- - - - - - - - - - - -
# スコアを保存する関数
def save_score(score):
    with open(SCORE_FILE, "a") as file:
        file.write(str(score) + "\n")

# スコアを読み込む関数
def load_scores():
    scores = []
    try:
        with open(SCORE_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                score = int(line.strip())
                scores.append(score)
    except FileNotFoundError:
        pass
    return scores

#- - - - - - - - - - - -
# 敵の大きさに応じて音声を再生
def play_enemy_down_sound(enemy_size):
    try:
        if enemy_size == 1:
            enemy_down_sound_1.play()
        elif enemy_size == 2:
            enemy_down_sound_2.play()
        elif enemy_size == 3:
            enemy_down_sound_3.play()
        else:
            raise ValueError("Invalid enemy size: {}".format(enemy_size))
    except ValueError as ve:
        print("エラーが発生しました: {}".format(ve))
        # ここでエラーの処理を行う (例: デフォルトのサウンドを再生する、ログにエラー情報を出力するなど)

#- - - - - - - - - - - -
# スコア表示
# 引数　params = (good_score, bad_score, powerbullet_rest, player_powered_up)
            
def draw_score(screen, params, gameover):
    goodscore = params[0]
    badscore = params[1]
    bossRest = params[2]
    playerPowered_up = params[3]
    cleared = params[4]
            
    if(gameover):
        # ゲームオーバー時に文字を表示
        font = pygame.font.SysFont(None, 136)
        if(cleared==True):
            if(badscore>=0):
                text = font.render("Perfect", True, colorSCORE_inner)
            else:
                text = font.render("Cleared", True, colorSCORE_inner)
        else:   
            text = font.render("Game Over", True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 -50
        screen.blit(text, (posx, posy))
        # プラス/マイナススコア表示
        font = pygame.font.SysFont(None, 80) 
        if(badscore<0):
            text = font.render("score: "+str(goodscore)+str(badscore), True, colorSCORE_inner)
        else:
            text = font.render("score: "+str(goodscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 + 20


        screen.blit(text, (posx, posy))
        # スコアを保存, 読み出し
        totalscore = goodscore + badscore
        if(shoot_auto == False):
            save_score(totalscore)  # 自動シューティングは書き込まない
        print("totalscore="+str(totalscore))
        scores = load_scores()
        # ランキングを表示する
        scores.sort(reverse=True) # スコアを降順にソート
        rank=-1
        #print("Ranking:")
        for i, rankscore in enumerate(scores):
            #print("Rank {}: {}".format(i+1,rankscore))
            if((totalscore ==rankscore) and (rank==-1)):
                rank = i+1
        # ランク表示
        font = pygame.font.SysFont(None, 60) 
        text = font.render("rank: "+str(rank)+" / "+str(len(scores)), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 + 80
        screen.blit(text, (posx, posy))

    else:
        # 通常のスコア表示
        font = pygame.font.SysFont(None, 236) 
        text = font.render(str(goodscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 - 80
        screen.blit(text, (posx, posy))
        # 落下到達したスコア
        text = font.render(str(badscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 3 * 2 - text.get_height() // 2
        screen.blit(text, (posx, posy))
        # 弾の残り
        font = pygame.font.SysFont(None, 70) 
        text = font.render("rest= "+str(bossRest), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 5 * 1 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 5 * 4 - text.get_height() // 2
        screen.blit(text, (posx, posy))
        # 弾のレベル
        text = font.render("level= "+str(playerPowered_up), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 5 * 4 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 5 * 4 - text.get_height() // 2
        screen.blit(text, (posx, posy))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
# プレイヤーのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("files/ninjin4b.png") # プレイヤーの画像を読み込む
        self.rect = self.image.get_rect() 
        self.rect.x = 20
        self.rect.centery = HEIGHT_OF_SCREEN
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if (self.rect.centery < 0):
            self.rect.centery = 0
        if (self.rect.centery > HEIGHT_OF_SCREEN):
            self.rect.centery = HEIGHT_OF_SCREEN
        if (self.rect.centerx < 0):
            self.rect.centerx = 0
        if (self.rect.centerx >= self.rect.width*3):
            self.rect.centerx = self.rect.width*3

    def shoot(self):
        # 弾を撃つ処理をここに追加する
        pass

# 敵のクラス
class SpaceEnemy(pygame.sprite.Sprite):
    def __init__(self, type, size, speed_x=-5):
        super().__init__()
        self.type = type
        #----
        if(type == GREEN_LEAF):
            self.image = pygame.image.load('files/nin-enemy5.png')
        elif(type == BROCCOLI):
            self.image = pygame.image.load('files/blockoly-5.png')            
        else:
            self.image = pygame.image.load('files/pampkin.png')  
            self.energy = 30         
        #----
        # サイズ変形
        self.size = size
        if size == 1:
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect()
        elif size == 2:
            self.image = pygame.transform.scale(self.image, (45, 45))
            self.rect = self.image.get_rect()
        elif size == 3:            
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.rect = self.image.get_rect()
        elif size == 4:            
            self.image = pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect()
        elif size == 21:
            self.image = pygame.transform.scale(self.image, (150, 100))
            self.rect = self.image.get_rect()
        else:  # 大きい
            self.image = pygame.transform.scale(self.image, (450, 300))
            self.rect = self.image.get_rect()

        # 位置と速度
        size = self.rect.height
        if(type==BROCCOLI): #ブロッコリー
            self.rect.x = WIDTH_OF_SCREEN
            self.rect.y = random.randrange(0+size, HEIGHT_OF_SCREEN//3*2)   # 画面両端にマージン
            self.speed_x = speed_x
            if(self.rect.y < HEIGHT_OF_SCREEN//2):
                self.speed_y = 1
                #print("----speed_y:   "+str(self.speed_y))
            else: 
                self.speed_y = 0
                #print("====speed_y:   "+str(self.speed_y))
        elif(type==GREEN_LEAF): #葉っぱ
            self.rect.x = WIDTH_OF_SCREEN
            self.rect.y = random.randrange(HEIGHT_OF_SCREEN*2//3, HEIGHT_OF_SCREEN-size)   # 画面両端にマージン
            self.speed_x = speed_x
            if(self.rect.y> HEIGHT_OF_SCREEN*2//3):
                self.speed_y = -0.5
            else:
                self.speed_y = 0
        else:   # ボス
            self.rect.x = WIDTH_OF_SCREEN
            self.rect.y = random.randrange(0, HEIGHT_OF_SCREEN*2//3)   # 画面両端にマージン
            self.speed_x = speed_x
            self.speed_y = 0
        self.straight_y = self.rect.y #直進時の軌道
    def updateEnemy(self):
        # （bad スコア更新のために）敵の位置をここで更新する
        # 敵の種類による位置更新
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y 
        if(self.rect.centery > HEIGHT_OF_SCREEN-20):
            self.rect.centery = HEIGHT_OF_SCREEN - 20
        if(self.rect.centery < 20):
            self.rect.centery = 10
        if self.rect.x < 0: # 左端まできたら更新
            self.rect.x = WIDTH_OF_SCREEN
            size = self.rect.height
            if(self.type == BROCCOLI):
                self.rect.y = random.randrange(0+size, HEIGHT_OF_SCREEN//3*2)   # 画面両端にマージン
            else:
                self.rect.y = random.randrange(HEIGHT_OF_SCREEN//3*2-size)  
            # マイナス1点
            return -1
        else:
            return 0
        # 
        #(0,0) ------------------------------------------------------------------(WIDTH_OF_SCREEN, 0)
        #                                      <=enemy
        #                                    (+=speed_x)
        # player
        # (+=speed_y)
        #
        #(0, HEIGHT_OF_SCREEN)-------------------------------------(WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN)

    def bossAttacked(self):     
        # ボスを攻撃する（ボス敵限定）
        self.energy -= 1
        print("energy"+str(self.energy))
        x=self.rect.x
        y=self.rect.y
        if(self.type == BOSS_PAMPKIN):
            if(self.energy<=0):
                return DEAD        
            elif(self.energy<=3):
                self.image = pygame.image.load('files/pampkin-5.png')  
                self.image = pygame.transform.scale(self.image, (150, 100))
            elif(self.energy<=5):
                self.image = pygame.image.load('files/pampkin-3.png')  
                self.image = pygame.transform.scale(self.image, (150, 100))
            elif(self.energy<=10):
                self.image = pygame.image.load('files/pampkin-2.png')  
                self.image = pygame.transform.scale(self.image, (150, 100))
            # else
            #   何もしない
        # リセット x-y pos (サイズ変更したときのため)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        return ALIVE 
    def update(self):
        return  # なにもしない

# 敵の大きさに応じて音声を再生
def play_enemy_down_sound(enemy_size):
    if enemy_size == 1:
        enemy_down_sound_1.play()
    elif enemy_size == 2:
        enemy_down_sound_2.play()
    else:
        enemy_down_sound_3.play()

# 敵の音楽を再生
def play_bgm_sound(num):
    if num == 1:
        enemy_boss_music_1.play()
        
# 通常弾のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x=10, speed_y=0, wide = 0):
        super().__init__()
        self.image_org = pygame.image.load('files/bullet-Lw.png')  # 弾の画像
        resized_image = pygame.transform.scale(self.image_org, (10,10))
        self.image = resized_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.initial_y = x
        if((speed_x==0)and(speed_y==0)):    # もし止まっていたら
            self.speed_x = 5   # 右向きに修正
        else:
            self.speed_x = speed_x
        self.speed_y = speed_y
        self.wide = wide
    def update(self):
        if(self.wide>0):   
            # ゆらゆら
            dy = math.sin(self.rect.y / 100 * 2* math.pi) *self.wide
            self.rect.centerx += self.speed_x
            self.rect.centery = self.initial_y - dy
        else:
            # 直進
            self.rect.centerx += self.speed_x
            self.rect.centery += self.speed_y
        if(self.rect.x < 0):
            self.kill()
        elif(self.rect.x > WIDTH_OF_SCREEN):
            self.kill()
        elif(self.rect.y < 0):
            self.kill()
        elif(self.rect.y > HEIGHT_OF_SCREEN):
            self.kill()

# 拡散弾のクラス
class SplashBullet(pygame.sprite.Sprite):
    def __init__(self, x, y,numofbullet=3):
        super().__init__()        
        self.image_org =  pygame.image.load('files/bullet-Lw.png')  # 弾の画像
        self.image = pygame.transform.scale(self.image_org, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_x = 5
        self.speed_y = 5
        self.numofbullet = numofbullet
        self.timer = 0
    def update(self):
        self.timer+=1
        if((self.timer>100)):    # timer経過
            #spread
            i=0
            while(i<self.numofbullet):
                rnd_x = random.randrange(-8,13)
                rnd_y = random.randrange(-8,9)
                if((rnd_x <= -1)and(rnd_y==0)):
                   rand_x = 1   # 手前には進めない -> 右へ
                bullet = Bullet(self.rect.centerx, self.rect.centery, rnd_x, rnd_y,0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                i+=1
            self.kill()
        else:
            self.rect.centerx += self.speed_x
        
# 軌道弾のクラス
class trajectBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, param):
        super().__init__()
        self.image_org = pygame.image.load('files/bullet-Lw.png')  # 弾の画像
        resized_image = pygame.transform.scale(self.image_org, (10,10))
        self.image = resized_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.f1 = param[0]
        self.a1 = param[1]
        self.ph1 = param[2]
        self.speedx = 3
        self.x0 = x
        self.y0 = y
        self.x = 0
        self.y = 0
        #print(self.f1)
        #print(self.a1)
        #print(self.ph1)

    def update(self):
        self.x += self.speedx
        #self.rect.y = self.centery +np.sin(self.xself.f1*2*np.pi/100)*self.a1
        self.rect.x = self.x + self.x0
        a = self.a1 * (self.x / WIDTH_OF_SCREEN) 
        self.y = np.sin(self.x*np.pi/100)*a
        self.rect.y = self.y + self.y0
        if(self.rect.x > WIDTH_OF_SCREEN):
            self.kill()
# パワーアップ豆のクラス
class Bean(pygame.sprite.Sprite):
    def __init__(self,type,speed):
        super().__init__()
        if(type==GOODBEAN):
            # good
            self.image = pygame.image.load("files/beans_s.png").convert_alpha()  # 豆の画像を読み込み
        else:
            # bad
            self.image = pygame.image.load("files/beans4_bad_s.png").convert_alpha()  # 豆の画像を読み込み
        self.type=type
        self.rect = self.image.get_rect()
        if(speed >= 0):
            self.speed_x = -1
        else:
            self.speed_x = speed

    def update(self):
        self.rect.x += self.speed_x  # 豆の移動
        if(self.rect.x < 0):
            self.kill()
#---------------------------------------------
# メイン 
#---------------------------------------------
if __name__ == '__main__':

    # ゲームの初期化
    pygame.init()
    # 引数の取得
    # 自動シューティング
    args = sys.argv
    AUTO_COUNTER = 20
    if(len(args)>=2):
        if(args[1]=="1"):
            shoot_auto = True
            shoot_auto_counter = AUTO_COUNTER
        else:
            shoot_auto = False
            shoot_auto_counter = 0
        print(args[1])
    else:
        shoot_auto = False
        shoot_auto_counter = 0

    # サウンドのロード
    enemy_down_sound_1 = pygame.mixer.Sound('files/sound1.wav')
    enemy_down_sound_2 = pygame.mixer.Sound('files/sound2.wav')
    enemy_down_sound_3 = pygame.mixer.Sound('files/sound3.wav')
    enemy_boss_music_1 = pygame.mixer.Sound('files/holst_NYO-ss.mp3')
    pygame.mixer.set_num_channels(16) 

    # ウィンドウのサイズ
    WIDTH_OF_SCREEN = 1000.0
    HEIGHT_OF_SCREEN= 600.0

    # スコアを保存するファイル名
    SCORE_FILE = "scores.txt"
    screen = pygame.display.set_mode((WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN))
    pygame.display.set_caption("ベジタブルウォーズ")
    clock = pygame.time.Clock()

    # フォントの設定
    font = pygame.font.Font(None, 36)

    # 色の定義
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    # 描画色
    colorBG = (6,26,50)
    #colorSCORE_outer =(
    colorSCORE_outer = ((0,155,155),(33,188,188),(66,200,200),(155,0,250),(244,247,249),(44,248,252),(33,247,249),(155,248,252),(160,247,249),(155,248,252))
    #colorSCORE_inner = (201,243,247)
    colorSCORE_inner = (155,243,247)

    # 豆ID
    GOODBEAN = 1
    BADBEAN = 2
    # 敵ID
    GREEN_LEAF = 1
    BROCCOLI = 2
    BOSS_PAMPKIN = 21
    # 生きてる
    DEAD = 0
    ALIVE = 1
    # スプライトグループの作成
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    beans = pygame.sprite.Group()

    # プレイヤーの生成
    player = Player()
    all_sprites.add(player)

    # 敵の生成
    for i in range(10):
        e_type = random.randint(1, 3)
        if(e_type == 1):
            enemy_type = GREEN_LEAF
        else:
            enemy_type = BROCCOLI
        enemy_size = random.randint(1, 4)
        enemy_speed_x = random.randrange(-5, -2)
        enemy = SpaceEnemy(enemy_type, enemy_size, enemy_speed_x)
        all_sprites.add(enemy)
        enemies.add(enemy)
    play_bgm_sound(1)
    # ゲームループ
    running = True
    player_powered_up = 0
    good_score = 0
    bad_score = 0
    restboss = 10
    game_clear = False
    while running:
        # キー操作
        shoot = 0   # one shot
        for event in pygame.event.get():
            #print(event.type)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = 1
        #-------
        # 通常弾発射
        if(shoot_auto == True):
            shoot_auto_counter -= 1
            if(shoot_auto_counter <= 0):
                shoot = 1
                shoot_auto_counter = AUTO_COUNTER
                shoot_auto_counter += random.randrange(0,10)
            else:
                shoot = 0
                
        if(shoot == 1):
            shoot = 0
            speed = 10
            bullet = Bullet(player.rect.right, player.rect.centery,speed,0,0)
            all_sprites.add(bullet)
            bullets.add(bullet)

            # パワーアップ弾発射
            if(player_powered_up <=3):
                # ノーマルパワーアップ
                offset = -1 * player_powered_up * 5
                speed = 10
                posx = player.rect.centerx + player.rect.width / 4
                posy = player.rect.centery
                bullet = Bullet(posx, posy+offset, speed, 0, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                # ----
                offset = player_powered_up * 5
                speed = 10
                bullet = Bullet(posx, posy+offset, speed, 0, 0)
                bullets.add(bullet)
                all_sprites.add(bullet)

            if(player_powered_up >= 2):
                #軌道弾
                params = (10,160,30) #f=10, a=160
                bullet = trajectBullet(player.rect.right, player.rect.centery,params)
                all_sprites.add(bullet)
                bullets.add(bullet)

            if(player_powered_up >=10):
                # 拡散弾
                x=player.rect.right
                y=player.rect.centery
                bullet_num = player_powered_up+3  # 拡散弾の数
                bullet = SplashBullet(x, y, bullet_num)
                all_sprites.add(bullet)
                bullets.add(bullet)

                                       
        # 弾が右端まで到達したら消去
        for bullet in bullets:
            if bullet.rect.right < 0:
                bullet.kill()
        # 上下キー操作
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.speed_y = -5
        elif keys[pygame.K_DOWN]:
            player.speed_y = 5
        elif keys[pygame.K_LEFT]:
            player.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
        else:
            player.speed_y = 0

        # 全部更新
        all_sprites.update()    
        #弾の衝突判定   (future)
        # スプライトの画像を読み込み
        #sprite_image = pygame.image.load("files/nin-enemy5.png").convert_alpha()
        # スプライトの画像からマスクを生成
        #sprite_mask = pygame.mask.from_surface(sprite_image)
        #if sprite_mask.overlap(target_mask, sprite_mask):

        # Circle(丸)同士で比較
        hit_enemy = pygame.sprite.groupcollide(enemies, bullets, False, True, pygame.sprite.collide_circle_ratio(0.75))
        # 判定結果を反映
        for enemy in hit_enemy:
            # 弾があたった
            enemy_size = enemy.size
            good_score += 1
            # print("size= "+str(enemy_size)+", score= "+str(score))
            play_enemy_down_sound(enemy_size)
            if(game_clear ==False):
                if((good_score % 300)==99):
                    # ボスの生成
                    nextType = BOSS_PAMPKIN
                    size=21 # fixed
                    speed_x = -1
                    enemy_new = SpaceEnemy(nextType, size, speed_x)
                    all_sprites.add(enemy_new)
                    enemies.add(enemy_new)
                # 敵が size <= 2 のときだけ
                if(enemy.size<=2):
                    bonus = random.randrange(0, 100)
                    if(bonus <20):
                        # パワーアップ豆を追加
                        speed_x = enemy.speed_x / 3 - 1
                        if(bonus<14):
                            bean = Bean(GOODBEAN, speed_x)  # good
                        else:
                            bean = Bean(BADBEAN, speed_x)  # bad
                        bean.rect.x = enemy.rect.x
                        bean.rect.y = enemy.rect.y
                        beans.add(bean)
                        all_sprites.add(bean)
                if(enemy.type==BOSS_PAMPKIN):
                    res = enemy.bossAttacked()
                    if(res==DEAD):
                        restboss-=1

                        if(restboss<=0):
                            game_clear = True
                        enemy.kill()
                else:                
                    # 敵はすぐに右から出す
                    enemy.kill()
                    type = random.randrange(1, 3)   # 1 or 2
                    if(type==1):
                        nextType = BROCCOLI
                    else:
                        nextType = GREEN_LEAF
                    size = random.randrange(1, 4)   # 1 - 3
                    speed_x = random.randrange(-5,-2) # -5 to -3
                    # size とtype は更新
                    enemy_new = SpaceEnemy(nextType, size, speed_x)
                    all_sprites.add(enemy_new)
                    enemies.add(enemy_new)

        # 自分と敵との衝突判定
        #hits = pygame.sprite.spritecollide(player, enemies, False)
        hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle_ratio(0.6))
        if hits:
            # 敵にあたったらゲーム終了
            running = False
        if game_clear:
            running = False
            game_clear= True 
        # 自分とパワーアップ豆との当たり判定（パワーアップするかどうか）
        for bean in beans:
            if bean.rect.colliderect(player.rect):
                if(bean.type==2):
                    min = 0
                    if(player_powered_up > min):
                        player_powered_up -= 1 # パワーダウン
                        print("(down) current power= "+str(player_powered_up)+"")
                else:
                    max = 20
                    if(player_powered_up < max):
                        player_powered_up += 1 # パワーアップ
                        print("(up) current power= "+str(player_powered_up))
                bean.kill()
        # badscore の更新
        for enemy in enemies:
            minusPoint = enemy.updateEnemy()  # 敵を更新、bad 得点を取得
            bad_score += minusPoint
            #if(minusPoint < 0): # デバッグ用
                #print("bad: " + str(bad_score)+", "+str(minusPoint))
        # 描画
        screen.fill(colorBG) # 背景を塗りつぶす
        
        # 再描画
        all_sprites.draw(screen)

        # スコア表示
        if not running:
            # スコアを描画して終了
            gameend = True
            params = (good_score, bad_score, restboss, player_powered_up, game_clear)
            #print(params)
            draw_score(screen, params, gameend) #game over
            pygame.display.flip()
            # 1秒待機
            time.sleep(3)

        else:
            # 背景
            screen.fill(colorBG)
            # スコアの描画
            gameend = False
            params = (good_score, bad_score, restboss, player_powered_up, game_clear)
            draw_score(screen, params, gameend)
            # スプライトも表示    
            all_sprites.draw(screen) # スプライトを描画する
            pygame.display.flip()
        
        clock.tick(60) # フレームレートを60に設定

    print("end")
    pygame.quit() # Pygameを終了する
