import pymongo
from bson.dbref import DBRef
from bson.objectid import ObjectId
import json


_id = 0

class DB:

    MAIN_DB_NAME = "telegram-bot"
    CATEGORIES_COLLECTION_NAME = "categories"
    PACKEGES_COLLECTION_NAME = "packeges"

    def __init__(self, hostname='localhost', port=27017):
        self.client = pymongo.MongoClient(hostname, port)
        self.db = self.client[self.MAIN_DB_NAME]
        
        self.categories = self.db[self.CATEGORIES_COLLECTION_NAME]
        self.packeges = self.db[self.PACKEGES_COLLECTION_NAME]
    
    # ФУНКЦИИ ДЛЯ РАБОТЫ С КАТЕГОРИЯМИ

    # Создание новой категории (необходимо передать <имя> и <описание>). Возвращает id новой категории    
    def add_category(self, name, description, parent_id=None):
        new_category = {"name": name, "description": description, "parent": parent_id, "children": [], "packeges": []}
        child_id = self.categories.insert_one(new_category).inserted_id

        if parent_id != None:
            myquery = { "_id": parent_id}
            children = [i for i in self.categories.find({"_id": parent_id})][0]['children']
            children.append(child_id)
            newvalues = { "$set": { "children": children } }
            self.categories.update_one(myquery, newvalues)
        
        return child_id
        
    # Обновить имя и описание категории (необходимо передать еще id категории)
    def update_category(self, new_name, new_description, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return 
        
        newvalues = { "$set": { "name": new_name, "description": new_description } }
        self.categories.update_one({"_id": _id}, newvalues)

    # Получить имя категории по id
    def get_category_name(self, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        return category[0]['name']

    # Получить описание категории по id    
    def get_category_description(self, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        return category[0]['description']
    
    # Получить id детей категории по id    
    def get_children_category_id(self, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        return category[0]['children']

    # Получить родителя категории по id    
    def get_parent_category_id(self, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        return category[0]['parent']
    
    # Удалить описание категорию по id    
    def delete_category(self, _id):
        children = [i for i in self.categories.find({"parent": _id})]

        for x in children:
            for i in x['children']:
                self.categories.delete_one({"_id": i})
            self.categories.delete_one({"_id": x['_id']})

        self.categories.delete_one({"_id": _id})

    # Получить массив id категорий первого уровня (root)   
    def get_root_categories_id(self):
        root = [i for i in self.categories.find({"parent": None})]
        res = []
        for item in root:
            res.append(item['_id'])
        return res


    # ФУНКЦИИ ДЛЯ РАБОТЫ С ПАКЕТАМИ

    # Получает все пакеты категории
    def get_packedges_for_category(self, _id):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        return category[0]['packeges']
    
    # Обновляет все пакеты категории
    def set_packedges_for_category(self, _id, packeges):
        category = [i for i in self.categories.find({"_id": _id})]

        if not(category):
            return None
        
        newvalues = { "$set": {"packeges": packeges } }
        self.categories.update_one({"_id": _id}, newvalues)

   
    # DEBUG: Вывести все элементы
    def print(self):
        print("================================")
        for x in self.categories.find():
            print(x) 
        print("================================")



if __name__ == '__main__':
    db = DB()
    # db.add_category('kek', "desck2")
    # db.add_category('test1', "desck2", parent_id=ObjectId('5f779e64ec02c1e862dcb2dc'))
    # db.delete_category(ObjectId('5f779e4a290e7b88332011c8'))
    print(db.get_root_categories_id())
    print(db.get_category_name(ObjectId('5f779e64ec02c1e862dcb2dc')))
    print(db.get_category_description(ObjectId('5f779e64ec02c1e862dcb2dc')))
    print(db.get_children_category_id(ObjectId('5f779e64ec02c1e862dcb2dc')))
    print(db.get_parent_category_id(ObjectId('5f77a58236a225d294e8f8ca')))
    print(db.get_packedges_for_category(ObjectId('5f77a58236a225d294e8f8ca')))

    packeges = [
        {"name": "Имя пакета", "description": "Описание пакета"},
        {"name": "Имя пакета2", "description": "Описание пакета2"},
    ]
    db.set_packedges_for_category(ObjectId('5f77a58236a225d294e8f8ca'), packeges)

    print(db.get_packedges_for_category(ObjectId('5f77a58236a225d294e8f8ca')))


    db.print()
    