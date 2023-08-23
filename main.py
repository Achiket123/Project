from kivy.app import App
from kivy.uix import label,button,textinput,boxlayout,floatlayout,checkbox,gridlayout,anchorlayout,scrollview
from kivy.core.window import Window
from kivy.graphics import Color,Rectangle
import csv


fh=open("tasks.csv",'+r',newline='')
ob=csv.reader(fh)
wr=csv.writer(fh)

Window.clearcolor='#30120c'
Window.size=(325,565)


class Tasklabels(boxlayout.BoxLayout):
    def __init__(self,text,bxlayout,list_task,comp=False,**kwargs):
        super().__init__(**kwargs)
        self.complete=comp
        self.text=text
        self.bxlayout = bxlayout
        self.list_task=list_task
        with self.canvas:
            Color(0.270, 0.00, 0.0855,1)
            self.background_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_background, size=self.update_background)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height=95
        
        self.checkbox = checkbox.CheckBox(size_hint_x=None, width=100,active=False)
        self.checkbox.bind(active=self.returning_value)
        self.lbl = label.Label(text=text, size_hint_x=2000)
        
        
        self.add_widget(self.checkbox)
        self.add_widget(self.lbl)
    
    def returning_value(self, checkbox, value):
        if value:
            self.complete = True
            for i in self.list_task:
                if i[0] == self.text:
                    self.list_task.remove(i)
            
            self.bxlayout.remove_widget(self)
            
			
    def update_background(self, *args):
        self.background_rect.pos = self.pos
        self.background_rect.size = self.size




class ToDoApp(App):
    def build(self):
        self.tasklabels=[]
        self.tasks=[x for x in ob]
        
        
        
        
        
        self.main_layout = floatlayout.FloatLayout()
        self.scroll = scrollview.ScrollView()
        
        self.upper_layout= anchorlayout.AnchorLayout(pos_hint={'center_x':0.5,'center_y':0.54},size_hint=(1,0.9))
        self.bx_layout=boxlayout.BoxLayout(orientation='vertical')
        self.scroll.add_widget(self.bx_layout)
        self.upper_layout.add_widget(self.scroll)
        
        self.main_layout.add_widget(self.upper_layout)
        self.inner_layout=anchorlayout.AnchorLayout(anchor_y='bottom',size_hint=(1,0.1))
        self.inner_layout_1=gridlayout.GridLayout(rows=1)
        self.inner_layout.add_widget(self.inner_layout_1)
        self.main_layout.add_widget(self.inner_layout)

        self.input=textinput.TextInput(hint_text="Enter a task",size_hint=(0.7,0.1),padding_y=25,font_size='16sp',scroll_from_swipe=True)
        self.inner_layout_1.add_widget(self.input)
        
        self.button1 = button.Button(text='Add Task',bold=True,size_hint=(0.3,0.1),on_press=self.Add_task,background_color='red')
        self.inner_layout_1.add_widget(self.button1)
        
        self.load_tasks_from_csv()
        return self.main_layout
    
    
    def load_tasks_from_csv(self):
       
        for row in self.tasks:
            if row:
                text, complete = row
                complete = complete != "True"
                l = Tasklabels(text=text, comp=complete, list_task=self.tasks, bxlayout=self.bx_layout)
                
                self.bx_layout.add_widget(l)
               
        
    def Add_task(self,btn):
        
        self.text=self.input.text
        self.input.text=''
        l=Tasklabels(text=self.text,bxlayout=self.bx_layout,list_task=self.tasks)
        self.tasklabels.append(l)
        k=[self.text,False]
        self.tasks.append(k)
        if self.text != '':
            self.bx_layout.add_widget(l)
    

    
    def on_stop(self):
        fh.seek(0,0)
        fh.truncate(0)
        wr.writerows(self.tasks)
        fh.close()
        return super().on_stop()
        
            
    
        
    
ToDoApp().run()
