
import tkinter as tk

# ==========================================
# CLASS GAME OBJECT
# Class dasar untuk semua objek dalam game
# ==========================================

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


# ==========================================
# CLASS BALL
# Mengatur bola dalam permainan
# ==========================================

class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10

        # TAMBAHAN: Bola berwarna emas dengan garis putih
        item = canvas.create_oval(
            x-self.radius, y-self.radius,
            x+self.radius, y+self.radius,
            fill='#FFD700',
            outline='white',
            width=2
        )

        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1

        if coords[1] <= 0:
            self.direction[1] *= -1

        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed

        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5

        if len(game_objects) > 1:
            self.direction[1] *= -1

        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()

            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


# ==========================================
# CLASS PADDLE
# Mengatur papan pemantul bola
# ==========================================

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None

        # TAMBAHAN: Paddle berwarna cyan
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill='#00FFFF',
            outline='white',
            width=2
        )

        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)

            if self.ball is not None:
                self.ball.move(offset, 0)


# ==========================================
# CLASS BRICK
# Mengatur warna dan ketahanan brick
# ==========================================

class Brick(GameObject):

    # TAMBAHAN: Variasi enam warna brick
    COLORS = {
        1: '#FF4757',  # Merah
        2: '#1E90FF',  # Biru
        3: '#FFA502',  # Oranye
        4: '#2ED573',  # Hijau
        5: '#A55EEA',  # Ungu
        6: '#FF6B81'   # Pink
    }

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits

        color = Brick.COLORS[hits]

        # TAMBAHAN: Brick memiliki garis tepi putih
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=color,
            outline='white',
            width=2,
            tags='brick'
        )

        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1

        if self.hits <= 0:
            self.delete()
        else:
            # Warna brick berubah sesuai sisa ketahanan
            self.canvas.itemconfig(
                self.item,
                fill=Brick.COLORS[self.hits]
            )


