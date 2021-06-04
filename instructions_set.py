def process(n, p):
    print('Running instruction P with parameters {}, {}'.format(n,p))

def access(d, p, m):
    print('Running instruction A with parameters {}, {}, {}'.format(d, p, m))

def free(p):
    print('Running instruction L with parameters {}'.format(p))

def comment(c):
    print('Running instruction C with parameters {}'.format(c))

def end():
    print('Running instruction F')

def exit():
    print('Running instruction E')
