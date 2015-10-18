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

class PurchaseWidget(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.curChosenType = '- Choose Type -'
        self.curChosenCategory = '- Choose Category -'
        self.listboxList = []
        self.curSelectIdx = -1
        self.initUI()

    def reset(self):
        self.curChosenType = '- Choose Type -'
        self.chosenType.set('- Choose Type -')
        self.curChosenCategory = '- Choose Category -'
        self.chosenCategory.set('- Choose Category -')
        self.listboxList = []
        self.curSelectIdx = -1
        size = self.itemListbox.size()
        if size:
            self.itemListbox.delete(0, size-1)
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoContent.config(state=Tkinter.NORMAL)
        self.marketInfoContent.delete('1.0', Tkinter.END)
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
        self.resourceContent.set(message)

    def updateType(self, event):
        def setUpCategory(option):
            self.chosenCategory.set(option)
            self.updateCategory()
            
        chosenType = self.chosenType.get()
        if self.curChosenType == chosenType:
            return
        self.curChosenType = chosenType
        self.chosenCategory.set('- Choose Category -')
        self.curChosenCategory = '- Choose Category -'
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoContent.config(state=Tkinter.NORMAL)
        self.marketInfoContent.delete('1.0', Tkinter.END)
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        size = self.itemListbox.size()
        if size:
            self.itemListbox.delete(0, size-1)
        self.listboxList = []
        self.curSelectIdx = -1

        if chosenType == 'Equip':
            equipTypes = sorted(EquipLib.m_lib.keys())
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for equipType in equipTypes:
                self.categoryOptionMenu['menu'].add_command(label=equipType,
                                                    command=lambda name=equipType: setUpCategory(name))
        elif chosenType == 'Use':
            useTypes = ['Special', 'Hammer', 'Cube', 'Scroll', 'Trace']
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for useType in useTypes:
                self.categoryOptionMenu['menu'].add_command(label=useType,
                                                    command=lambda name=useType: setUpCategory(name))
        elif chosenType == 'Etc':
            etcTypes = ['Trace', 'Meso', 'NX', 'Coin']
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for etcType in etcTypes:
                self.categoryOptionMenu['menu'].add_command(label=etcType,
                                                    command=lambda name=etcType: setUpCategory(name))

    def updateCategory(self):
            chosenCategory = self.chosenCategory.get()
            if self.curChosenCategory == chosenCategory:
                return
            self.curChosenCategory = chosenCategory
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.config(state=Tkinter.DISABLED)
            size = self.itemListbox.size()
            if size:
                self.itemListbox.delete(0, size-1)
            self.listboxList = []
            self.curSelectIdx = -1

            if self.curChosenType == 'Equip':
                self.listboxList = sorted(EquipLib.m_lib[chosenCategory].keys())
##                print self.listboxList
                for equipName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, equipName)
            elif self.curChosenType == 'Use':
                usesLib = {}
                usesLib.update(ScrollLib.m_lib)
                usesLib.update(SpecialLib.m_lib)
                self.listboxList = sorted([key for key in usesLib.keys() if usesLib[key]['type'] == chosenCategory])
                for useName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, useName)
            elif self.curChosenType == 'Etc':
                etcLib = EtcLib.m_lib
                self.listboxList = sorted([key for key in etcLib.keys() if etcLib[key]['type'] == chosenCategory])
                for etcName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, etcName)
                
                

    def itemListboxSelect(self, event):
        listbox = event.widget
        choice = listbox.curselection()
        if len(choice) != 0:
            idx = choice[0]
            value = listbox.get(choice[0])
            self.curSelectIdx = idx
        else:
            self.curSelectIdx = -1
        if self.curSelectIdx == -1:
            return
        if self.curChosenType == 'Equip':
            equip = Equip(self.listboxList[self.curSelectIdx])
            equip.setClean()
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.insert('insert', equip.showEquip())
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(equip.m_name, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
        elif self.curChosenType == 'Use':
            scrollName = self.listboxList[self.curSelectIdx]
            description = scrollName + '\n\n'
            description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_use[scrollName]) + '\n\n'
            if self.curChosenCategory in ['Special', 'Hammer', 'Cube']:
                description += SpecialLib.m_lib[scrollName]['description']
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
            else:
                description += ScrollLib.showScrollStat(scrollName)
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(scrollName, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
                
        elif self.curChosenType == 'Etc':
            etcName = self.listboxList[self.curSelectIdx]
            description = etcName + '\n\n'
            description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc[EtcLib.m_lib[etcName]['etc']]) + ' ' + EtcLib.m_lib[etcName]['etc'] +'\n\n'
            description += EtcLib.m_lib[etcName]['description']
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.insert('insert', description)
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(etcName, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
            
        
    def purchaseButtonClicked(self):
        def purchaseEquip():
            choiceIdx = radioButtonVar.get()
            if choiceIdx == -1:
                tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                return
            marketInfo = self.parent.m_marketInfo.m_info[equipName]
            availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
            if marketInfo['stock'][choiceIdx] == 0:
                tkMessageBox.showwarning('Invalid', 'Out of stock.')
                return
            elif marketInfo['value'][choiceIdx] > availPay:
                message = 'Can not afford.\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                tkMessageBox.showwarning('Invalid', message)
                return
            else:
                message = 'Are You Sure?\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                if res == 'yes':
                    self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= marketInfo['value'][choiceIdx]
                    if marketInfo['stock'][choiceIdx] != -1:
                        self.parent.m_marketInfo.m_info[equipName]['stock'][choiceIdx] -= 1
                    self.parent.m_inventory.createEquip(self.listboxList[self.curSelectIdx])

                    message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                    message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                    self.resourceContent.set(message)
                    self.marketInfoContent.config(state=Tkinter.NORMAL)
                    self.marketInfoContent.delete('1.0', Tkinter.END)
                    self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(equipName, self.parent.m_inventory.m_etc))
                    self.marketInfoContent.config(state=Tkinter.DISABLED)
                    self.parent.tabInventory.reset()
                    self.parent.tabEquip.reset()
                    toplevel.destroy()

            
        def purchaseUse():
            choiceIdx = radioButtonVar.get()
            if choiceIdx == -1:
                tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                return
            value = quantityEntry.get()
            try: 
                quantity = int(value)
                assert quantity > 0
            except Exception:
                tkMessageBox.showwarning('Invalid', 'Invalid input!')
                return
            marketInfo = self.parent.m_marketInfo.m_info[scrollName]
            availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
            if marketInfo['stock'][choiceIdx] == 0:
                tkMessageBox.showwarning('Invalid', 'Out of stock.')
                return
            elif marketInfo['stock'][choiceIdx] != -1 and marketInfo['stock'][choiceIdx] < quantity:
                message = 'Only ' + EtcLib.dispLongNum(marketInfo['stock'][choiceIdx]) + ' in stock.\n'
                tkMessageBox.showwarning('Invalid', message)
                return
            elif marketInfo['value'][choiceIdx] * quantity > availPay:
                message = 'Can not afford.\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                tkMessageBox.showwarning('Invalid', message)
                return
            else:
                message = 'Are You Sure?\n\n'
                message += 'Purchasing ' + EtcLib.dispLongNum(quantity) + ' ' + self.listboxList[self.curSelectIdx] + '.\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                if res == 'yes':
                    self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= (marketInfo['value'][choiceIdx] * quantity)
                    if marketInfo['stock'][choiceIdx] != -1:
                        self.parent.m_marketInfo.m_info[scrollName]['stock'][choiceIdx] -= quantity
                    self.parent.m_inventory.m_use[self.listboxList[self.curSelectIdx]] += quantity

                    message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                    message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                    self.resourceContent.set(message)
                    self.marketInfoContent.config(state=Tkinter.NORMAL)
                    self.marketInfoContent.delete('1.0', Tkinter.END)
                    self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(scrollName, self.parent.m_inventory.m_etc))
                    self.marketInfoContent.config(state=Tkinter.DISABLED)
                    self.parent.tabInventory.reset()
                    description = scrollName + '\n\n'
                    description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_use[scrollName]) + '\n\n'
                    if self.curChosenCategory in ['Special', 'Hammer', 'Cube']:
                        description += SpecialLib.m_lib[scrollName]['description']
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
                    else:
                        description += ScrollLib.showScrollStat(scrollName)
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
##                    self.parent.tabEquip.reset()
                    toplevel.destroy()
        def purchaseEtc():
##            print etcName
            if not 'Meso Sack' in etcName:
                choiceIdx = radioButtonVar.get()
                if choiceIdx == -1:
                    tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                    return
                value = quantityEntry.get()
                try: 
                    quantity = int(value)
                    assert quantity > 0
                except Exception:
                    tkMessageBox.showwarning('Invalid', 'Invalid input!')
                    return
                marketInfo = self.parent.m_marketInfo.m_info[etcName]
                availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
                if marketInfo['stock'][choiceIdx] == 0:
                    tkMessageBox.showwarning('Invalid', 'Out of stock.')
                    return
                elif marketInfo['stock'][choiceIdx] != -1 and marketInfo['stock'][choiceIdx] < quantity:
                    message = 'Only ' + EtcLib.dispLongNum(marketInfo['stock'][choiceIdx]) + ' in stock.\n'
                    tkMessageBox.showwarning('Invalid', message)
                    return
                elif marketInfo['value'][choiceIdx] * quantity > availPay:
                    message = 'Can not afford.\n\n'
                    message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                    message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                    tkMessageBox.showwarning('Invalid', message)
                    return
                else:
                    message = 'Are You Sure?\n\n'
                    message += 'Purchasing ' + EtcLib.dispLongNum(quantity) + ' ' + self.listboxList[self.curSelectIdx] + '.\n'
                    message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                    message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                    res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                    if res == 'yes':
                        self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= (marketInfo['value'][choiceIdx] * quantity)
                        if marketInfo['stock'][choiceIdx] != -1:
                            self.parent.m_marketInfo.m_info[etcName]['stock'][choiceIdx] -= quantity
                            
                        #self.parent.m_inventory.m_use[self.listboxList[self.curSelectIdx]] += quantity
                        self.parent.m_inventory.m_etc[EtcLib.m_lib[etcName]['etc']] += quantity * EtcLib.m_lib[etcName]['quantity']

                        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                        self.resourceContent.set(message)
                        self.marketInfoContent.config(state=Tkinter.NORMAL)
                        self.marketInfoContent.delete('1.0', Tkinter.END)
                        self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(etcName, self.parent.m_inventory.m_etc))
                        self.marketInfoContent.config(state=Tkinter.DISABLED)
                        self.parent.tabInventory.reset()
                        description = etcName + '\n\n'
                        description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc[EtcLib.m_lib[etcName]['etc']]) + ' ' + EtcLib.m_lib[etcName]['etc'] +'\n\n'
                        description += EtcLib.m_lib[etcName]['description']
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
##                      self.parent.tabEquip.reset()
                        toplevel.destroy()
            else: #Meso Sack
                choiceIdx = radioButtonVar.get()
                if choiceIdx == -1:
                    tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                    return
                marketInfo = self.parent.m_marketInfo.m_info[etcName]
                availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
                if marketInfo['stock'][choiceIdx] == 0:
                    tkMessageBox.showwarning('Invalid', 'Out of stock.')
                    return
                elif marketInfo['value'][choiceIdx] > availPay:
                    message = 'Can not afford.\n\n'
                    message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                    message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                    tkMessageBox.showwarning('Invalid', message)
                    return
                else:
                    message = 'Are You Sure?\n\n'
                    message += 'Purchasing ' + self.listboxList[self.curSelectIdx] + '.\n'
                    message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                    message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                    res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                    if res == 'yes':
                        self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= (marketInfo['value'][choiceIdx])
                        if marketInfo['stock'][choiceIdx] != -1:
                            self.parent.m_marketInfo.m_info[etcName]['stock'][choiceIdx] -= 1

                        amount = int(random.expovariate(EtcLib.m_lib[etcName]['quantity'])*50000000)
                        mesoSackMessage = 'You opened ' + etcName + '.\n\n'
                        mesoSackMessage += 'You received ' + EtcLib.dispLongNum(amount) + ' ' + EtcLib.m_lib[etcName]['etc'] +'!\n'
                        self.parent.m_inventory.m_etc[EtcLib.m_lib[etcName]['etc']] += amount

                        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                        self.resourceContent.set(message)
                        self.marketInfoContent.config(state=Tkinter.NORMAL)
                        self.marketInfoContent.delete('1.0', Tkinter.END)
                        self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(etcName, self.parent.m_inventory.m_etc))
                        self.marketInfoContent.config(state=Tkinter.DISABLED)
                        self.parent.tabInventory.reset()
                        description = etcName + '\n\n'
                        description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc[EtcLib.m_lib[etcName]['etc']]) + ' ' + EtcLib.m_lib[etcName]['etc'] +'\n\n'
                        description += EtcLib.m_lib[etcName]['description']
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
##                      self.parent.tabEquip.reset()

                        tkMessageBox.showinfo('Open Meso Sack', mesoSackMessage)
                        
                        toplevel.destroy()
        
        if self.curSelectIdx == -1:
            return
        if self.curChosenType == 'Equip':
            equipName = self.listboxList[self.curSelectIdx]
            choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(equipName)
            if choiceNum == 0:
                tkMessageBox.showwarning('Not available', 'Not available for purchase.')
                return
            toplevel = Tkinter.Toplevel(self)
            toplevel.title('Purchase')
            height = choiceNum * 80 + 150
            toplevel.geometry('300x'+str(height)+'+300+300')
            toplevel.grab_set()
            choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
            
            radioButtons = []
            radioButtonVar = Tkinter.IntVar()
            radioButtonVar.set(-1)
            for i in range(choiceNum):
                choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(equipName, i)
                radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                radioButtons.append(radioButton)
                
            purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseEquip)
            cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

            toplevel.columnconfigure(0, weight=1)
            toplevel.columnconfigure(1, weight=1)
            toplevel.columnconfigure(2, weight=1)
            choiceLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            for i in range(choiceNum):
                toplevel.rowconfigure(i+1, weight=1)
                radioButtons[i].grid(row=i+1, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
            purchaseButton.grid(row=choiceNum+1, column=0, columnspan=3, padx=5, pady=5)
            cancelButton.grid(row=choiceNum+2, column=0, columnspan=3, padx=5, pady=5)
                            
        elif self.curChosenType == 'Use':
            scrollName = self.listboxList[self.curSelectIdx]
            choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(scrollName)
            if choiceNum == 0:
                tkMessageBox.showwarning('Not available', 'Not available for purchase.')
                return
            toplevel = Tkinter.Toplevel(self)
            toplevel.title('Purchase')
            height = choiceNum * 80 + 180
            toplevel.geometry('300x'+str(height)+'+300+300')
            toplevel.grab_set()
            toplevel.columnconfigure(0, weight=1)
            toplevel.columnconfigure(1, weight=1)
            toplevel.columnconfigure(2, weight=1)
            quantityLabel = Tkinter.Label(toplevel, text='Quantity:')
            quantityEntry = Tkinter.Entry(toplevel)

            choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
            
            radioButtons = []
            radioButtonVar = Tkinter.IntVar()
            radioButtonVar.set(-1)
            for i in range(choiceNum):
                choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(scrollName, i)
                radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                radioButtons.append(radioButton)
            
            
            purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseUse)
            cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

            quantityLabel.grid(row=0, column=0, padx=5, pady=5)
            quantityEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
            choiceLabel.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
            for i in range(choiceNum):
                toplevel.rowconfigure(i+2, weight=1)
                radioButtons[i].grid(row=i+2, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
            purchaseButton.grid(row=choiceNum+2, column=1, padx=5, pady=5)
            cancelButton.grid(row=choiceNum+3, column=1, padx=5, pady=5)
            
        elif self.curChosenType == 'Etc':
            etcName = self.listboxList[self.curSelectIdx]
            if 'Meso Sack' not in etcName:
                choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(etcName)
                if choiceNum == 0:
                    tkMessageBox.showwarning('Not available', 'Not available for purchase.')
                    return
                toplevel = Tkinter.Toplevel(self)
                toplevel.title('Purchase')
                height = choiceNum * 80 + 180
                toplevel.geometry('300x'+str(height)+'+300+300')
                toplevel.grab_set()
                toplevel.columnconfigure(0, weight=1)
                toplevel.columnconfigure(1, weight=1)
                toplevel.columnconfigure(2, weight=1)
                quantityLabel = Tkinter.Label(toplevel, text='Quantity:')
                quantityEntry = Tkinter.Entry(toplevel)

                choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
                
                radioButtons = []
                radioButtonVar = Tkinter.IntVar()
                radioButtonVar.set(-1)
                for i in range(choiceNum):
                    choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(etcName, i)
                    radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                    radioButtons.append(radioButton)
                
                
                purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseEtc)
                cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

                quantityLabel.grid(row=0, column=0, padx=5, pady=5)
                quantityEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
                choiceLabel.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
                for i in range(choiceNum):
                    toplevel.rowconfigure(i+2, weight=1)
                    radioButtons[i].grid(row=i+2, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
                purchaseButton.grid(row=choiceNum+2, column=1, padx=5, pady=5)
                cancelButton.grid(row=choiceNum+3, column=1, padx=5, pady=5)
            else: #meso sack
                choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(etcName)
                toplevel = Tkinter.Toplevel(self)
                toplevel.title('Purchase')
                height = choiceNum * 80 + 180
                toplevel.geometry('300x'+str(height)+'+300+300')
                toplevel.grab_set()
                toplevel.columnconfigure(0, weight=1)
                toplevel.columnconfigure(1, weight=1)
                toplevel.columnconfigure(2, weight=1)

                choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
                
                radioButtons = []
                radioButtonVar = Tkinter.IntVar()
                radioButtonVar.set(-1)
                for i in range(choiceNum):
                    choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(etcName, i)
                    radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                    radioButtons.append(radioButton)
                
                
                purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseEtc)
                cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

                choiceLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
                for i in range(choiceNum):
                    toplevel.rowconfigure(i+1, weight=1)
                    radioButtons[i].grid(row=i+1, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
                purchaseButton.grid(row=choiceNum+1, column=1, padx=5, pady=5)
                cancelButton.grid(row=choiceNum+2, column=1, padx=5, pady=5)
    
    def initUI(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=10)
        self.Frameleft.rowconfigure(2, weight=1)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright.rowconfigure(1, weight=1)
        self.Frameright.rowconfigure(5, weight=1)


        self.categories = ['']
        self.chosenCategory = Tkinter.StringVar()
        self.chosenCategory.set('- Choose Category -')
        
        self.types = ['Equip', 'Use', 'Etc']
        self.chosenType = Tkinter.StringVar()
        self.chosenType.set('- Choose Type -')

        self.typeOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenType, *self.types, command=self.updateType)
        self.categoryOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenCategory, *self.categories)
        self.categoryOptionMenu['menu'].delete(0)

        self.itemListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.itemListbox.bind('<<ListboxSelect>>', self.itemListboxSelect)

        self.resourceContent = Tkinter.StringVar()
        self.resourceLabel = Tkinter.Label(self.Frameleft, textvariable=self.resourceContent, justify=Tkinter.LEFT)
        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
        self.resourceContent.set(message)

        self.descriptionLabel = Tkinter.Label(self.Frameright, text='Description')
        self.descriptionContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.descriptionContent.config(font=('San Francisco', 13, 'normal'))
        self.descriptionContent.insert('insert', '')
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoLabel = Tkinter.Label(self.Frameright, text='Market Info')
        self.marketInfoContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.marketInfoContent.config(font=('San Francisco', 13, 'normal'))
        self.marketInfoContent.insert('insert', '')
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        self.purchaseButton = Tkinter.Button(self.Frameright, text='Purchase', command=self.purchaseButtonClicked)

        self.typeOptionMenu.grid(row=0, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.categoryOptionMenu.grid(row=1, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.itemListbox.grid(row=2, column=0, rowspan=6, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
        self.resourceLabel.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)

        self.descriptionLabel.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.descriptionContent.grid(row=1, column=0,
                                    rowspan=3, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.marketInfoLabel.grid(row=4, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.marketInfoContent.grid(row=5, column=0,
                                    rowspan=3, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.purchaseButton.grid(row=8, column=2, padx=5, pady=5, sticky=Tkinter.E)
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

