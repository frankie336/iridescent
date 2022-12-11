import abc
import pandas as pd
from largecollections import  base_df_dict


class ProcessDataInterface(metaclass=abc.ABCMeta):
    """Formal Interface"""
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'create_data_frame') and
                callable(subclass.create_data_frame) and

                hasattr(subclass, 'get_keywords_cpp') and
                callable(subclass.get_keywords_cpp) or

                NotImplemented)


    @abc.abstractmethod
    def create_data_frame(self):
        """
        Creates a pandas df where training
        data will be stored
        """
        raise  NotImplemented



class ProcessData(ProcessDataInterface):

    def __int__(self):
        pass

    def create_data_frame(self):


        test = pd.DataFrame([base_df_dict])
        print(test)


def test_module():

    run = ProcessData()
    run.create_data_frame()



test_module()