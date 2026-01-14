from typing import Self

from curvaceoia1.aff.models.base import GameObjectEvent


__all__ = ['FloorEvent', 'SkyEvent', 'LongNoteEvent', 'TapLikeEvent']

class FloorEvent(GameObjectEvent):
	pass

class SkyEvent(GameObjectEvent):
	pass

class LongNoteEvent(GameObjectEvent):
	@property
	def time_range(self) -> tuple[int, int]:
		return (self.begin_time, self.end_time)
	
	@time_range.setter
	def time_range(self, value: tuple[int, int]) -> None:
		begin, end = value
		if begin > end:
			raise ValueError(f'Invalid time range; begin should not be greater than end')
		
		if begin <= self.end_time:
			self.begin_time, self.end_time = begin, end
		else:
			self.end_time, self.begin_time = end, begin

	@property
	def duration(self) -> int:
		return self.end_time - self.begin_time
	
	def __len__(self) -> int:
		return self.duration
	
	def after_validation(self) -> Self:
		super().after_validation()
		if self.end_time < self.begin_time:
			raise ValueError('end_time must be greater than or equal to begin_time')
		return self

class TapLikeEvent(GameObjectEvent):
	pass