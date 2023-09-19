import getchar

kb = getchar.Getchar()
key = ''
    
while key!='Q':
    
    key = kb.getch()
    if key != '':
        print(key)
    else:
        pass
        

