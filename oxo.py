
# o | x | o
# __|___|__
#   |   |
# x | o | x
# __|___|__
#   |   |
# o | x | o

grid = """
 1   2   3
1 %s | %s | %s
  __|___|__
    |   |
2 %s | %s | %s 
  __|___|__
    |   |
3 %s | %s | %s
"""

def print_grid(cell_11):
    print grid % cell_11
    
   
print_grid(' ')
print_grid('x')
print_grid('o')
    