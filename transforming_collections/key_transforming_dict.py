# -*- coding: utf-8 -*-

import collections
import abc
import typing

class BaseKeyTransformingDict(collections.UserDict[object, object]):
	"""
	Dictionary that transforms keys before using them in any operation.
	Requires subclassing and implementing the key transformation function.
	"""
	@staticmethod
	@abc.abstractmethod
	def transform_key(key: object) -> object:
		"""
		Function that transforms the key before it is used in any operation.
		It must be idempotent, i.e. subsequent calls with the same key
		must return the same result.
		"""
		raise NotImplementedError
	
	@typing.override
	def __contains__(self, key: object) -> bool:
		key = self.transform_key(key)
		return super().__contains__(key)
	
	@typing.override
	def __getitem__(self, key: object) -> object:
		key = self.transform_key(key)
		return super().__getitem__(key)
	
	@typing.override
	def __setitem__(self, key: object, value: object) -> None:
		key = self.transform_key(key)
		super().__setitem__(key, value)
	
	@typing.override
	def __delitem__(self, key: object) -> None:
		key = self.transform_key(key)
		super().__delitem__(key)
	
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


class KeyTransformingDict(BaseKeyTransformingDict):
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
				v = self._mapping._getitem_without_transform(key)
			except KeyError:
				return False
			else:
				return v is value or v == value
		
		@typing.override
		def __iter__(self):
			for key in self._mapping:
				yield (key, self._mapping._getitem_without_transform(key))
	
	class ValuesView(collections.abc.ValuesView):
		@typing.override
		def __contains__(self, value: object) -> bool:
			for key in self._mapping:
				v = self._mapping._getitem_without_transform(key)
				if v is value or v == value:
					return True
			return False
		
		@typing.override
		def __iter__(self):
			for key in self._mapping:
				yield self._mapping._getitem_without_transform(key)
	
	__marker = object()
	
	def _contains_without_transform(self, key: object) -> bool:
		return super(BaseKeyTransformingDict, self).__contains__(key)
	
	def _getitem_without_transform(self, key: object) -> object:
		return super(BaseKeyTransformingDict, self).__getitem__(key)
	
	def _setitem_without_transform(self, key: object, value: object) -> None:
		super(BaseKeyTransformingDict, self).__setitem__(key, value)
	
	def _delitem_without_transform(self, key: object) -> None:
		super(BaseKeyTransformingDict, self).__delitem__(key)
	
	@typing.override
	def get(self, key: object, default: object=None) -> object:
		key = self.transform_key(key)
		if self._contains_without_transform(key):
			return self._getitem_without_transform(key)
		return default
	
	@typing.override
	def pop(self, key:object, default: object=__marker) -> object:
		key = self.transform_key(key)
		try:
			value = self._getitem_without_transform(key)
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
		value = self._getitem_without_transform(key)
		self._delitem_without_transform(key)
		return key, value
	
	@typing.override
	def setdefault(self, key: object, default: object=None) -> object:
		key = self.transform_key(key)
		try:
			return self._getitem_without_transform(key)
		except KeyError:
			self._setitem_without_transform(key, default)
		return default
	
	@typing.override
	def update(self, other=(), /, **kwds):
		if isinstance(other, type(self)):
			for key in other:
				value = other._getitem_without_transform(key)
				self._setitem_without_transform(key, value)
			if kwds:
				super().update(**kwds)
		else:
			super().update(other, **kwds)
	
	@typing.override
	def __eq__(self, other: object) -> bool:
		if isinstance(other, type(self)):
			return self.data == other.data
		if isinstance(other, collections.UserDict):
			return self.data == other.data
		if isinstance(other, collections.abc.Mapping):
			return self.data == dict(other.items())
		return NotImplemented
	
	@typing.override
	def items(self) -> collections.abc.ItemsView:
		return self.ItemsView(self)
	
	@typing.override
	def values(self) -> collections.abc.ValuesView:
		return self.ValuesView(self)
