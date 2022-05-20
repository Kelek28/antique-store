import datetime
import os
from csv import reader

from werkzeug.security import generate_password_hash

import dbInterface

dirname = os.path.dirname(__file__)
data_folder = os.path.join(dirname, 'data')


def parseDate(date_string):
    day, month, year = date_string.split('/')
    date = datetime.date(int(year), int(month), int(day))
    return date


def importPurchases():
    file = os.path.join(data_folder, 'Online Store Items Sales.csv')
    with open(file) as csv_file:
        csv_reader = reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count:
                ###############
                userId = None  # no user id in csv file
                ###############
                productId = row[0]
                if row[1]:
                    date = parseDate(row[1])
                    purchaseId = dbInterface.addPurchase(date)
                    dbInterface.addPurchaseIdToProduct(productId, purchaseId)
            line_count += 1


def importProducts():
    file = os.path.join(data_folder, 'Online Store Project Items for Sale.csv')
    with open(file) as csv_file:
        csv_reader = reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count:
                product_id = row[0]
                description = row[1]
                #################
                image_url = None  # no image_url in csv file
                #################
                price = row[2]
                ##############
                set_id = None  # set_id imported later
                ##############
                dbInterface.addProduct(description, image_url, price, set_id, product_id)
            line_count += 1


def importListing(shop, filename):
    file = os.path.join(data_folder, filename)
    with open(file) as csv_file:
        csv_reader = reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count:
                product_id = row[0]
                dbInterface.addListing(product_id, shop)
            line_count += 1


def importListings():
    importListing(0, 'Online Store Project Items for Sale ALTERNATIVE SHOP A.csv')
    importListing(1, 'Online Store Project Items for Sale ALTERNATIVE SHOP B.csv')


def importSets():
    file = os.path.join(data_folder, 'Online Store Project Sets of Items for Sale.csv')
    with open(file) as csv_file:
        csv_reader = reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count:
                set_id = row[0]
                description = row[1]
                price = row[2]
                num_items = row[3]
                dbInterface.addSet(description, price, set_id)
                for i in range(int(num_items)):
                    item_id = row[i + 4]
                    dbInterface.addProductToSet(item_id, set_id)
            line_count += 1


def importImageUrls():
    file = os.path.join(data_folder, 'Stock Pictures.csv')
    with open(file) as csv_file:
        csv_reader = reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count:
                item_id = row[0]
                #####################
                description = row[1]  # Not used
                #####################
                image_url = row[2]
                dbInterface.addImageUrlToProduct(item_id, image_url)
            line_count += 1


def addAdminUser():
    dbInterface.addUser("admin@admin.com", "Admin", "Admin", generate_password_hash("password"), "Admin")


def importDataFromCsv():
    importProducts()
    importImageUrls()
    importListings()
    importSets()
    # importPurchases()
    addAdminUser()


if __name__ == "__main__":
    importDataFromCsv()
