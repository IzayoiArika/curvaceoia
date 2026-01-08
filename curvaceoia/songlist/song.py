from typing import ClassVar, Literal

from pydantic import NonNegativeInt as uint, PositiveFloat as posfloat

from curvaceoia.songlist.i18ns import I18nBool, I18nStrEnRequired, I18nStrs
from curvaceoia.songlist.lowerid import LowerId
from curvaceoia.songlist.model import AdvancedModel


__all__ = [
	'BaseSong', 'DeletedSong', 'Song',
	'SongDifficulty', 'AdditionalFile', 'BgDayNight',
	'SongList',
]

class BaseSong(AdvancedModel):

	idx: uint
	id: LowerId
	deleted: bool

class DeletedSong(BaseSong):
	deleted: Literal[True] # type: ignore

class SongDifficulty(AdvancedModel):

	ratingClass: Literal[0, 1, 2, 3, 4]

	# title: str | None = None
	title_localized: I18nStrEnRequired | None = None

	audioOverride: bool | None = None

	chartDesigner: str

	jacketDesigner: str
	jacketOverride: bool | None = None

	rating: int
	ratingPlus: bool | None = None

	jacket_night: str | None = None

	legacy11: bool | None = None

	artist: str | None = None
	# artist_localized: I18nStrEnRequired | None = None

	bpm: str | None = None
	bpm_base: posfloat | None = None

	bg: str | None = None
	bg_inverse: str | None = None

	date: uint | None = None
	version: str = ''

	hidden_until: Literal[None, 'always', 'difficulty', 'none', 'song', 'unlockconditions'] = None
	hidden_until_unlocked: bool | None = None

	world_unlock: bool | None = None

	plusFingers: bool | None = None

	# mutexes: ClassVar[tuple[tuple[str, str], ...]] = (
	# 	('artist', 'artist_localized'),
	# 	('title', 'title_localized'),
	# )

class AdditionalFile(AdvancedModel):
	file_name: str
	requirement: Literal['hi_res', 'required', 'low_res']

class BgDayNight(AdvancedModel):
	day: str
	night: str

class Song(BaseSong):
	deleted: Literal[False] | None = None # type: ignore

	title: str | None = None
	title_localized: I18nStrEnRequired | None = None

	artist: str | None = None
	artist_localized: I18nStrEnRequired | None = None
	
	search_title: I18nStrs | None = None
	search_artist: I18nStrs | None = None

	bpm: str
	bpm_base: posfloat

	set: LowerId # "set"
	category: Literal[None, 'musicgames', 'partner', 'poprec', 'original', 'variety'] = None
	purchase: LowerId | Literal[""]

	audioPreview: uint
	audioPreviewEnd: uint

	side: Literal[0, 1, 2, 3]
	
	remote_dl: bool | None = None
	
	world_unlock: bool | None = None

	bg: str
	bg_inverse: str | None = None

	date: uint | None = None
	version: str = ''

	difficulties: list[SongDifficulty]

	songlist_hidden: bool | None = None
	byd_local_unlock: bool | None = None
	
	jacket_localized: I18nBool | None = None

	additional_files: list[AdditionalFile] | None = None
	bg_daynight: BgDayNight | None = None

	limitedSaleEndTime: uint | None = None
	no_stream: bool | None = None
	source_copyright: str | None = None
	source_localized: I18nStrEnRequired | None = None
	
	# val_aliases: ClassVar[dict[str, str]] = {'set': 'pack'}
	# ser_rev_map: ClassVar[dict[str, str]] = {'pack': 'set'}

	mutexes: ClassVar[tuple[tuple[str, str], ...]] = (
		('artist', 'artist_localized'),
		('title', 'title_localized'),
	)

	def _extra_check(self) -> None:
		# if self.pack != 'single':
		# 	self.__dict__['category'] = None

		if self.audioPreview > self.audioPreviewEnd:
			raise ValueError(f'audioPreview should not be later than audioPreviewEnd')
		
class SongList(AdvancedModel):
	songs: list[DeletedSong | Song]
