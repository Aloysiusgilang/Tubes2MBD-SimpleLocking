import LockManager as SL
import Process as P
import Transaction as T
import copy

def load():
    # Baca file
    file_input = input("Ketik nama test file yang ada dalam folder test (dengan .txt): ")
    file = open("test/" + file_input, "r")
    buff = file.read()
    arrString = buff.split('\n')

    transactions = []
    dataInvoved = []
    processes = []

    for line in arrString:
        if (line[0]=='W' or line[0]=='R'):
            if (int(line[1]) not in transactions):
                transactions.append(int(line[1]))
            if (line[3] not in dataInvoved):
                dataInvoved.append((line[3]))
            processes.append([line[0], int(line[1]), line[3] ])
        else:
            processes.append([line[0], int(line[1]), None])
            
    # buat objek data dan lock manager
    SLData = []
    arrDataLabel = []
    for data in processes:
        data_label = data[2]
        arrDataLabel.append(data_label)
        SLData.append(T.Data((data_label)))
    SL_LockManager = SL.LockManager(SLData)

    # buat objek transaction
    SLTransaction = []
    for transaction in transactions:
        SLTransaction.append(T.Txn(transaction, SL_LockManager))
  
    # buat objek process
    SLProcess = []
    for proc in processes:
        transaction_id = proc[1]
        action = proc[0]
        dataLabel = proc[2]
        SLProcess.append(P.Process(SLTransaction[transaction_id - 1], action, SLData[arrDataLabel.index(dataLabel)], SL_LockManager))
    return SLProcess, SL_LockManager

# Main Program
# load transactions
processes, LockManager = load()
for process in processes:
        process.execute()
LockManager.deadlocked_transactions = []
newArrProcess = copy.deepcopy(LockManager.deadlocked_process)
LockManager.deadlocked_process = []

while (len(newArrProcess) > 0):
        for process in newArrProcess:
            process.execute()
        LockManager.deadlocked_transactions = []
        newArrProcess = copy.deepcopy(LockManager.deadlocked_process)
        LockManager.deadlocked_process = []

if len(LockManager.deadlocked_transactions) > 0:
        print('\nAborted Transactions:')
        for deadlock in LockManager.deadlocked_transactions:
            print(f'T{deadlock}'.format(deadlock))  

print('END') 