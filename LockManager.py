
class LockManager :
    def __init__(self, all_data):
        self.all_data = all_data
        self.pending = []
        self.deadlock_detector = {}
        self.deadlocked_transactions = []
        self.deadlocked_process = []

    def grant_lock(self, transaction, data):
        if (transaction.txnId not in self.deadlock_detector):
            self.deadlock_detector[transaction.txnId] = []
        
        # jika data sudah memiliki lock 
        if ((len(data.lock) > 0) and (transaction.txnId == data.lock[0])):
            return True

        success = True
        # cek apakah transaksi sedang pending
        for process in self.pending:
            if (process.transaction.txnId == transaction.txnId):
                success = False 
                break

        if (success):
            data.lock.append(transaction.txnId)
            # cek apakah transaksi sudah memiliki lock
            if (transaction.txnId != data.lock[0]):
                self.deadlock_detector[data.lock[0]].append(transaction.txnId)
                success = False
            
        return success
    
    def detect_deadlock(self, current_id, lockowner_id):
        wait1 = False
        wait2 = False
        if lockowner_id in self.deadlock_detector:
            if current_id in self.deadlock_detector[lockowner_id]:
                wait1 = True
        if current_id in self.deadlock_detector:
            if lockowner_id in self.deadlock_detector[current_id]:
                wait2 = True
        return wait1 and wait2

    def clear_lock(self, transaction_id):
        for data in self.all_data:
            if transaction_id in data.lock:
                data.lock.remove(transaction_id)
        self.deadlock_detector.pop(transaction_id, None)


