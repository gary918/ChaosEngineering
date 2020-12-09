import random
import time
import threading
import collections

class default_injected_exception(Exception):
    pass

class FaultInjectionStatus:
    def __init__ (self):
        self.reset_status ()    

    def reset_status(self):
        self.latency_injected = False
        self.latency = 0
        self.exception_raised = False
        self.injected_exception = None     


    def get_last_status(self):
        Status = collections.namedtuple('Status', ['latency_injected', 'latency', 'exception_raised','injected_exception'])
        return  Status (latency_injected=self.latency_injected, latency=self.latency, 
                            exception_raised=self.exception_raised, injected_exception=self.injected_exception)

class FaultInjector:


    random.seed()
    
    def __get_next_random_number (self) -> float:
        return random.random()


    def __should_inject_latency(self, is_enabled: bool, latency_injection_rate: int) -> bool:
        if ((is_enabled == False) or (latency_injection_rate <= 0)):
            return False
        print(f"....latency_injection_rate:{latency_injection_rate}")
        if (self.__get_next_random_number() <= latency_injection_rate  / 100.0):
            return True
        else:
            return False

      
    def __cause_sleep (self, sleepTime : int):
        sleepTimeInSeconds = sleepTime / 1000
        time.sleep (sleepTimeInSeconds)


    def __should_inject_exception(self, is_enabled: bool, exception_injection_rate: int) -> bool:
        if ((is_enabled == False) or (exception_injection_rate <= 0)):
            return False
        if (self.__get_next_random_number() <= exception_injection_rate / 100.0):
            return True
        else:
            return False


    def __inject_latency (self, min_latency: int, max_latency: int, latency_function):
        latencyRange = max_latency - min_latency
        latencyRatio = self.__get_next_random_number()
        latency = min_latency + (latencyRange * latencyRatio)
        print ('.....Delaying %d ...' % latency)
        self.faultInjectionStatus.latency_injected = True
        self.faultInjectionStatus.latency = latency
        latency_function (self, latency)
        # print ('Delay complete')


    def __init__ (self, is_enabled=False, 
                        min_latency=0, max_latency=0, latency_injection_rate=0, latency_function=__cause_sleep,
                        exception_injection_rate=0, injected_exception=default_injected_exception('Default Chaos Exception raised') 
                        ):
        self.is_enabled = is_enabled
        self.min_latency = min_latency
        self.max_latency = max_latency
        self.latency_injection_rate = latency_injection_rate
        self.latency_function = latency_function        
        self.exception_injection_rate = exception_injection_rate
        self.injected_exception = injected_exception
        self.faultInjectionStatus = FaultInjectionStatus()


    def __call__ (self, func, args):
        self.faultInjectionStatus.reset_status()

        if (self.__should_inject_latency(self.is_enabled, self.latency_injection_rate)):
            self.__inject_latency (self.min_latency, self.max_latency, self.latency_function)
        
        if (self.__should_inject_exception(self.is_enabled, self.exception_injection_rate)):
            #print('Raising injected exception ...')
            self.faultInjectionStatus.exception_raised = True
            self.faultInjectionStatus.injected_exception = self.injected_exception
            raise self.injected_exception

        val = func(*args)
        return val
        
    def get_last_status (self):
        return self.faultInjectionStatus.get_last_status()