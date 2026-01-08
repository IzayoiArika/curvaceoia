from typing import Self, final

from pydantic_core.core_schema import CoreSchema, str_schema, no_info_plain_validator_function, plain_serializer_function_ser_schema


__all__ = ['LowerId']

class LowerId(str):

	__slots__ = ()

	def __new__(cls, obj: object) -> Self:
		instance = super().__new__(cls, obj)
		if not instance.isidentifier():
			raise ValueError(f'Value must be a valid identifier')
		
		if instance != instance.lower():
			raise ValueError(f'Value must be in pure lowercase')
		
		return instance
	
	@final
	@classmethod
	def __get_pydantic_core_schema__(cls, source_type, handler) -> CoreSchema:

		def validate(value):
			if isinstance(value, cls):
				return value
			try:
				return cls(value)
			except TypeError as e:
				raise ValueError(e) from e

		return no_info_plain_validator_function(
			validate,
			serialization=plain_serializer_function_ser_schema(
				lambda v: str(v),
				return_schema=str_schema()
			)
		)