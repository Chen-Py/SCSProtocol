import threading,time

def TestA():
    cond.acquire()
    time.sleep(10)
    print('李白：看见一个敌人，请求支援')
    cond.release()
    #cond.wait()
    #print('李白：好的')
    #cond.notify()
    #cond.release()

def TestB():
    cond.acquire()
    time.sleep(5)
    print('亚瑟：等我...')
    #cond.notify()
    #cond.wait()
    #print('亚瑟：我到了，发起冲锋...')

if __name__=='__main__':
    cond = threading.Condition()
    testA = threading.Thread(target=TestA)
    testB = threading.Thread(target=TestB)
    testA.start()
    testB.start()
    testA.join()
    testB.join()