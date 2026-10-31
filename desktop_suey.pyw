"""Dependency-free desktop launcher for Suey's original wandering sprite."""
import argparse
import json
from pathlib import Path
import random
import tkinter as tk

ASSETS=Path(__file__).resolve().parent/'kantekiFemale/wandering_sprite_full_package/assets'

class Suey:
    def __init__(self,root,wander=True):
        self.root=root
        self.root.title('Suey')
        self.root.overrideredirect(True)
        self.root.configure(background='#ff00ff')
        self.root.attributes('-topmost',True)
        self.root.wm_attributes('-transparentcolor','#ff00ff')
        self.label=tk.Label(root,bg='#ff00ff',borderwidth=0,highlightthickness=0)
        self.label.pack()
        self.frames={}
        timing=json.loads((ASSETS/'timing.json').read_text(encoding='utf-8'))
        self.timing={name:timing[state] for name,state in [('walk1','running-right'),('walk2','running-left'),('sit','idle')]}
        for name in self.timing:
            frames=[]
            for index in range(len(self.timing[name])):
                image=tk.PhotoImage(file=str(ASSETS/(name+'.gif')),format=f'gif -index {index}')
                if (image.width(),image.height())!=(192,208):
                    raise ValueError(f'Unexpected frame size in {name}')
                frames.append(image)
            self.frames[name]=frames
        self.action='sit'
        self.index=0
        self.animation_job=None
        self.wander_job=None
        self.drag_origin=None
        self.label.bind('<ButtonPress-1>',self.start_drag)
        self.label.bind('<B1-Motion>',self.drag)
        self.label.bind('<ButtonRelease-1>',self.end_drag)
        self.label.bind('<Button-3>',self.show_menu)
        self.root.bind('<Escape>',lambda event:self.root.destroy())
        self.menu=tk.Menu(root,tearoff=False)
        self.menu.add_command(label='Wander',command=self.resume)
        self.menu.add_command(label='Stay here',command=self.pause)
        self.menu.add_separator()
        self.menu.add_command(label='Quit Suey',command=self.root.destroy)
        self.place_randomly()
        self.animate()
        if wander:self.resume()

    def animate(self):
        self.label.configure(image=self.frames[self.action][self.index])
        delay=self.timing[self.action][self.index]
        self.index=(self.index+1)%len(self.frames[self.action])
        self.animation_job=self.root.after(delay,self.animate)

    def set_action(self,name):
        if self.animation_job is not None:self.root.after_cancel(self.animation_job)
        self.action=name
        self.index=0
        self.animate()

    def place_randomly(self):
        x=random.randint(0,max(0,self.root.winfo_screenwidth()-192))
        y=random.randint(0,max(0,self.root.winfo_screenheight()-258))
        self.root.geometry(f'192x208+{x}+{y}')

    def wander(self):
        self.set_action(random.choice(['walk1','walk2','sit']))
        self.place_randomly()
        self.wander_job=self.root.after(3000,self.wander)

    def resume(self):
        if self.wander_job is not None:self.root.after_cancel(self.wander_job)
        self.wander_job=self.root.after(3000,self.wander)

    def pause(self):
        if self.wander_job is not None:self.root.after_cancel(self.wander_job)
        self.wander_job=None
        self.set_action('sit')

    def start_drag(self,event):
        self.pause()
        self.drag_origin=(event.x_root,event.y_root,self.root.winfo_x(),self.root.winfo_y())

    def drag(self,event):
        if self.drag_origin:
            ox,oy,x,y=self.drag_origin
            new_x=x+event.x_root-ox
            new_y=y+event.y_root-oy
            self.root.geometry(f'{new_x:+d}{new_y:+d}')

    def end_drag(self,event):
        self.drag_origin=None

    def show_menu(self,event):
        self.menu.tk_popup(event.x_root,event.y_root)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke-test',action='store_true')
    args=parser.parse_args()
    root=tk.Tk()
    pet=Suey(root,wander=not args.smoke_test)
    if args.smoke_test:
        for action,frames in pet.frames.items():
            assert len(frames)==len(pet.timing[action])
            pet.set_action(action)
            root.update()
        print('Suey startup passed: Tk window, transparent background, and 22 loaded animation frames.',flush=True)
        root.after(500,root.destroy)
    root.mainloop()

if __name__=='__main__':main()
