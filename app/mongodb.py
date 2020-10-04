import pymongo
from bson.dbref import DBRef
from bson.objectid import ObjectId
import json


_id = 0

class DB:

    MAIN_DB_NAME = "telegram-bot"
    CATEGORIES_COLLECTION_NAME = "categories"
    PACKEGES_COLLECTION_NAME = "packeges"

    def __init__(self, hostname='176.119.157.152', port=27017):
        self.client = pymongo.MongoClient(hostname, port, username='root', password='ffP4a42yMFkGrrTj')
        self.db = self.client[self.MAIN_DB_NAME]
        
        self.categories = self.db[self.CATEGORIES_COLLECTION_NAME]
        self.packeges = self.db[self.PACKEGES_COLLECTION_NAME]
    
    # ФУНКЦИИ ДЛЯ РАБОТЫ С КАТЕГОРИЯМИ

    # Создание новой категории (необходимо передать <имя> и <описание>). Возвращает id новой категории    
    def add_category(self, name, description, parent_id=None, is_category=True):
        new_category = {"name": name, "description": description, "parent": parent_id, "children": [], "category": is_category}
        child_id = self.categories.insert_one(new_category).inserted_id

        if parent_id != None:
            myquery = { "_id": ObjectId(parent_id)}
            children = [i for i in self.categories.find({"_id": ObjectId(parent_id)})][0]['children']
            children.append(str(child_id))
            newvalues = { "$set": { "children": children } }
            self.categories.update_one(myquery, newvalues)
        
        return str(child_id)
        
    # Обновить имя и описание категории (необходимо передать еще id категории)
    def update_category(self, new_name, new_description, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(category):
            return 
        
        newvalues = { "$set": { "name": new_name, "description": new_description } }
        self.categories.update_one({"_id": ObjectId(_id)}, newvalues)
        return _id

    # Получить имя категории по id
    def get_category_name(self, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(category):
            return None
        
        return category[0]['name']

    # Получить описание категории по id    
    def get_category_description(self, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(category):
            return None
        
        return category[0]['description']
    
    # Получить id детей категории по id    
    def get_children_category_id(self, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(category):
            return None
        
        return category[0]['children']

    # Получить родителя категории по id    
    def get_parent_category_id(self, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(category):
            return None
        
        return category[0]['parent']
    
    # Удалить описание категорию по id    
    def delete_category(self, _id, del_from_parent=True):
        current = [i for i in self.categories.find({"_id": ObjectId(_id)})]

        if not(current):
            return
        children = current[0]['children']
        parent_id = current[0]['parent']

        for c in children:
            self.delete_category(c, del_from_parent=False)
        self.categories.delete_one({"_id": ObjectId(_id)})
        if del_from_parent and parent_id:
            parent = [i for i in self.categories.find({"_id": ObjectId(parent_id)})][0]

            parent_childrens = parent['children']
            parent_childrens.remove(_id)
            newvalues = { "$set": { "children": parent_childrens} }
            self.categories.update_one({"_id": ObjectId(parent_id)}, newvalues)
            

    # Получить массив id категорий первого уровня (root)   
    def get_root_categories_id(self):
        root = [i for i in self.categories.find({"parent": None})]
        res = []
        for item in root:
            res.append(str(item['_id']))
        return res

    # Проверить, является ли категорией (возвращает True/False)
    def is_category(self, _id):
        category = [i for i in self.categories.find({"_id": ObjectId(_id)})]
        if not(category):
            return None  
        return category[0]['category']
   
    # DEBUG: Вывести все элементы
    def print(self):
        print("\n================================")
        for x in self.categories.find():
            print(x) 
        print("================================\n")



if __name__ == '__main__':
    db = DB()

    # _id = db.add_category('newnew', "desck2", parent_id='5f79f8f59a585aac8b3a83ab')
    # _id = db.add_category('kek_new', "desckasfsa2", parent_id=_id)
    # db.add_category('kek_new', "desckasfsa2", parent_id=_id)
    # db.delete_category('5f79f737f1161458c4abb646')
    # db.delete_category('5f79f76df1161458c4abb658')

    print(db.get_root_categories_id())
    db.delete_category("5f79f8f59a585aac8b3a83ac")
    # print('\n========================================\n')
    # print(db.get_category_name('5f798786aa63f7881289667b'), type(db.get_category_name('5f798786aa63f7881289667b')))
    # print(db.get_category_description('5f798786aa63f7881289667b'), type(db.get_category_description('5f798786aa63f7881289667b')))
    # print(db.get_children_category_id('5f798786aa63f7881289667b'), type(db.get_children_category_id('5f798786aa63f7881289667b')))

    db.print()
    