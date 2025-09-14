# -*- coding: utf-8 -*-

import collections
import abc
import typing


class KeyTransformingDict(collections.UserDict):
	"""
	Dictionary that transforms keys before using them in any operation.
	Requires subclassing and implementing the key transformation function.
	Optimized so keys are transformed only when necessary, and without repeated redundant transformations.
	Best for cases where transforming a key is an expensive operation.
	"""
	class ItemsView(collections.abc.ItemsView):
		@typing.override
		def __contains__(self, item: object) -> bool:
			key, value = item
			key = self._mapping.transform_key(key)
			try:
				v = self._mapping._getitem_without_transform(key)[1]
			except KeyError:
				return False
			else:
				return v is value or v == value
		
		@typing.override
		def __iter__(self):
			for key in self._mapping:
				yield (key, self._mapping._getitem_without_transform(key)[1])
	
	class ValuesView(collections.abc.ValuesView):
		@typing.override
		def __contains__(self, value: object) -> bool:
			for key in self._mapping:
				v = self._mapping._getitem_without_transform(key)[1]
				if v is value or v == value:
					return True
			return False
		
		@typing.override
		def __iter__(self):
			for key in self._mapping:
				yield self._mapping._getitem_without_transform(key)[1]
	
	__marker = object()
	
	@staticmethod
	@abc.abstractmethod
	def transform_key(key: object) -> object:
		"""
		Function that transforms the key before it is used in any operation.
		It must be idempotent, i.e. subsequent calls with the same key
		must return the same result.
		"""
		raise NotImplementedError
	'''
	#TODO
	def __init__(self, transform_key, replace_keys:bool=False, *args, **kwargs):
		self.transform_key = transform_key
		self.replace_keys = replace_keys
		super().__init__(*args, **kwargs)
	'''
	@classmethod
	def factory(cls, name: str, key_transformer):
		return type( name, (cls,), { 'transform_key': staticmethod(key_transformer) } )
	@typing.override
	def __contains__(self, key: object) -> bool:
		key = self.transform_key(key)
		return self._contains_without_transform(key)
	
	@typing.override
	def __getitem__(self, key: object) -> object:
		key = self.transform_key(key)
		return self._getitem_without_transform(key)[1]
	
	@typing.override
	def __setitem__(self, key: object, value: object) -> None:
		transformed_key = self.transform_key(key)
		return self._setitem_without_transform(transformed_key, key, value)
	
	@typing.override
	def __delitem__(self, key: object) -> None:
		key = self.transform_key(key)
		return self._delitem_without_transform(key)
	
	@typing.override
	def __or__(self, other: object) -> typing.Self:
		if not isinstance(other, collections.abc.Mapping):
			return NotImplemented
		new = type(self)(self)
		new.update(other)
		return new
	
	@typing.override
	def __ror__(self, other: object) -> typing.Self:
		if not isinstance(other, collections.abc.Mapping):
			return NotImplemented
		new = type(self)(other)
		new.update(self)
		return new
	
	@typing.override
	def __ior__(self, other: object) -> typing.Self:
		if not isinstance(other, collections.abc.Mapping):
			return NotImplemented
		self.update(other)
		return self
	
	@property
	def _dict(self):
		return {key: item[1] for key, item in self.data.items()}
	
	def _contains_without_transform(self, key: object) -> bool:
		return super().__contains__(key)
	
	def _getitem_without_transform(self, key: object) -> tuple[object, object]:
		return super().__getitem__(key)
	
	def _setitem_without_transform(self, transformed_key: object, original_key: object, value: object) -> None:
		super().__setitem__(transformed_key, (original_key, value))
	
	def _delitem_without_transform(self, key: object) -> None:
		super().__delitem__(key)
	
	@typing.override
	def get(self, key: object, default: object=None) -> object:
		key = self.transform_key(key)
		if self._contains_without_transform(key):
			return self._getitem_without_transform(key)[1]
		return default
	
	@typing.override
	def pop(self, key:object, default: object=__marker) -> object:
		key = self.transform_key(key)
		try:
			value = self._getitem_without_transform(key)[1]
		except KeyError:
			if default is self.__marker:
				raise
			return default
		else:
			self._delitem_without_transform(key)
			return value
	
	@typing.override
	def popitem(self) -> tuple[object, object]:
		try:
			key = next(iter(self))
		except StopIteration:
			raise KeyError from None
		original_key, value = self._getitem_without_transform(key)
		self._delitem_without_transform(key)
		return original_key, value
	
	@typing.override
	def setdefault(self, key: object, default: object=None) -> object:
		transformed_key = self.transform_key(key)
		try:
			return self._getitem_without_transform(transformed_key)[1]
		except KeyError:
			self._setitem_without_transform(transformed_key, key, default)
		return default
	
	@typing.override
	def update(self, other=(), /, **kwds):
		if isinstance(other, type(self)):
			for key in other.data:
				original_key, value = other._getitem_without_transform(key)
				self._setitem_without_transform(key, original_key, value)
			if kwds:
				super().update(**kwds)
		else:
			super().update(other, **kwds)
	
	@typing.override
	def __eq__(self, other: object) -> bool:
		if isinstance(other, type(self)):
			return self.data == other.data
		if isinstance(other, collections.UserDict):
			return self._dict == other.data
		if isinstance(other, collections.abc.Mapping):
			return self._dict == dict(other.items())
		return NotImplemented
	
	def __iter__(self):
		return (v[0] for v in self.data.values())
	
	@typing.override
	def items(self) -> collections.abc.ItemsView:
		return self.ItemsView(self)
	
	@typing.override
	def values(self) -> collections.abc.ValuesView:
		return self.ValuesView(self)
