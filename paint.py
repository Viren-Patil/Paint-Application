from tkinter import *
from tkinter import ttk
from tkinter.ttk import Scale
from tkinter import colorchooser, filedialog, messagebox
import tkinter as tk
import PIL.ImageGrab as ImageGrab
from PIL import ImageTk, Image

class Paint():
    
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application")
        self.root.geometry("900x700")
        self.root.configure(background='white')
        self.stack = []
        self.item = None

        self.old_x = None
        self.old_y = None

        self.width_val = self.root.winfo_screenwidth()
        self.height_val = self.root.winfo_screenheight()

        self.pen_color = 'black'
        self.eraser_color = 'white'
        self.save_color = self.pen_color

        # Adding widgets to tkinter window
        self.color_frame = LabelFrame(self.root, bd=4, relief=RIDGE, bg="white")
        self.color_frame.grid(row=0, column=0,pady=(5,0))
        self.color_frame.config(cursor="hand2")

        colors = ['#800000', '#FF0000', '#FFA500', '#FFFF00', '#808000', '#800080', '#FF00FF', '#808080', '#00FF00', '#008000', '#000080', '#0000FF', '#00FFFF', '#008080', '#000000', '#C0C0C0']
        i = j = 0
        for color in colors:
            Button(self.color_frame, bg=color, bd=2, relief=RIDGE, width=3, command=lambda col= color:self.select_color(col)).grid(row=i, column=j)
            i += 1
            if i==8:
                i = 0
                j += 1

        self.clear_image = PhotoImage(file='signs.png')
        self.clear_button = Button(self.root, image=self.clear_image, command=self.clear, width=64)
        self.clear_button.grid(row=1, column=0, pady=(5,0))
        self.clear_button.config(cursor="hand2")
        self.clear_button_tooltip = CreateToolTip(self.clear_button, 'Clear the Canvas')
        
        self.eraser_image = PhotoImage(file='eraser.png')
        self.eraser_button = Button(self.root, image = self.eraser_image, command=self.eraser, width = 64)
        self.eraser_button.grid(row=2, column=0)
        self.eraser_button.config(cursor="hand2")
        self.eraser_button_tooltip = CreateToolTip(self.eraser_button, 'Eraser')
       
        self.line_image = PhotoImage(file='line.png')
        self.line_button = Button(self.root, image=self.line_image, command=self._createLine, width=64)
        self.line_button.grid(row=3, column=0)
        self.line_button.config(cursor="hand2")
        self.line_button_tooltip = CreateToolTip(self.line_button, 'Straight Line')
        
        self.rectangle_image = PhotoImage(file='rectangle.png')
        self.rectangle_button = Button(self.root, image=self.rectangle_image, command=self._createRectangle, width=64)
        self.rectangle_button.grid(row=4, column=0)
        self.rectangle_button.config(cursor="hand2")
        self.rectangle_button_tooltip = CreateToolTip(self.rectangle_button, 'Rectangle and Square')

        self.oval_image = PhotoImage(file='oval.png')
        self.oval_button = Button(self.root, image=self.oval_image, command=self._createOval, width=64)
        self.oval_button.grid(row=5, column=0)
        self.oval_button.config(cursor="hand2")
        self.oval_button_tooltip = CreateToolTip(self.oval_button, 'Oval and Circle')

        self.pencil_image = PhotoImage(file='pencil.png')
        self.pencil_button = Button(self.root, image=self.pencil_image, command=self._pencil, width=64)
        self.pencil_button.grid(row=6, column=0)
        self.pencil_button.config(cursor="hand2")
        self.pencil_button_tooltip = CreateToolTip(self.pencil_button, 'Pencil')

        self.undo_image = PhotoImage(file='undo.png')
        self.undo_button = Button(self.root, image=self.undo_image, command=self.undo, width=64)
        self.undo_button.grid(row=7, column=0)
        self.undo_button.config(cursor="hand2")
        self.undo_button_tooltip = CreateToolTip(self.undo_button, 'Undo')

        # self.redo_image = PhotoImage(file='redo.png')
        # self.redo_button = Button(self.root, image=self.redo_image, command=self.redo, width=64)
        # self.redo_button.grid(row=8, column=0)
        # self.redo_button.config(cursor="hand2")



        # Creating a Scale for pen and eraser size...

        self.pen_size_scale_frame = Frame(self.root, bd=5, bg='lightblue', relief=RIDGE)
        self.pen_size_scale_frame.grid(row=9, column=0,  pady=5)
        
        self.pen_size = Scale(self.pen_size_scale_frame, orient = VERTICAL, from_ = 60, to = 2, length=180)
        self.pen_size_tooltip = CreateToolTip(self.pen_size, 'Adjust the size of pen and eraser using this slider.')
        self.pen_size.set(1)
        self.pen_size.grid(row=0, column=1, padx=15, pady=5)
        self.pen_size.config(cursor="hand2")

        # Creating Canvas

        self.canvas = Canvas(self.root, bg='white', relief=GROOVE, height=self.height_val, width=self.width_val, cursor="crosshair")
        self.canvas.place(x=70, y=0)
        
        # Binding the canvas with the mouse drag

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        

        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Brush Color',command=self.brush_color)
        colormenu.add_command(label='Background Color',command=self.canvas_color)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options',menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas',command=self.clear)
        optionmenu.add_command(label='Exit',command=self.root.destroy)
        menu.add_cascade(label='File',menu=filemenu)
        filemenu.add_command(label='Save', command=self.save_it)
        filemenu.add_command(label='Save and Exit', command=self.save_it_destroy)


    # Function definitions

    def _createRectangle(self):
        self.rectx0 = 0
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectid = None
        self.pen_color = self.save_color
        self.canvas.config(cursor="fleur")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind( "<Button-1>", self.startRect )
        self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
        self.canvas.bind( "<B1-Motion>", self.movingRect )


    def startRect(self, event):
        #Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y) 
        #Create rectangle
        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, outline=self.pen_color, width=self.pen_size.get())

    def movingRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)

    def stopRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)

        self.stack.append(self.rectid)
        self.stack.append('$')            # Delimeter


    def _createOval(self):
        self.ovalx0 = 0
        self.ovaly0 = 0
        self.ovalx1 = 0
        self.ovaly1 = 0
        self.ovalid = None
        self.pen_color = self.save_color
        self.canvas.config(cursor="fleur")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind( "<Button-1>", self.startOval )
        self.canvas.bind( "<ButtonRelease-1>", self.stopOval )
        self.canvas.bind( "<B1-Motion>", self.movingOval )


    def startOval(self, event):
        #Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.ovalx0 = self.canvas.canvasx(event.x)
        self.ovaly0 = self.canvas.canvasy(event.y) 
        #Create rectangle
        self.ovalid = self.canvas.create_oval(
            self.ovalx0, self.ovaly0, self.ovalx0, self.ovaly0, outline=self.pen_color, width=self.pen_size.get())

    def movingOval(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.ovalx1 = self.canvas.canvasx(event.x)
        self.ovaly1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.ovalid, self.ovalx0, self.ovaly0,
                      self.ovalx1, self.ovaly1)

    def stopOval(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.ovalx1 = self.canvas.canvasx(event.x)
        self.ovaly1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.ovalid, self.ovalx0, self.ovaly0,
                      self.ovalx1, self.ovaly1)

        self.stack.append(self.ovalid)
        self.stack.append('$')            # Delimeter


    def _createLine(self):
        self.linex0 = 0
        self.liney0 = 0
        self.linex1 = 0
        self.liney1 = 0
        self.lineid = None
        self.pen_color = self.save_color
        self.canvas.config(cursor="tcross")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind( "<Button-1>", self.startLine )
        self.canvas.bind( "<ButtonRelease-1>", self.stopLine )
        self.canvas.bind( "<B1-Motion>", self.movingLine )

    def startLine(self, event):
        #Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.linex0 = self.canvas.canvasx(event.x)
        self.liney0 = self.canvas.canvasy(event.y) 
        #Create rectangle
        self.lineid = self.canvas.create_line(
            self.linex0, self.liney0, self.linex0, self.liney0, fill=self.pen_color, width = self.pen_size.get(), smooth=True, capstyle=ROUND)

    def movingLine(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.linex1 = self.canvas.canvasx(event.x)
        self.liney1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.lineid, self.linex0, self.liney0,
                      self.linex1, self.liney1)

    def stopLine(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.linex1 = self.canvas.canvasx(event.x)
        self.liney1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.lineid, self.linex0, self.liney0,
                      self.linex1, self.liney1)
        
        self.stack.append(self.lineid)
        self.stack.append('$')            # Delimeter


    def _pencil(self):
        self.pen_color = self.save_color
        self.canvas.config(cursor="crosshair")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def undo(self):

        self.item = self.stack.pop()

        if(self.item == '$'):     # For undoing figures like rectangle, oval, circle, square, straight lines.
            self.item = self.stack.pop()
            self.canvas.delete(self.item)

        elif(self.item == '#'):
            self.item = self.stack.pop()
            while(self.item != '#' and self.item != '$'):
                self.canvas.delete(self.item)
                if len(self.stack) == 0:
                    break
                self.item = self.stack.pop()
            
            if self.item == '#' or self.item == '$':
                self.stack.append(self.item)

    # def redo(self):
    #     self.item = self.stack.pop()
    #     self.canvas.delete(self.x)

    def clear(self):
        self.canvas.delete(ALL)
        self.canvas.configure(background='white')

    def paint(self, event):

        if self.old_x and self.old_y:
            self.stack.append(self.canvas.create_line(self.old_x,self.old_y,event.x,event.y,width=self.pen_size.get(),fill=self.pen_color,capstyle=ROUND,smooth=True))

        self.old_x = event.x
        self.old_y = event.y
        

    def reset(self,e):    # Resetting 
        
        self.old_x = None
        self.old_y = None
        self.stack.append('#')


    def select_color(self, col):
        self.pen_color = col
        self.save_color = col

    def eraser(self):
        self.canvas.config(cursor="dotbox")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.pen_color = self.eraser_color

    def brush_color(self):  #changing the pen color
        self.pen_color=colorchooser.askcolor(color=self.pen_color)[1]
        self.save_color = self.pen_color

    def canvas_color(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])
        self.eraser_color = color[1]

    
    def save_it(self):

        try:
            filename = filedialog.asksaveasfilename(defaultextension = '.jpg')
            ImageGrab.grab().save(filename)
            messagebox.showinfo('Paint says', 'image is saved as ' + str(filename))
            
        except:
            messagebox.showerror('Paint says', 'unable to save image, \n something went wrong')


    def save_it_destroy(self):

        try:
            filename = filedialog.asksaveasfilename(defaultextension = '.jpg')
            ImageGrab.grab().save(filename)
            messagebox.showinfo('Paint says', 'image is saved as ' + str(filename))
            self.root.destroy()

        except:
            messagebox.showerror('Paint says', 'unable to save image, \n something went wrong')


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 55
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


if __name__ == "__main__":
    root = Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')
    p = Paint(root)
    root.mainloop()