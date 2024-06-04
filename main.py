from typing import List
import pandas as pd
from matplotlib import pyplot as plt
import hashlib
import time


class Block:
    def __init__(self, timestamp: float, data: str, previous_hash: str, index: int = 0):
        self.index = index  # Індекс блоку в ланцюжку
        self.timestamp = timestamp  # Мітка часу створення блоку
        self.data = data  # Дані, які зберігаються в блоці
        self.previous_hash = previous_hash  # Хеш попереднього блоку
        self.nonce = 0  # Значення nonce (number used once) для Proof-of-Work
        self.hash = self.calculate_hash()  # Хеш поточного блоку

    def calculate_hash(self) -> str:
        """
        Обчислює хеш блоку
        """
        return hashlib.sha256(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        ).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Майнить блок з вказаною складністю proof-of-work.
        """
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.__create_genesis_block()]  # Ланцюжок блоків.
        self.difficulty: int = difficulty  # Складність proof-of-work (кількість нулів на початку).

    @staticmethod
    def __create_genesis_block() -> Block:
        """
        Створює генезисний блок (перший блок) у ланцюжку
        """
        return Block(time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Отримати останній блок у ланцюжку.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Додавання нового блоку до блокчейну.
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.index = self.get_latest_block().index + 1  # Встановлення коректного індекса.
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        Перевірка цілісності блокчейну.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or \
                    current_block.previous_hash != previous_block.hash:
                return False
            if current_block.index != previous_block.index + 1:
                return False
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                return False
        return True


def example():
    # Приклад майнінгу
    blockchain = Blockchain()
    blockchain.add_block(Block(time.time(), "RegularBlock", blockchain.get_latest_block().hash))
    blockchain.add_block(Block(time.time(), "RegularBlock", blockchain.get_latest_block().hash))

    print("Blockchain is valid:", blockchain.is_chain_valid())


def create_blockchain(difficulty: int, number_of_blocks: int):
    """
    Створення блокчейну заданої складності з заданою кількістю блоків (не рахуючи блок генезису).
    """
    blockchain = Blockchain(difficulty)
    for i in range(1, number_of_blocks+1):
        block = Block(time.time(), f"RegularBlock#{i}", blockchain.get_latest_block().hash)
        blockchain.add_block(block)
    return blockchain


def test():
    difficulties = (1, 2, 3, 4, 5)
    number_of_blocks = 100
    time_length = []
    for d in difficulties:
        start = time.time_ns()
        create_blockchain(d, number_of_blocks)
        end = time.time_ns()
        time_length.append((end-start)//1e6)
    mining_duration = pd.DataFrame(data=time_length, index=difficulties, columns=['мс'])
    print(mining_duration)
    mining_duration.plot(kind='area', title='Оцінка швидкості майнінгу 100 блоків у мілісекундах', grid=True,
                         xlabel='Складність', ylabel='мс', legend=True)
    plt.show()

if __name__ == '__main__':
    test()
