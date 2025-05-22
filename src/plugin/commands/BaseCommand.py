from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for Gini commands.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the command with the given arguments.
        """
        pass

    # @abstractmethod
    # def help(self) -> str:
    #     """
    #     Return a help string for the command.
    #     """
    #     pass
