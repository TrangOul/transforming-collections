# -*- coding: utf-8 -*-

import unittest
import unittest.mock
import collections

from .test_base_key_transforming_dict import TestKeyTransformingDict, KeyTransformingDictBaseTestMixin

class KeyTransformingDictPerformanceTestMixin:
	def test_fromkeys_transform_once(self):
		keys = (self.KEY_UNTRANSFORMED, )
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class.fromkeys(keys, 'fromkeys')
			transform_key_mock.assert_called_once()
	
	def test_fromkeys_transform_once_per_key(self):
		keys = (self.KEY_UNTRANSFORMED, self.KEY_TRANSFORMED)
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class.fromkeys(keys, 'fromkeys')
			self.assertEqual(transform_key_mock.call_count, len(keys), "transform_key should be called once for each key")
	
	def test_init_same_class_no_transforms(self):
		source_dict = self.test_class({self.KEY_UNTRANSFORMED: 'untransformed'})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_dict)
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for init with same class")
	
	def test_init_dict_transform_once(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'untransformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_dict)
			transform_key_mock.assert_called_once()
	
	def test_init_list_transform_once(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'untransformed']]
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_list)
			transform_key_mock.assert_called_once()
	
	def test_init_kwargs_transform_once(self):
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(**source_kwargs)
			transform_key_mock.assert_called_once()
	
	
	def test_init_dict_transform_once_per_key(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_dict)
			self.assertEqual(transform_key_mock.call_count, len(source_dict), "transform_key should be called once for each key")
	
	def test_init_list_transform_once_per_key(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'untransformed'], [self.KEY_TRANSFORMED, 'transformed']]
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_list)
			self.assertEqual(transform_key_mock.call_count, len(source_list), "transform_key should be called once for each key")
	
	def test_init_kwargs_transform_once_per_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(**source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_kwargs), "transform_key should be called once for each key")
	
	
	def test_init_same_class_kwargs_transform_once_per_key(self):
		source_dict = self.test_class({self.KEY_UNTRANSFORMED: 'untransformed'})
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_dict, **source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_kwargs), "transform_key should be called once for each key from kwargs")
	
	def test_init_dict_kwargs_transform_once_per_key(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'untransformed'}
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_dict, **source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_dict) + len(source_kwargs), "transform_key should be called once for each key")
	
	def test_init_list_kwargs_transform_once_per_key(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'untransformed']]
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			self.test_class(source_list, **source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_list) + len(source_kwargs), "transform_key should be called once for each key")
	
	
	def test_update_dict_transform_once(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'dict'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_dict)
			transform_key_mock.assert_called_once()
	
	def test_update_list_transform_once(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'list']]
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_list)
			transform_key_mock.assert_called_once()
	
	def test_update_kwargs_transform_once(self):
		source_kwargs = {self.KEY_UNTRANSFORMED: 'kwargs'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(**source_kwargs)
			transform_key_mock.assert_called_once()
	
	
	def test_update_dict_transform_once_per_key(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_dict)
			self.assertEqual(transform_key_mock.call_count, len(source_dict), "transform_key should be called once for each key")
	
	def test_update_list_transform_once_per_key(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'untransformed'], [self.KEY_TRANSFORMED, 'transformed']]
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_list)
			self.assertEqual(transform_key_mock.call_count, len(source_list), "transform_key should be called once for each key")
	
	def test_update_kwargs_transform_once_per_key(self):
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(**source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_kwargs), "transform_key should be called once for each key")
	
	
	def test_update_dict_kwargs_transform_once_per_key(self):
		source_dict = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_dict, **source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_dict) + len(source_kwargs), "transform_key should be called once for each key")
	
	def test_update_list_kwargs_transform_once_per_key(self):
		source_list = [[self.KEY_UNTRANSFORMED, 'untransformed'], [self.KEY_TRANSFORMED, 'transformed']]
		source_kwargs = {self.KEY_UNTRANSFORMED: 'untransformed', self.KEY_TRANSFORMED: 'transformed'}
		d = self.test_class({self.KEY_TRANSFORMED: 'original'})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.update(source_list, **source_kwargs)
			self.assertEqual(transform_key_mock.call_count, len(source_list) + len(source_kwargs), "transform_key should be called once for each key")
	
	def test_len_no_transforms(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			len(d)
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for len")
	
	
	def test_in_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			self.KEY_UNTRANSFORMED in d
			transform_key_mock.assert_called_once()
	
	
	def test_getitem_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d[self.KEY_UNTRANSFORMED]
			transform_key_mock.assert_called_once()
	
	
	def test_get_present_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.get(self.KEY_UNTRANSFORMED)
			transform_key_mock.assert_called_once()
	
	def test_get_missing_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.get(self.KEY_UNTRANSFORMED_2)
			transform_key_mock.assert_called_once()
	
	
	def test_setitem_transform_once(self):
		d = self.test_class()
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d[self.KEY_UNTRANSFORMED] = 1
			transform_key_mock.assert_called_once()
	
	
	def test_delitem_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			del d[self.KEY_UNTRANSFORMED]
			transform_key_mock.assert_called_once()
		
	def test_pop_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.pop(self.KEY_UNTRANSFORMED)
			transform_key_mock.assert_called_once()
	
	
	def test_popitem_no_transforms(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.popitem()
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for popitem")
	
	
	def test_clear_no_transforms(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.clear()
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not be called for clear")
	
	
	def test_setdefault_missing_transform_once(self):
		d = self.test_class()
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.setdefault(self.KEY_UNTRANSFORMED, 1)
			transform_key_mock.assert_called_once()
		
			
	def test_setdefault_present_transform_once(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			d.setdefault(self.KEY_UNTRANSFORMED, 1)
			transform_key_mock.assert_called_once()
	
	def test_iter_no_transform(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
			list(iter(d))
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called during iteration")
		
	def test_keys_no_transform(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			list(d.keys())
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for keys")
	
	def test_items_no_transform(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			list(d.items())
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for items")
		
	def test_values_no_transform(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			list(d.values())
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called for values")
	
	
	def test_copy_method_transform_once_per_key(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			d.copy()
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called during copying")
		
	def test_copy_transform_once_per_key(self):
		import copy
		
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			copy.copy(d)
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called during copying")
			
	def test_deepcopy_transform_once_per_key(self):
		import copy
		
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			copy.deepcopy(d)
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not have been called during copying")
	
	
	def test_or_no_transform_this_class(self):
		d1 = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		d2 = self.test_class({self.KEY_TRANSFORMED: 3, self.KEY_TRANSFORMED_3: 4})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			d1 | d2
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not be called when oring with the same class")
	
	def test_ior_no_transform_this_class(self):
		d1 = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		d2 = self.test_class({self.KEY_TRANSFORMED: 3, self.KEY_TRANSFORMED_3: 4})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			d1 |= d2
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not be called when ioring with the same class")
	
	
	def test_or_transform_once_per_key_other_class(self):
		source_dict = {
			self.KEY_UNTRANSFORMED: 1,
			self.KEY_TRANSFORMED: 2,
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED: 1})
				
				with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
					d1 | d2
					self.assertEqual(transform_key_mock.call_count, len(d2), "transform_key should be called once for each key in the other dict")
	
	def test_ror_transform_once_per_key_other_class(self):
		source_dict = {
			self.KEY_UNTRANSFORMED: 1,
			self.KEY_TRANSFORMED: 2,
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED: 1})
				
				with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
					d2 | d1
					self.assertEqual(transform_key_mock.call_count, len(d2), "transform_key should be called once for each key in the other dict")
	
	def test_ior_transform_once_per_key_other_class(self):
		source_dict = {
			self.KEY_UNTRANSFORMED: 1,
			self.KEY_TRANSFORMED: 2,
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED: 1})
				
				with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
					d1 |= d2
					self.assertEqual(transform_key_mock.call_count, len(d2), "transform_key should be called once for each key in the other dict")
	
	
	def test_eq_no_transforms_this_class(self):
		d1 = self.test_class({self.KEY_TRANSFORMED: 1})
		d2 = self.test_class({self.KEY_TRANSFORMED: 1})
		
		with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
			d1 == d2
			self.assertEqual(transform_key_mock.call_count, 0, "transform_key should not be called for equality on same class")
	
	def test_eq_transform_once_per_key_other_class(self):
		source_dict = {
			self.KEY_UNTRANSFORMED: 1,
			self.KEY_TRANSFORMED: 2,
			self.KEY_UNTRANSFORMED_2: 3,
			self.KEY_TRANSFORMED_2: 4,
		}
		
		ds = (
			source_dict,
			collections.Counter(source_dict),
			collections.OrderedDict(source_dict),
			collections.defaultdict(None, source_dict),
			collections.UserDict(source_dict),
		)
		
		for d2 in ds:
			with self.subTest(type_=type(d2).__name__):
				d1 = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
				with unittest.mock.patch.object(self.test_class, 'transform_key', wraps=self.test_class.transform_key) as transform_key_mock:
					d1 == d2
					self.assertEqual(transform_key_mock.call_count, 0, "transform_key should be called once per key when comparing with another mapping")
	
	def test_builtin_cast_no_transform(self):
		d = self.test_class({self.KEY_TRANSFORMED: 1, self.KEY_TRANSFORMED_2: 2})
		
		collection_types = {
			list,
			tuple,
			set,
			frozenset,
			dict, # FIXME currently unfixable; dict calls __iter__ and then __getitem__ for each key
			str,
			repr,
		}
		
		for collection_type in collection_types:
			with self.subTest(type_=collection_type.__name__):
				with unittest.mock.patch.object(d, 'transform_key', wraps=d.transform_key) as transform_key_mock:
					collection_type(d)
					self.assertEqual(transform_key_mock.call_count, 0, f"transform_key should not be called when casting to {collection_type.__name__}")


class TestKeyTransformingDictPerformance(unittest.TestCase, KeyTransformingDictPerformanceTestMixin, KeyTransformingDictBaseTestMixin):
	test_class = TestKeyTransformingDict


if __name__ == '__main__':
	unittest.main()
