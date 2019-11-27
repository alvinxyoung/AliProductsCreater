from Model import Product, Session

class SqliteIntefer:
    def __init__(self):
        self.session =Session()

    def receive_data(self):
        '''接受product 实例'''
        pass

    def save_data(self):
        '''将product 保存至sqlite3'''
        pass