
def fizzbuzzwoof(n):
    for number in range(1,n+1):
        output = ''
        if (number%3 == 0):
            output += 'Fizz'
        if (number%5 == 0):
            output += 'Buzz'
        if (number%7 == 0):
            output += 'Woof'
        if not output:
            output = number
            
        print output
        
        
n = input('Choose a number')
fizzbuzzwoof(n)
    
