class Category():

  def __init__(self, category):
    self.category = category
    self.ledger = []

  def get_balance(self):
    total = sum([i["amount"] for i in self.ledger])
    return total

  def check_funds(self, amount):
    balance = self.get_balance()
    return balance >= amount

  def deposit(self, amount, description=""):
    deposit_dict = {"amount": amount, "description": description}
    self.ledger.append(deposit_dict)

  def withdraw(self, amount, description=""):
    withdraw_dict = {"amount": -amount, "description": description}
    withdraw_check = self.check_funds(amount)
    if withdraw_check:
      self.ledger.append(withdraw_dict)
      return True
    else:
      return False

  def transfer(self, amount, category):
    transfer = self.withdraw(amount,
                             f"Transfer to {category.category.title()}")
    transfer
    if transfer:
      category.deposit(amount, f"Transfer from {self.category.title()}")
      return True
    else:
      return False

  def __str__(self):
    display_title = self.category.center(30, "*").title()
    display_balance = []
    for i in self.ledger:
      a = str(i["description"][0:23]).ljust(23, " ") + str(
          "%.2f" % i["amount"]).rjust(30 - 23)
      display_balance.append(a)
    display_balance = "\n".join(display_balance)

    display_total = f"\nTotal: {'%.2f'%self.get_balance()}"

    display = display_title + "\n" + display_balance + display_total
    return display


def create_spend_chart(categories):
  expenses_bycategory = list()
  total_expense = 0
  for category in categories:
    expenses_list = category.ledger
    expenses = dict()
    expenses["category"] = category.category
    expenses["amount"] = 0

    for i in expenses_list:
      if i["amount"] < 0:
        expenses["amount"] += i["amount"]
        expenses.update({"amount": expenses["amount"]})
        total_expense += i["amount"]
    expenses_bycategory.append(expenses)

  #getting each category contribution
  for i in expenses_bycategory:
    contr = i["amount"] / total_expense * 100
    #rounding it down to the nearest 10
    contr = (contr // 10)  #* 10
    i.update({"contribution": contr})

  # PLOTTING THE EXPENSES CHART
  exp_chart_title = "Percentage spent by category\n"
  plotting_list = list()
  num_spaces = len(categories) + (len(categories)) * 2 + 1

  y_axis = list()
  for y in range(100, -10, -10):
    y = f"{y}| ".rjust(5, " ")
    y_axis.append(y)
  plotting_list.append(y_axis)

  # CATEGORY BARS
  for i in expenses_bycategory:
    bar_list = list()
    bar = 10
    while i["contribution"] < bar:
      bar_list.append("   ")
      bar -= 1
      while i["contribution"] >= bar and bar >= 0:
        bar_list.append("o  ")
        bar -= 1
    plotting_list.append(bar_list)

  # Plotting y_axis and bars
  c = 0
  i = 0
  n_lines = 10
  chart_field = ""
  while i <= n_lines:
    for c in range(0, len(plotting_list)):
      if c == len(plotting_list) - 1:
        #print(plotting_list[c][i], end="  \n")
        chart_field += plotting_list[c][i] + "\n"
      else:
        #print(plotting_list[c][i], end="")
        chart_field += plotting_list[c][i]
      if c < len(plotting_list):
        c += 1
      else:
        c = 0
    i += 1

  # x_axis
  x_axis = 4 * " " + (num_spaces * "-") + "\n"
  #print(x_axis)

  x_categories = []
  for i in expenses_bycategory:
    x_categories.append(i["category"].title())
  x_cat_lines = len(max(x_categories, key=len))
  # equalizing the lenght of the categories
  i = 0
  for x_cat in x_categories:
    if len(x_cat) < x_cat_lines:
      x_cat = x_cat + (x_cat_lines - len(x_cat)) * " "
      x_categories[i] = x_cat
    i += 1

  back_spaces = list()
  for i in range(0, x_cat_lines):
    back_spaces.append(3 * " ")
  x_categories.insert(0, back_spaces)

  #print(x_categories)
  c = 0
  i = 0
  x_categ_display = ""
  while i < x_cat_lines:
    for c in range(0, len(x_categories)):
      if c == len(x_categories) - 1:
        #print(x_categories[c][i], end="  \n")
        x_categ_display += x_categories[c][i] + "  \n"
      else:
        #print(x_categories[c][i], end="  ")
        x_categ_display += x_categories[c][i] + "  "
      if c < len(x_categories):
        c += 1
      else:
        c = 0
    i += 1

  spend_chart = exp_chart_title + chart_field + x_axis + x_categ_display[
      0:-1]  #[0:-1] to remove the last "\n" in the string
  return spend_chart
