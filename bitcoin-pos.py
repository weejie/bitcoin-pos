#!/usr/bin/python

import time, datetime, urllib2, json, printer, sys, os, sqlite3

taxrate = 0.0725

'''
connect to database
'''

conn = sqlite3.connect('posdb.db')
c = conn.cursor()



'''

Input the bitcoin addresses for primary account and the tip account
for the server on duty.

'''

def Setup():
    MainDepositAddress = ''
    TipDepositAddress = ''
    print('The primary address is ',MainDepositAddress)
    MainDepositAddress = raw_input("Enter a new Primary receive address:")
    print('The server address tips will be sent to is ', TipDepositAddress)
    TipDepositAddress = raw_input("Enter new server address:")
    taxrate = raw_input('Enter state sales tax: ')
    print('Bitcoin address setup complete')
    print('Going to main menu')
    time.sleep(3)
    main()

'''

Pull current coinbase market rate.  Rate updates once a minute.


'''

def GetCoinbaseRate():
    CBrate = urllib2.urlopen('https://coinbase.com/api/v1/currencies/exchange_rates').read()
    btcJSON = json.loads(CBrate)
    CBlastP = btcJSON['btc_to_usd']
    return CBlastP


'''

Functions for printer 

'''

def PrinterTesting():
    
    if len(sys.argv) == 2:
        serialport = sys.argv[1]
    else:
        serialport = printer.ThermalPrinter.SERIALPORT

    if not os.path.exists(serialport):
        sys.exit("ERROR: Serial port not found at: %s" % serialport)

    p = printer.ThermalPrinter(serialport=serialport)
    



def PrintReceipt():
    btc_s = str(btc)
    amount_s = str('%.2f'%amount)
    total_s = str('%.2f'%total)
    tip_s = str('%.2f'%tip)
    tx_s = str('%.2f'%tx)
    b_s = str('%.2f'%b)
    
    if len(sys.argv) == 2:
        serialport = sys.argv[1]
    else:
        serialport = printer.ThermalPrinter.SERIALPORT

    if not os.path.exists(serialport):
        sys.exit("ERROR: Serial port not found at: %s" % serialport)

    p = printer.ThermalPrinter(serialport=serialport)
    now = time.strftime("%c")
    
    p.justify("C")
    p.bold_on()
    p.print_text("Red Rock Bar\n")
    p.linefeed()
    p.bold_off()
    p.print_text("241 S Sierra St.\n")
    p.print_text("Reno, NV 89501\n")
    p.print_text("775-324-2468\n")
    p.linefeed()

    p.justify("L")
    p.print_text(now)
    p.print_text("\n")
    
    p.print_text("Invoice 1111\n")

    p.justify("C")
    p.linefeed()

    amount_ln = "Subtotal       $"+amount_s
    p.print_text(amount_ln)
    p.print_text('\n')

    tip_ln = "Tip            $"+tip_s 
    p.print_text(tip_ln)
    p.print_text('\n')
    
    tax_ln = "Tax            $"+tx_s
    p.print_text(tax_ln)
    p.print_text("\n")

    p.bold_on()
    p.linefeed()

    total_ln = "Total USD      $"+total_s
    p.print_text(total_ln)
    p.print_text("\n")

    btc_ln = "Total BTC    "+btc_s 
    p.print_text(btc_ln)
    p.print_text("\n")
    p.bold_off()
    p.linefeed()

    x_rate_ln = "1 bitcoin is currently $"+b_s
    p.print_text(x_rate_ln)
    p.print_text("\n")
    p.linefeed()

    p.print_text("Please send bitcoin payment to")
    
    #p.print_markup(markup)

    # runtime dependency on Python Imaging Library
    import Image, ImageDraw
    i = Image.open("print-output.png")
    data = list(i.getdata())
    w, h = i.size
    p.justify("C")
    p.print_bitmap(data, w, h, True)

    p.linefeed()
    p.linefeed()
    p.linefeed()

#def PrintOpenTickets():

'''

Update database with ticket status

'''

def tablecreate():
    c.execute('''CREATE TABLE transactions(ID INT, unix REAL, datestamp TEXT, amount REAL, tip REAL, tax REAL, totalAmount REAL, btc REAL, btcRate REAL, status TEXT)''')

def dataEntry():
    db_ID = 1
    date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    
    c.execute('''INSERT INTO transactions (ID, unix, datestamp, amount, tip, tax, totalAmount, btc, btcRate, status) VALUES (?,?,?,?,?,?,?,?,?,?)''',
              (db_ID, time.time(), date, amount, tip, tx, total, btc, b, 'open'))

    conn.commit()


'''

Button functionality.


'''

def YesButtonPress():
    ButtonPress = "Y"
def NoButtonPress():
    ButtonPress = "N"
def CancelButtonPress():
    ButtonPress = "C"

'''

New invoice creation.

'''
    
def NewInvoiceButtonPress():
    global amount, tip, total, tx, btc, b
    amount = float(raw_input("Enter bill amount: "))
    tip = float(raw_input("Enter tip total:"))
    total = (amount) * taxrate + (amount + tip)
    
    print('The total is ' '%.2f'% total)
    
    confirmation = raw_input("Is this correct?")

    if confirmation == "Y" or "y":
        InvoiceStatus = "Printed"

        print('The invoice amount is $' '%.2f'% total)

        
        tx = (amount * taxrate)
        b = float(GetCoinbaseRate())
        btc = total / b

        print('One bitcoin is currently $' '%.2f'% b)
        print('Printing Receipt...')

        dataEntry()
        PrintReceipt()
        

    else:
        print('exiting')
        quit()


'''

Functions used to query bitcoin network for confirmations on a payment

'''

#def PaymentProcess():
#def PaymentConfirmation():


'''

Main menu

'''

def main():

    print('1. Setup')
    print('2. New Invoice')
    print('3. Invoice report')
    print('4. Check invoice status')
    print('\n')
      
    pointer = raw_input('Enter choice: ')
    if pointer == '1':
        Setup()
    elif pointer == '2':
        NewInvoiceButtonPress()

main()

