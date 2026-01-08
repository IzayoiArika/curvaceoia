from contextlib import contextmanager
from typing import Any, ClassVar, Self

from pydantic import BaseModel, PrivateAttr, model_serializer, model_validator

from curvaceoia.utils.cfg import get_default_model_cfg


__all__ = ['AdvancedModel']

class AdvancedModel(BaseModel):

	model_config = get_default_model_cfg()
	
	val_aliases: ClassVar[dict[str, str]] = {}
	ser_rev_map: ClassVar[dict[str, str]] = {}

	mutexes: ClassVar[tuple[tuple[str, ...], ...]] = ()

	_in_batch_update: bool = PrivateAttr(default=False)

	@model_validator(mode='before')
	@classmethod
	def model_validator_before(cls, data: Any) -> Any:
		return cls.before_validation(data)
	
	@classmethod
	def before_validation(cls, data: Any) -> Any:
		if not isinstance(data, dict):
			return data
		
		data = data.copy()
		for alias, mapsto in cls.val_aliases.items():
			if alias not in data:
				continue

			data[mapsto] = data[alias]
			del data[alias]

		return data
	
	@model_serializer
	def to_dict(self) -> dict:
		cls = self.__class__
		data = {}

		for field, info in cls.model_fields.items():
			current = getattr(self, field)
			if not info.is_required() and current == info.default:
				continue
			
			data_name = cls.ser_rev_map.get(field, field)
			if isinstance(current, float):
				data[data_name] = int(current) if current.is_integer() else current

			elif isinstance(current, AdvancedModel):
				data[data_name] = current.to_dict()

			else:
				data[data_name] = current

		return data
	
	def _validate_mutexes(self) -> None:
		cls = self.__class__
		for mutex in cls.mutexes:
			attrs = [getattr(self, name) for name in mutex]
			if sum(attr is not None for attr in attrs) != 1:
				fields_str = ', '.join(list(map(repr, mutex)))
				raise ValueError(f'Fields ({fields_str}) are mutually exclusive; only one should have a value.')
			
	def _extra_check(self) -> None:
		pass
	
	def _force_check(self) -> None:
		self._validate_mutexes()
		self._extra_check()

	@model_validator(mode='after')
	def model_validator_after(self) -> Self:
		return self.after_validation()
	
	def after_validation(self) -> Self:
		if not self._in_batch_update:
			self._force_check()
		return self
	
	@contextmanager
	def batch_update(self):
		self._in_batch_update = True
		try:
			yield
		finally:
			self._in_batch_update = False
		
		self._force_check()