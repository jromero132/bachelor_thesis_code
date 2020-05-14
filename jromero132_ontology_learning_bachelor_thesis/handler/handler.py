from abc import ABC, abstractmethod


class Handler(ABC):
	@abstractmethod
	def handle(self, request):
		pass