# It is strongly suggested to us a separate file to define the io of your tile and process. 
# it will help you to have control over it's fonctionality using object oriented programming

# in python variable are not mutable object (their value cannot be changed in a function)
# Thus use a class to define your input and output in order to have mutable variables
class ProcessIo:
    def __init__(self):
        # set up your inputs
        self.year_beg     = None
        self.year_end     = None
        self.scale        = 30
        self.type_tmf     = 'DEG'
        
        # set up your outputs
        self.asset_id = None
        self.dataset  = None