import pandas as pd
import matplotlib.pyplot as plt
import math



class Mortage:
    _capital = 0
    _debt = 0
    _interest_rate = 0 #percentage of interest
    _monthly_interest_rate = 0
    _total_interests = 0
    _term_years = 0
    _term = 0 #months
    _monthly_payment = 0

    _related_expenses = {}
    _history = None

    _bank_data = {}
    
    def __init__(self, capital=0, interest=0, term = 0):
        self._capital = capital
        self._debt = capital
        self._interest_rate = interest/100
        self._monthly_interest_rate = self._interest_rate/12
        self._term_years = term
        self._term = term * 12

        self._history = pd.DataFrame(columns=['debt', 'time', 'amortization', 'interest', 'payment', 'type', 'frequency'])


        self._monthly_payment = self.calculate_monthly_amortization()        
        self._toString()

    def set_bank_data(self,**kwargs):
        for k,v in kwargs.items():
            self._bank_data[k]=v

    def add_related_expense(self, name:str='', value:int=0, frequency:str='monthly', **kwargs):
        expense = {
            'name': name,
            'value':value,
            'frequency':frequency,
            'last_payment':0
        }
        self._related_expenses[name] = expense

    def get_related_expense(self, name):
        print(self._related_expenses)
        return self._related_expenses[name]
    
    def pay_related_expenses(self, time):
        for name,expense in self._related_expenses.items():
            
            print(name)
            print(expense)
            print(expense['frequency'])
            if (expense['frequency'] == 'yearly' and expense['last_payment'] == 11) or \
                (expense['frequency'] == 'quarterly' and expense['last_payment'] == 3) or \
                expense['frequency'] == 'monthly':
                self.related_expense_payment(name, time)
                expense['last_payment'] = 0

            expense['last_payment'] +=1


    def related_expense_payment(self, name, time):
        print(f"-- related_expense_payment: {name}")
        expense = self.get_related_expense(name)
        print(expense)
        self._history = self._history._append({'debt': self._debt, 
                                                  'time': time, 
                                                  'amortization':0, 
                                                  'interest': 0,
                                                  'payment':expense['value'],
                                                  'type':'extra_expense',
                                                  'frequency':expense['name']}, ignore_index=True)

    def calculate_monthly_amortization(self):
        """
        Calculates the monthly amortization (monthly payment) for a mortgage.

        Returns:
        - Monthly amortization (monthly payment).
        """
        monthly_payment = self._debt * (self._monthly_interest_rate * (1 + self._monthly_interest_rate) ** self._term) / ((1 + self._monthly_interest_rate) ** self._term - 1)
        return monthly_payment


    def calculate_current_debt(self)->tuple[float,float]:
        """
        Calculates the pending debt to be amortized in a mortgage and the pending interests to be paid.
        """
        # self._monthly_payment = self.calculate_monthly_amortization()
        total_debt = self._monthly_payment * self._term
        pending_interests = total_debt - self._capital
        # total_debt = self._debt * ((1 + self._interest_rate/12) ** self._term - 1) / self._interest_rate/12

        return round(total_debt,2), round(pending_interests,2)


    

    def amortization(self, payment:int=0, amortization_interest:int=0, type:str='monthly', **kwargs):
        """
        makes an extra amortization to current debt reducing term or monthly payment

        Args:
            payment (int): Quantity of extra amortization
            amortization_interest (int): interest aplied
            type (str, optional): _description_. Defaults to 'fee'.
        """
        time = kwargs['time']

        if self._debt - payment < 0:
            payment = payment - (self._debt - payment)


        if type=='monthly':
            interest = self._debt * self._monthly_interest_rate
            # payment = self._monthly_payment
            type = 'monthly_amortization'
            frequency = 'monthly' 

            amortization = payment - interest
            self._debt -= amortization
            self._term -= 1
        elif type == 'extra_term':
            interest = payment * amortization_interest
            type = 'extra_term_amortization'
            frequency = '-' 


            amortization = payment - interest
            self._debt -= amortization
            self._term = math.log(self._monthly_payment / (self._monthly_payment - self._debt * self._interest_rate/12)) / math.log(1 + self._interest_rate/12)
        elif type == 'extra_payment':
            interest = payment * amortization_interest
            type = 'extra_payment_amortization'
            frequency = '-'


            amortization = payment - interest
            self._debt -= amortization
            self._monthly_payment = self.calculate_monthly_amortization()
        

        self._history = self._history._append({'debt': self._debt, 
                                                  'time': time, 
                                                  'amortization':amortization, 
                                                  'interest':interest,
                                                  'payment':payment,
                                                  'type':type,
                                                  'frequency':frequency}, ignore_index=True)

        # if type=='monthly':
        #     interest = self._debt * self._monthly_interest_rate
        #     amortization = self._monthly_payment - interest
        #     self._debt -= amortization
        #     # self._term -= 1
        #     #'debt', 'term', 'amortization', 'payment' 'type']
        #     self._history = self._history._append({'debt': self._debt, 
        #                                           'time': time, 
        #                                           'amortization':amortization, 
        #                                           'interest': interest,
        #                                           'payment':self._monthly_payment,
        #                                           'type':'monthly_amortization',
        #                                           'frequency':type}, ignore_index=True)
        # elif type == 'extra_term':
        #     #     new_term_months = math.log(monthly_payment / (monthly_payment - new_principal * monthly_interest_rate)) / math.log(1 + monthly_interest_rate)
        #     interest = self._debt * amortization_interest
        #     amortization = payment - interest
        #     self._debt -= payment
        #     self._term = math.log(self._monthly_payment / (self._monthly_payment - self._debt * self._interest_rate/12)) / math.log(1 + self._interest_rate/12)
        #     self._history = self._history._append({'debt': self._debt, 
        #                                           'time': time, 
        #                                           'amortization':amortization, 
        #                                           'interest': interest,
        #                                           'payment':payment,
        #                                           'type':'amortization_extra_term',
        #                                           'frequency':type}, ignore_index=True)
        # elif type == 'extra_payment':
        #     #     new_term_months = math.log(monthly_payment / (monthly_payment - new_principal * monthly_interest_rate)) / math.log(1 + monthly_interest_rate)
        #     interest = payment * amortization_interest
        #     amortization = payment - interest
        #     self._debt -= amortization
        #     # self._term = math.log(self._monthly_payment / (self._monthly_payment - self._debt * self._interest/12)) / math.log(1 + self._interest/12)
        #     self._monthly_payment = self.calculate_monthly_amortization()
        #     self._history = self._history._append({'debt': self._debt, 
        #                                           'time': time, 
        #                                           'amortization':amortization, 
        #                                           'interest':interest,
        #                                           'payment':payment,
        #                                           'type':'amortization_extra_term',
        #                                           'frequency':type}, ignore_index=True)
        
        

    


    def simulate(self):
        for y in range (0,self._term_years):
            if M._debt <= 0:
                break
            # print(f"Year: {2025 + y}")
            for m in range(0,12):
                if M._debt <= 0:
                    break
                print(f"{2025 + y} - {m+1}")
                M.amortization(self._monthly_payment, time=f"{2025 + y}-{m+1}")
                if y in [2] and m == 11:
                    M.amortization(10000, 0, 'extra_payment', time=f"{2025 + y}-{m+1}")
                if y in [] and m == 11:
                    M.amortization(10000, 0, 'extra_term', time=f"{2025 + y}-{m+1}")
                M.pay_related_expenses(f"{2025 + y}-{m+1}")

                
            


    def _toString(self):
        print("Mortage:")
        print(f" - Loan: {self._capital}")
        print(f" - Debt: {self._debt}")
        print(f" - Term: {self._term}")
        print(f" - Interests: {self._total_interests}")
        print(f" - Monthly amortization: {self._monthly_payment}")






if __name__ == '__main__':
    M = Mortage(378000, 2.1, 30)
    M.set_bank_data(bank_name='Sabadell')
    M.add_related_expense('seguro de vida', 266, 'quarterly')
    # e = M.get_related_expense('seguro de vida')
    # M.related_expense_payment('seguro de vida', '2025-12')

    initial_debt, initial_interest = M.calculate_current_debt()
    initial_term = M._term

    M.simulate()

    # total_cuotes = len(M._history[M._history]
    # len(df.loc[df.A > 0]

    
    print(M._history.head(50))

    # print(M._history.head(40))

    df = M._history[(M._history['type']=='monthly_amortization')]

    summary = {
        'total_pay':round(M._history['amortization'].sum() + M._history['interest'].sum(),2),
        'total_interest':round(M._history['interest'].sum(),2),
        'total_amortization':round(M._history['amortization'].sum(),2),
        'num_cuotes': df['payment'].count(),
        'initial_cuote': round(df['payment'][0:10].max(),2),
        'last_cuotes':round(df['payment'][-15:-5].min(),2)


    }


    

    # Create the figure and axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot on the primary y-axis (Debt)
    ax1.plot(df['time'], df['debt'], label='Debt (€)', color='blue')
    ax1.set_xlabel('Time (Months)')
    ax1.set_ylabel('Debt (€)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)

    # Plot on the secondary y-axis (Amortization)
    ax2 = ax1.twinx()
    ax2.plot(df['time'], df['payment'], label='Payment (€)', color='orange', linestyle='--')
    ax2.set_ylabel('Payment (€)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')


    # ax3 = ax1.twinx()
    ax2.plot(df['time'], df['amortization'], label='Amortization (€)', color='green', linestyle='--')
    ax2.plot(df['time'], df['interest'], label='Interest (€)', color='red', linestyle='--')
    # ax3.set_ylabel('Amortization (€)', color='orange')
    # ax3.tick_params(axis='y', labelcolor='orange')

    # Adjust x-axis labels
    ax1.set_xticks(df['time'][::12])  # Set fewer ticks
    ax1.set_xticklabels(df['time'][::12], rotation=45)  # Rotate labels

    # Add title and layout adjustments
    plt.title(M._bank_data['bank_name'])

    # Agregar resumen de resultados a la gráfica
    resumen = (
        f"Total pay: {summary['total_pay']:,.2f}€\n"
        # f"Total Interest: {summary['total_interest']:,.2f}€\n"
        f"Total Interest: {summary['total_interest']:,.2f}€\n"
        f"Total amortization: {summary['total_amortization']:,.2f}€\n"
        f"Total monthyl payments: {summary['num_cuotes']}\n"
        f"Initial cuote: {summary['initial_cuote']:,.2f}€\n"
        f"Last cuote: {summary['last_cuotes']:,.2f}€"
    )
    plt.gcf().text(0.14, 0.17, resumen, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
    fig.tight_layout()  # Adjust layout to prevent overlap

    # Show the plot
    plt.show()


    print(f"Total Interest: {summary['total_interest']}")
    print(f"Total amortization: {summary['total_amortization']}")
    print(f"Total monthyl payments: {summary['num_cuotes']}")
    print(f"Initial cuote: {summary['initial_cuote']}")
    print(f"Last cuote: {summary['last_cuotes']}")