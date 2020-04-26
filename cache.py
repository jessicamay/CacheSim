class cache():
    #initializing cache parameters
    cache_size = 0
    data_size = 0
    associativity = 0
    replace = 0
    write_hit = 0
    write_miss = 0
    
    #parameterized constructor
    def __init__(self, cache_size, data_size, associativity, replace, write_hit, write_miss):
        self.cache_size = cache_size
        self.data_size = data_size
        self.associativiy = associativity
        self.replace = replace
        self.write_hit = write_hit
        self.write_miss = write_miss