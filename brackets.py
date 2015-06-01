def valid_bracket_combinations(n):
    if n == 0:
        return set('')
    if n == 1:
        return set(['()'])
    results = valid_bracket_combinations(n-1)
    retval = set()
    for result in results:
        for i in range(len(result)):
            if result[i] == '(':
                retval.add(insert_pair_at_idx(i+1,result))
                retval.add('()'+result)
#         retval.add(add_one_level(result))
    return retval

def insert_pair_at_idx(idx,a_string):
    return ''.join([a_string[0:idx],'()',a_string[idx:]])
            

print valid_bracket_combinations(0)
print valid_bracket_combinations(1)
print valid_bracket_combinations(2)
print valid_bracket_combinations(3)



"""
n=0, ''
n=1, '()'
n=2, '(())', '()()'
n=3, '()()()','(()())','(())()','()(())','((()))'
"""