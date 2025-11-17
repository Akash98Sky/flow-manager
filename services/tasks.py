from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def execute(self):
        pass

class FetchDataTask(Task):
    def execute(self):
        # Fetch data logic
        return True

class ProcessDataTask(Task):
    def execute(self):
        # Process data logic
        return True

class StoreDataTask(Task):
    def execute(self):
        # Store data logic
        return True
