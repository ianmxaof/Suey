"""Suey's original transparent PyQt sprite, connected to the validated pet art."""
import argparse
from pathlib import Path
import random
import sys
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QWidget

BASE_DIR=Path(__file__).resolve().parent
ASSETS_DIR=BASE_DIR/'assets'

class SpriteGirl(QWidget):
    def __init__(self, wander=True):
        super().__init__()
        self.setWindowTitle('Suey')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(192,208)
        self.label=QLabel(self)
        self.label.setGeometry(0,0,192,208)
        self.animations={}
        for action,filename in [('walk1','walk1.gif'),('walk2','walk2.gif'),('sit','sit.gif')]:
            movie=QMovie(str(ASSETS_DIR/filename))
            movie.setCacheMode(QMovie.CacheAll)
            if not movie.isValid():
                raise RuntimeError(f'Missing or invalid animation: {ASSETS_DIR/filename}')
            self.animations[action]=movie
        self.current_action='sit'
        self.set_action('sit')
        self.move_to_random_location()
        self.drag_offset=None
        self.move_timer=QTimer(self)
        self.move_timer.timeout.connect(self.wander)
        if wander: self.move_timer.start(3000)

    def set_action(self,action):
        self.animations[self.current_action].stop()
        self.current_action=action
        self.label.setMovie(self.animations[action])
        self.animations[action].start()

    def move_to_random_location(self):
        area=QApplication.primaryScreen().availableGeometry()
        x=random.randint(area.left(),max(area.left(),area.right()-self.width()+1))
        y=random.randint(area.top(),max(area.top(),area.bottom()-self.height()+1))
        self.move(QPoint(x,y))

    def wander(self):
        self.set_action(random.choice(['walk1','walk2','sit']))
        self.move_to_random_location()

    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.drag_offset=event.globalPos()-self.pos()
            self.move_timer.stop()
            event.accept()

    def mouseMoveEvent(self,event):
        if self.drag_offset is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos()-self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self,event):
        self.drag_offset=None

    def contextMenuEvent(self,event):
        menu=QMenu(self)
        resume=menu.addAction('Wander')
        pause=menu.addAction('Stay here')
        menu.addSeparator()
        quit_action=menu.addAction('Quit Suey')
        selected=menu.exec_(event.globalPos())
        if selected==resume: self.move_timer.start(3000)
        elif selected==pause:
            self.move_timer.stop()
            self.set_action('sit')
        elif selected==quit_action: self.close()

    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape: self.close()
        else: super().keyPressEvent(event)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke-test',action='store_true')
    args=parser.parse_args()
    app=QApplication(sys.argv[:1])
    sprite=SpriteGirl(wander=not args.smoke_test)
    sprite.show()
    if args.smoke_test:
        for action,movie in sprite.animations.items():
            movie.jumpToFrame(0)
            assert movie.currentPixmap().size().width()==192,action
            assert movie.currentPixmap().size().height()==208,action
            assert movie.frameCount()>1,action
        print('Suey loaded: 3 transparent animated GIFs, 192x208, valid Qt movies.',flush=True)
        QTimer.singleShot(250,app.quit)
    return app.exec_()

if __name__=='__main__':
    sys.exit(main())
