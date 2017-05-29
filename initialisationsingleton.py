class InitialisationSingleton:
    
    class __InitialisationSingleton:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val

            
    instance = None
    def __init__(self, arg):
        if not InitialisationSingleton.instance:
            InitialisationSingleton.instance = InitialisationSingleton.__InitialisationSingleton(arg)
        else:
            InitialisationSingleton.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
