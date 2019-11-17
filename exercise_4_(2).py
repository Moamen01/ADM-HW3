def initial_string(s):
    n = len(s)
    if n == 0 or n == 1:         
        k = n
                                
    else:
        if s[0] == s[-1]:          
            return 2+initial_string(s[1:-1])
        else:
            return max(initial_string(s[:-1]), initial_string(s[1:]))
    return k
	

print(initial_string('DATAMININGSAPIENZA'))	
	
	
	

	
	
	

