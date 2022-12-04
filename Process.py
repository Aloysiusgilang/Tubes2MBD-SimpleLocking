class Process :
    def __init__(self, transaction, action, data, lockManager):
        self.transaction = transaction
        self.action = action
        self.data = data 
        self.lockManager = lockManager

    def execute(self):
        # jika transaksi masuk kedalam list deadlock maka tambahkan process ke list deadlock
        if (self.transaction.txnId in self.lockManager.deadlocked_transactions):
            self.lockManager.deadlocked_process.append(self)
        else:
            # jika tidak lalukan request exclusive lock
            granted = True
            if (self.action == 'R'):
                granted = self.transaction.read(self.data)
            elif (self.action == 'W'):
                granted = self.transaction.write(self.data)
            elif(self.action == 'C'):
                granted = self.transaction.commit()

            # jika process tidak berhasil maka masukan kedalam list pending
            if (not granted):
                self.lockManager.pending.append(self)
                # jika process tersebut bukan process commit dan memiliki lock 
                if (not isinstance(self.data, str) and len(self.data.lock) > 0):
                    current_id = self.transaction.txnId
                    lockowner_id = self.data.lock[0]
                    deadlock = self.lockManager.detect_deadlock(current_id, lockowner_id)
                    if not deadlock:
                        self.lockManager.deadlock_detector[lockowner_id].append(current_id)
                    else:
                        # Aborting transaction
                        if (current_id > lockowner_id):
                            tobedeleted_id = current_id
                        else:
                            tobedeleted_id = lockowner_id
                        print(f'\nDeadlock detected. Aborting T{tobedeleted_id}!!!\n'.format(tobedeleted_id))
                        self.lockManager.clear_lock(tobedeleted_id)
                        self.lockManager.deadlocked_transactions.append(tobedeleted_id)
                        length = len(self.lockManager.pending)
                        for i in range(length):
                            process = self.lockManager.pending.pop(0) 
                            process.execute()

