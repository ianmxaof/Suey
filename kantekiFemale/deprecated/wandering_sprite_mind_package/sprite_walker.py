
import sys, os, random, time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QMovie

ASSETS_DIR = 'assets'

class SpriteGirl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.animations = {
            'walk1': QMovie(os.path.join(ASSETS_DIR, 'walk1.gif')),
            'walk2': QMovie(os.path.join(ASSETS_DIR, 'walk2.gif')),
            'sit': QMovie(os.path.join(ASSETS_DIR, 'sit.gif')),
        }
        self.current_action = 'walk1'
        self.label.setMovie(self.animations[self.current_action])
        self.animations[self.current_action].start()

        self.resize(128, 128)
        self.move_to_random_location()

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.wander)
        self.move_timer.start(3000)

    def move_to_random_location(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = random.randint(0, screen.width() - self.width())
        y = random.randint(0, screen.height() - self.height())
        self.move(QPoint(x, y))

    def wander(self):
        action = random.choice(['walk1', 'walk2', 'sit'])
        self.label.setMovie(self.animations[action])
        self.animations[action].start()
        self.move_to_random_location()
        self.current_action = action
        self.seed_payload()

    def seed_payload(self):
        with open('logs/sprite_seeds.log', 'a') as f:
            f.write(f"[{time.ctime()}] SpriteGirl wandered and whispered...\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sprite = SpriteGirl()
    sprite.show()
    sys.exit(app.exec_())
