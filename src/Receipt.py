"""
// Name        : Receipt.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : La classe Receipt modella la singola entry della tabella Receipt del DB.
                 Essa contiente tutti i campi contenuti nella tabella come attributi e relativi metodi get e set.
"""

class Receipt:

    #Costruttore
    def __init__(self, K_Receipt, K_Member, Quantity, Q_Amount, Q_Discount_Amount, T_Receipt):
        self.__K_Receipt = K_Receipt
        self.__K_Member = K_Member
        self.__Quantity = Quantity
        self.__Q_Amount = Q_Amount
        self.__Q_Discount_Amount = Q_Discount_Amount
        self.__T_Receipt = T_Receipt

    # Metodo get per il campo K_Receipt
    def getKReceipt(self):
        return  self.__K_Receipt

    # Metodo get per il campo K_Member
    def getKMember(self):
        return self.__K_Member

    # Metodo get per il campo Quantity
    def getQuantity(self):
        return self.__Quantity

    # Metodo get per il campo Q_Amount
    def getQAmount(self):
        return self.__Q_Amount

    # Metodo get per il campo Q_Discount_Amount
    def getQDiscountAmount(self):
        return self.__Q_Discount_Amount

    # Metodo get per il campo T_Receipt
    def getTReceipt(self):
        return self.__T_Receipt

    # Metodo di override per la stampa
    def __repr__(self):
        return "K_Receipt: " + str(self.__K_Receipt) + "\n" \
                "K_Member: " + str(self.__K_Member) + "\n" \
                "Quantity: " + str(self.__Quantity) + "\n" \
                "Q_Discount_Amount: " + str(self.__Q_Discount_Amount) + "\n" \
                "Q_Amount: " + str(self.__Q_Amount) + "\n" \
                "T_Receipt: " + str(self.__T_Receipt) + "\n\n\n"
