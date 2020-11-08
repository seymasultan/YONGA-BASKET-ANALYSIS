import pandas as pd
from apyori import apriori
import pickle
from openpyxl import Workbook, load_workbook
import unittest
wb = Workbook()

ws = wb.active
ws.title = "İlk Çalışma Alanı"


# from mlxtend.frequent_patterns import apriori, association_rules
class Customer:
    def __init__(self, customerId, country, siparisList):
        self.customerId = customerId
        self.country = country
        self.siparisList = siparisList

    def __repr__(self):
        return self.customerId

    def __eq__(self, other):
        return self.customerId == other


class Order:
    def __init__(self, invoiceNo, productsList, invoiceDate):
        self.invoiceNo = invoiceNo
        self.productsList = productsList
        self.invoiceDate = invoiceDate

    def __str__(self):
        return "Products" + self.productsList

    def __repr__(self):
        return "Products" + self.productsList

    def __eq__(self, other):
        return self.invoiceNo == other


def readObjectFromFile(filename):
    try:
        with open(filename, 'rb') as inputs:
            data = pickle.load(inputs)
            print(filename[:-4], " dosyadan okuma başarılı.")
    except FileNotFoundError:
        data = []
    return data


def saveObjectToFile(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


'''adata = pd.read_excel('Online Retail.xlsx')
adata.head()
adata = adata.dropna()
customers = []
products = []
customers2 = []
for row in adata.values:
    custID = row[6]
    customer: Customer = None
    if custID not in customers:
        customer = Customer(custID, row[7], [])
        customers.append(customer)
    else:
        i = customers.index(custID)
        customer = customers[i]

    invoiceNo = row[0]
    product = row[2]
    if invoiceNo not in customer.siparisList:
        order = Order(invoiceNo, [], row[4])
        order.productsList.append(product)
        customer.siparisList.append(order)
    else:
        i = customer.siparisList.index(invoiceNo)
        customer.siparisList[i].productsList.append(product)

saveObjectToFile(customers, "customer.pkl") '''

customers = readObjectFromFile("customer.pkl")
print(customers[0].customerId)

customers2 = []
products = []
for i in range(0, len(customers)):
    customer = customers[i]

    if len(customer.siparisList) > 9:
        customers2.append(customer)

print(len(customers2))
ws.append(["kisiID", "items1", "items2"])

for i in range(0, 537):
    if (i == 529):
        continue
    sayac = 0
    customer = customers2[i]
    products.clear()
    for order in customer.siparisList:
        products.append(order.productsList)
    a = 5 / len(products)
    birliktelik_kural = apriori(products, min_support=a, min_confidence=0.8, min_lift=2.5, min_length=2, max_length=3)
    birliktelik_sonuc = list(birliktelik_kural)

    while len(birliktelik_sonuc) < 1 and a > 0:
        birliktelik_kural = apriori(products, min_support=a, min_confidence=0.8, min_lift=2.5, min_length=2,
                                    max_length=3)
        birliktelik_sonuc = list(birliktelik_kural)
        a = a - 0.05

    print(i, " toplam kural sayısı : ", len(birliktelik_sonuc))
    for x in birliktelik_sonuc:
        kural = x[0]
        items = [x for x in kural]
        ws.append([i, items[0], items[1]])
        sayac += 1
        if (sayac > 200):
            break
    """print("Kural: " + items[0] + " -> " + items[1])
        print("Destek: " + str(x[1]))
        print("Güven: " + str(x[2][0][2]))
        print("Lift: " + str(x[2][0][3]))
        print("=====================================") """

print(len(customers))

"""wb.save("dosyaAdi2.xlsx")
#https://kerteriz.net/python-ile-excel-dosya-islemleri/"""


class MyTestCase(unittest.TestCase):

    customers2 = []

    def test_musteriSayisi(self):
        customers = readObjectFromFile("customer.pkl")
        for i in range(0, len(customers)):
            customer: Customer = customers[i]

            if len(customer.siparisList) > 9:
                self.customers2.append(customer)
        self.assertEqual(537, len(self.customers2))

    def test_urunSayisi(self):
        count = 0
        for customer in self.customers2:
            for order in customer.siparisList:
                self.assertNotEqual(len(order.productsList),0)


if __name__ == '__main__':
    unittest.main()
