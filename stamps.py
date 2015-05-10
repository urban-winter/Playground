'''
Created on 2 May 2015

@author: Piers
'''
first_class = 63
second_class = 54
target = 280

def find_closest_stamp_combination(target):
    '''returns (number of first class, number of second class, total value)'''
    closest_amt = None
    for firsts in range(0,1000):
        for seconds in range(0,1000):
            total = firsts * first_class + seconds * second_class
            if closest_amt is None or (abs(target-total) < abs(target-closest_amt) and total >= target):
                closest_amt = total
                closest_vals = (firsts,seconds)
    print 'Best is %s firsts, %s seconds, total %s' % (closest_vals[0], closest_vals[1], closest_amt)
    return (firsts, seconds, total)

for target in range(1,500):
     find_closest_stamp_combination(target)

# target = input('Target amount?')
# find_closest_stamp_combination(target)