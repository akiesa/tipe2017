class InitialisationSingleton:
    
    class __InitialisationSingleton:
        def __init__(self, robotInitialPosition, focal):
            self.robotInitialPosition = robotInitialPosition
            self.focal=focal
            self.xTargets=[]
        def __str__(self):
            return repr(self) + self.val

            
    instance = None
    def __init__(self, robotInitialPosition, focal):
        if not InitialisationSingleton.instance:
            InitialisationSingleton.instance = InitialisationSingleton.__InitialisationSingleton(robotInitialPosition, focal)
        else:
            InitialisationSingleton.instance.robotInitialPosition = robotInitialPosition
            InitialisationSingleton.instance.focal = focal
    def __getattr__(self, name):
        return getattr(self.instance, name)
