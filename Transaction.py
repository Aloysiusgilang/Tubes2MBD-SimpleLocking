class Txn :
    def __init__(self, txnId, lockManager):
        self.txnId = txnId
        self.lockManager = lockManager

    def read(self, data):
        spacing = " " * (self.txnId-1) * 18
        if (self.lockManager.grant_lock(self, data)):
            print("->"+ spacing+" R" + str(self.txnId) + "(" + data.data +") ")
            return True
        else:
            print("-|"+ spacing+" R" + str(self.txnId) + "(" + data.data + ") on queue")
            return False
    
    def write(self, data):
        spacing = " " * (self.txnId-1) * 18
        if (self.lockManager.grant_lock(self, data)):
            print("->"+ spacing+" W"+ str(self.txnId) + "(" + data.data +") ")
            return True
        else:
            print("-|"+ spacing+" W"+ str(self.txnId) + "(" + data.data + ") on queue")
            return False

    def commit(self):
        spacing = " " * (self.txnId-1) * 18
        success = True
        for process in self.lockManager.pending:
            if (process.transaction.txnId == self.txnId):
                success = False
                break
        
        if (success):
            for index, data in enumerate(self.lockManager.all_data):
                if (len(data.lock) > 0 and data.granted_lock() == self.txnId):
                    data_pop = data.lock.pop(0)
            self.lockManager.deadlock_detector.pop(self.txnId, None)

            print(f'-> {spacing}C{self.txnId}')
            
            length = len(self.lockManager.pending)
            for i in range(length):
                process = self.lockManager.pending.pop(0) 
                process.execute()
            print(f'-|{spacing} C{self.txnId} on queue ')

        return success

class Data :
    def __init__(self, data):
        self.data = data
        self.lock = []

    def granted_lock(self):
        return self.lock[0]

