import multiprocessing
import Miner1
import Miner2
import Miner3

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=Miner1.mine_loop)
    p2 = multiprocessing.Process(target=Miner2.mine_loop)
    p3 = multiprocessing.Process(target=Miner3.mine_loop)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
