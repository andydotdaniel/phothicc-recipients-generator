import csv
import pandas as pd

class Price: 
    def __init__(self, name, value): 
        self.name = name 
        self.value = value

def isEmpty(str):
    return (not str or len(str) == 0)

def numberWithCommas(number):
    return "{:,}".format(number)

def file_to_list(filename):
    list = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            if line != '':
                list.append(line.strip())
    reader.close()

    return list

def contruct_message_body(items_qty, needs_delivery):
    prices = [
        Price('Pho Thicc', 75000),
        Price('Pho Super Thicc', 105000),
        Price('Secret Menu', 85000),
        Price('Banh Mi', 75000),
        Price('Extra Braised Beef', 25000),
        Price('Extra Sliced Beef', 25000),
        Price('Extra Kikil', 15000)
    ]

    message = "Thank you for your order!";

    items_message_list = []
    totalPrice = 0
    for index in range(len(items_qty)):
        item_qty = items_qty[index]
        if not isEmpty(item_qty):
            totalItemPrice = prices[index].value * int(item_qty)
            items_message_list.append(' ' + item_qty + ' ' + prices[index].name + ' (IDR ' + numberWithCommas(totalItemPrice) + ')')

            totalPrice += totalItemPrice

    if needs_delivery:
        deliveryPrice = 35000
        totalPrice += deliveryPrice
        items_message_list.append(' Delivery (IDR ' + numberWithCommas(deliveryPrice) + ')')
    else:
        items_message_list.append(' Delivery (IDR 0; Self-Pickup)')

    message += ','.join(items_message_list) + "."
    message += " Total " + numberWithCommas(totalPrice)
    message += " Please make the payment as soon as possible to: BCA 8700098983 / Brian Dhicosumarvin Sumito. Please send your proof of payment immediately. cảm ơn"

    return message

filename = input('Enter file name: ')
print('Generating recipients list...')
    
contacts = []
messages = []
with open(filename, mode="r") as csv_source_file:
        recipient_count = 0
        dialect = csv.Sniffer().sniff(csv_source_file.read(1024), delimiters=";,")
        csv_source_file.seek(0)
        csv_reader = csv.reader(csv_source_file, dialect)

        for row in csv_reader:
            if recipient_count != 0:
                contact = row[2]
                if contact[0] == '0':
                    contact = '+62' + contact[1:]
                if contact[0] == '8':
                    contact = '+62' + contact

                contacts.append(contact.replace(" ", ""))

                itemsQty = [
                    row[3], # phoThicc
                    row[4], # phoThiccSuper
                    row[5], # secretMenu
                    row[6], # banhmi
                    row[7], # extraBraisedBeef
                    row[8], # extraSlicedBeef
                    row[9] # extraKikil
                ]
                messages.append(contruct_message_body(itemsQty, isEmpty(row[-1])))

            recipient_count += 1

csv_source_file.close()

# dataframe Name and Age columns
df = pd.DataFrame({
    'Contact': contacts,
    'Message': messages
})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('./whatsapp_bulk_script/Recipients data.xlsx', engine='xlsxwriter')
writer.book.add_format({'num_format': '@'})

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Recipients', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

print('Recipients list generated! Total recipients: ' + str(recipient_count - 1))
