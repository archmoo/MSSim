from lib.equiplib import EquipLib
from lib.speciallib import SpecialLib
from lib.scrolllib import ScrollLib
from lib.etclib import EtcLib
import random

class MarketInfo:
    m_info = {}

    def __init__(self):
        self.m_info = {}
        for equipList in EquipLib.m_lib.values():
            for equipName, data in equipList.items():
                self.m_info[equipName] = {
                    'cost': data['cost'],
                    'value': data['value'],
                    'stock': data['stock'],
                    'max': data['max'],
                    'supply': data['supply'],
                    'orig': data['value'],
                    }
        for scrollName, data in ScrollLib.m_lib.items():
            self.m_info[scrollName] = {
                    'cost': data['cost'],
                    'value': data['value'],
                    'stock': data['stock'],
                    'max': data['max'],
                    'supply': data['supply'],
                    'orig': data['value'],
                    }
        for specialName, data in SpecialLib.m_lib.items():
            self.m_info[specialName] = {
                    'cost': data['cost'],
                    'value': data['value'],
                    'stock': data['stock'],
                    'max': data['max'],
                    'supply': data['supply'],
                    'orig': data['value'],
                    }
        for etcName, data in EtcLib.m_lib.items():
            self.m_info[etcName] = {
                    'cost': data['cost'],
                    'value': data['value'],
                    'stock': data['stock'],
                    'max': data['max'],
                    'supply': data['supply'],
                    'orig': data['value'],
                    }
        for key, data in self.m_info.items():
            for i in range(len(data['max'])):
                if data['cost'][i] == 'Meso' and data['max'][i] != -1:
                    self.m_info[key]['orig'][i] = int(round(data['orig'][i] * (1+(random.random()-0.5)*0.1)))
                    self.m_info[key]['value'][i] = int(round(data['orig'][i] * (1+max(-0.5, random.normalvariate(0, 0.1)))))

    def nextDay(self):
        for key, data in self.m_info.items():
            for i in range(len(data['max'])):
                if not data['max'][i] == -1:
                    newStock = data['stock'][i] + data['supply'][i]
                    if newStock > data['max'][i]:
                        newStock = data['max'][i]
                    self.m_info[key]['stock'][i] = newStock
                if data['cost'][i] == 'Meso' and data['max'][i] != -1:
                    self.m_info[key]['value'][i] = int(round(data['orig'][i] * (1+max(-0.5, random.normalvariate(0, 0.1)))))

                    
    def getPaymentTypeNum(self, itemName):
        data = self.m_info[itemName]
        return len(data['max'])

    def showPurchaseChoice(self, itemName, idx):
        data = self.m_info[itemName]
        info = ''
        if self.getPaymentTypeNum(itemName) == 0:
            info = '      Not available for purchase.\n'
            return info
        info += '      Payment: ' + data['cost'][idx] + '\n'
        info += '      Price: ' + EtcLib.dispLongNum(data['value'][idx]) + '\n'
        if data['max'][idx] == -1:
            info += '      Stock: Unlimited\n'
        else:
            info += '      Stock: ' + EtcLib.dispLongNum(data['stock'][idx]) + '\n'
        return info
    
    def showMarketInfo(self, itemName, etc):
        data = self.m_info[itemName]
        info = ''
        if self.getPaymentTypeNum(itemName) == 0:
            info = 'Not available for purchase.\n'
        for i in range(self.getPaymentTypeNum(itemName)):
            info += 'Choice ' + str(i+1) + ':\n'
            info += 'Payment: ' + data['cost'][i] + ' (You have '+EtcLib.dispLongNum(etc[data['cost'][i]]) + ')\n'
            info += 'Price: ' + EtcLib.dispLongNum(data['value'][i]) + '\n'
            if data['max'][i] == -1:
                info += 'Stock: Unlimited\n\n'
            else:
                info += 'Stock: ' + EtcLib.dispLongNum(data['stock'][i]) + '\n\n'
        return info

if __name__ == '__main__':

    m = MarketInfo()
    print m.showMarketInfo('Royal Dunwitch Hat')
    m.nextDay()
    print m.showMarketInfo('Royal Dunwitch Hat')
    m.nextDay()
    print m.showMarketInfo('Royal Dunwitch Hat')
