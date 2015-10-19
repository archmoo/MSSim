import pickle, random, os.path
import Tkinter, ttk, tkMessageBox
import ScrolledText

from equip import Equip
from lib.equiplib import EquipLib
from lib.scrolllib import ScrollLib
from lib.speciallib import SpecialLib
from lib.etclib import EtcLib
from lib.joblib import JobLib

from marketinfo import MarketInfo
from character import Character
from potential import rank_label
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID, NOITEM

from inventorywidget import InventoryWidget
from equipwidget import EquipWidget
from purchasewidget import PurchaseWidget

class MainWidget(Tkinter.Frame):

    m_inventory = None
    m_marketInfo = None
    m_charInfo = None
    m_sysMessage = None
    
    def __init__(self, parent):
        
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent

        self.init()

    def saveButtonClicked(self):
        message = 'Save Progress?\n(Old savefiles will be overwritten.)'
        result = tkMessageBox.askquestion("Save", message, icon='warning', type='yesno')
        if result == 'yes':
            with open('savedata', 'wb') as output:
                pickle.dump([self.m_inventory, self.m_marketInfo, self.m_charInfo], output, -1)
            tkMessageBox.showinfo('Save', 'Progress saved.')
            self.m_sysMessage.set('Progress saved.')

    def loadButtonClicked(self):
        message = 'Load Savedata?\n(Current progress will be overwritten.)'
        result = tkMessageBox.askquestion("Load", message, icon='warning', type='yesno')
        if result == 'yes':
            if not os.path.isfile('savedata'):
                tkMessageBox.showwarning('Invalid', 'Can not find save file.')
                return
            with open('savedata', 'rb') as save:
                oldapp = pickle.load(save)
            self.m_inventory = oldapp[0]
            self.m_marketInfo = oldapp[1]
            self.m_charInfo = oldapp[2]
            tkMessageBox.showinfo('Load', 'Progress loaded.')
            self.m_sysMessage.set('Progress loaded.')
            self.tabInventory.reset()
            self.tabEquip.reset()
            self.tabPurchase.reset()
            
    def initLoadClicked(self):
        message = 'Load Savedata?'
        result = tkMessageBox.askquestion("Load", message, icon='warning', type='yesno')
        if result == 'yes':
            if not os.path.isfile('savedata'):
                tkMessageBox.showwarning('Invalid', 'Can not find save file.')
                return

            self.initFrame.destroy()
            
            self.m_inventory = Inventory()
            self.m_marketInfo = MarketInfo()
            self.m_charInfo = Character()
            self.m_sysMessage = Tkinter.StringVar()
            self.m_sysMessage.set('Welcome!')

            self.initMainUI()
            
            with open('savedata', 'rb') as save:
                oldapp = pickle.load(save)
            self.m_inventory = oldapp[0]
            self.m_marketInfo = oldapp[1]
            self.m_charInfo = oldapp[2]
            tkMessageBox.showinfo('Load', 'Progress loaded.')
            self.m_sysMessage.set('Progress loaded.')
            self.tabInventory.reset()
            self.tabEquip.reset()
            self.tabPurchase.reset()
    
    def quitClicked(self):
        message = 'Are You Sure?'
        result = tkMessageBox.askquestion("Quit", message, icon='warning', type='yesno')
        if result == 'yes':
            self.destroy()
            self.parent.destroy()

    def nextDayButtonClicked(self):
        message = 'Are You Sure?\n\nCertain items on the market will restock.'
        result = tkMessageBox.askquestion("Next Day", message, type='yesno')
        if result == 'yes':
            self.m_marketInfo.nextDay()
            self.tabPurchase.reset()

        
    def init(self):
        
        self.parent.title('MapleStory Simulator')
        self.pack(fill=Tkinter.BOTH, expand=1)

        self.initFrame = Tkinter.Frame(self)
        self.initFrame.place(in_=self, anchor='c', relx=.5, rely=.5)
        introLabel = Tkinter.Label(self.initFrame, text='MapleStory Simulator\n\nVer. 0.1.0')
        newGameButton = Tkinter.Button(self.initFrame, text='New', command=self.initNewClicked)
        loadGameButton = Tkinter.Button(self.initFrame, text='Load', command=self.initLoadClicked)
        quitGameButton = Tkinter.Button(self.initFrame, text='Quit', command=self.quitClicked)

        introLabel.pack(pady=30)
        newGameButton.pack(pady=5)
        loadGameButton.pack(pady=5)
        quitGameButton.pack(pady=5)

        
    def initNewClicked(self):
        def updateJobList(event):
            curClass = chosenClass.get()
            size = jobListbox.size()
            if size:
                jobListbox.delete(0, size-1)
            self.classList = sorted([key for key in JobLib.m_job.keys() if JobLib.m_job[key]['class'] == curClass], key=lambda key=key: (JobLib.m_job[key]['category'], key))
            if curClass in ['Thief', 'Pirate']:
                self.classList.append('Xenon')
            for className in self.classList:
                jobListbox.insert(Tkinter.END, className)
            descriptionContent.config(state=Tkinter.NORMAL)
            descriptionContent.delete('1.0', Tkinter.END)
            descriptionContent.config(state=Tkinter.DISABLED)
            self.startFrame.curSelectIdx = -1
            
        def jobListSelected(event):
            choice = jobListbox.curselection()
            if len(choice) != 0:
                idx = choice[0]
                value = jobListbox.get(choice[0])
                self.startFrame.curSelectIdx = idx
            else:
                self.startFrame.curSelectIdx = -1
            if self.startFrame.curSelectIdx != -1:
                description = JobLib.m_job[self.classList[self.startFrame.curSelectIdx]]['description']
                descriptionContent.config(state=Tkinter.NORMAL)
                descriptionContent.delete('1.0', Tkinter.END)
                descriptionContent.insert('insert', description)
                descriptionContent.config(state=Tkinter.DISABLED)
               
        def start():
            if self.startFrame.curSelectIdx == -1:
                tkMessageBox.showwarning('Invalid', 'Please choose a job.')
                return
            chosenJob = self.classList[self.startFrame.curSelectIdx]
            message = 'Are You Sure?\n\n'
            message += 'Starting as: ' + chosenJob + '\n'
            message += 'Funding level: ' + chosenResource.get()
            res = tkMessageBox.askquestion('Start', message, type='yesno')
            if res == 'no':
                return

            self.startFrame.destroy()
            self.m_inventory = Inventory()
            self.m_marketInfo = MarketInfo()
            self.m_charInfo = Character(chosenJob)
            self.m_sysMessage = Tkinter.StringVar()
            self.m_sysMessage.set('Welcome!')

            self.initMainUI()
            
        def cancel():
            self.startFrame.destroy()
            self.init()
        
        self.initFrame.destroy()


        self.startFrame = Tkinter.Frame(self)
        self.startFrame.pack(fill="both", expand=True, padx=20, pady=20)

        self.startFrame.Frameleft = Tkinter.Frame(self.startFrame)
        self.startFrame.Frameright = Tkinter.Frame(self.startFrame)

        self.startFrame.Frameleft.rowconfigure(1, weight=1)
        self.startFrame.Frameright.rowconfigure(1, weight=1)

        classes = ['Warrior', 'Bowman', 'Magician', 'Thief', 'Pirate']
        chosenClass = Tkinter.StringVar()
        chosenClass.set('- Choose Class -')
        classOptionMenu = Tkinter.OptionMenu(self.startFrame.Frameleft, chosenClass, *classes, command=updateJobList)

        self.startFrame.curSelectIdx = -1
        jobListbox = Tkinter.Listbox(self.startFrame.Frameleft, selectmode='single')
        jobListbox.bind('<<ListboxSelect>>', jobListSelected)

        descriptionLabel = Tkinter.Label(self.startFrame.Frameright, text='Description')
        descriptionContent = ScrolledText.ScrolledText(self.startFrame.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=45, height=10)
        descriptionContent.config(font=('San Francisco', 13, 'normal'))
        descriptionContent.insert('insert', '')
        descriptionContent.config(state=Tkinter.DISABLED)

        resourceLabel = Tkinter.Label(self.startFrame.Frameright, text='Funding:', justify=Tkinter.LEFT)

        resources = ['Minimum', 'Decent (default)', 'Abundant', 'Excessive', 'Unlimited (dev only)']
        chosenResource = Tkinter.StringVar()
        chosenResource.set('Decent (default)')
        resourceOptionMenu = Tkinter.OptionMenu(self.startFrame.Frameright, chosenResource, *resources)

        startButton = Tkinter.Button(self.startFrame.Frameright, text='Start', command=start)
        cancelButton = Tkinter.Button(self.startFrame.Frameright, text='Back', command=cancel)

        classOptionMenu.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        jobListbox.grid(row=1, column=0, rowspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
        descriptionLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=Tkinter.W)
        descriptionContent.grid(row=1, column=0, rowspan=3, columnspan=5, padx=5, pady=5, sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        resourceLabel.grid(row=4, column=0, padx=5, pady=5, sticky=Tkinter.W)
        resourceOptionMenu.grid(row=4, column=1, padx=5, pady=5, sticky=Tkinter.W)
        startButton.grid(row=4, column=3, padx=5, pady=5, sticky=Tkinter.E)
        cancelButton.grid(row=4, column=4, padx=5, pady=5, sticky=Tkinter.E)
        
        self.startFrame.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.startFrame.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

    def initMainUI(self):
        
        self.tabs = ttk.Notebook(self)
        self.tabInventory = InventoryWidget(self)
        self.tabEquip = EquipWidget(self)
        self.tabPurchase = PurchaseWidget(self)
        self.tabs.add(self.tabInventory, text='Inventory')
        self.tabs.add(self.tabEquip, text='Equip')
        self.tabs.add(self.tabPurchase, text='Purchase')

        self.sysMessage = Tkinter.Label(self,
                                        textvariable=self.m_sysMessage,
                                        justify=Tkinter.LEFT)
        self.nextdayButton = Tkinter.Button(self, text='Next Day', command=self.nextDayButtonClicked)
        self.saveButton = Tkinter.Button(self, text='Save', command=self.saveButtonClicked)
        self.loadButton = Tkinter.Button(self, text='Load', command=self.loadButtonClicked)
        self.quitButton = Tkinter.Button(self, text='Quit', command=self.quitClicked)
        
        self.tabs.pack(fill=Tkinter.BOTH, expand=1)
        self.sysMessage.pack(padx=5, pady=5, side=Tkinter.LEFT)
        self.quitButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        self.loadButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        self.saveButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        self.nextdayButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        
        
        
if __name__ == '__main__':

    root = Tkinter.Tk()
    root.geometry('680x600+200+200')
    app = MainWidget(root)
    root.mainloop()
    
