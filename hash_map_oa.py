# Name: Serkan Bayramoglu
# OSU Email: bayramos@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 11 March 2022
# Description:  This project implements the HashMap class using a dynamic array to store hashtable and
#               implementing Open Addressing with Quadratic Probing for collision resolution.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the content of the hash map
        """
        self.__init__(self.capacity, self.hash_function)

    def get(self, key: str) -> object:
        """
        This method returns the value associated with a key stored in the hash map
        """
        initial_hash = self.hash_function(key)
        data_index = initial_hash % self.capacity
        current_data = self.buckets.get_at_index(data_index)
        counter = 0
        while current_data is not None:
            if current_data.key == key and current_data.is_tombstone is False:
                return current_data.value
            counter += 1
            new_hash = initial_hash + (counter ** 2)
            data_index = new_hash % self.capacity
            current_data = self.buckets.get_at_index(data_index)
        return None

    def put(self, key: str, value: object) -> None:
        """
        This method inserts a HashEntry with key - value pair into the hash map
        """
        # remember, if the load factor is greater than 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        initial_hash = self.hash_function(key)
        data_index = initial_hash % self.capacity
        current_data = self.buckets.get_at_index(data_index)
        counter = 0
        while current_data is not None and current_data.is_tombstone is False and current_data.key != key \
                and counter < self.capacity:
            counter += 1
            new_hash = initial_hash + (counter ** 2)
            data_index = new_hash % self.capacity
            current_data = self.buckets.get_at_index(data_index)
        if counter < self.capacity:
            if current_data is None:
                self.size += 1
            elif current_data.is_tombstone == True:
                self.size += 1
            self.buckets.set_at_index(data_index, HashEntry(key, value))


    def remove(self, key: str) -> None:
        """
        This method removes the HashEntry for the requested key in the hash map
        """
        # quadratic probing required
        initial_hash = self.hash_function(key)
        data_index = initial_hash % self.capacity
        current_data = self.buckets.get_at_index(data_index)
        counter = 0
        while current_data is not None:
            if current_data.key == key and current_data.is_tombstone is False:
                current_data.is_tombstone = True
                self.buckets.set_at_index(data_index, current_data)
                self.size -= 1
                return None
            counter += 1
            new_hash = initial_hash + (counter ** 2)
            data_index = new_hash % self.capacity
            current_data = self.buckets.get_at_index(data_index)
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the hash map contains a queried key, or False otherwise
        """
        # quadratic probing required
        initial_hash = self.hash_function(key)
        data_index = initial_hash % self.capacity
        current_data = self.buckets.get_at_index(data_index)
        counter = 0
        while current_data is not None:
            if current_data.key == key and current_data.is_tombstone is False:
                return True
            counter += 1
            new_hash = initial_hash + (counter ** 2)
            data_index = new_hash % self.capacity
            current_data = self.buckets.get_at_index(data_index)
        return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in a hash map
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        This method calculates and returns the table load for a hash map
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        This method resizes a hash map to a given new capacity
        """
        if new_capacity > self.size:
            new_table = HashMap(new_capacity, self.hash_function)
            for index in range(self.capacity):
                current_data = self.buckets.get_at_index(index)
                if current_data is not None and current_data.is_tombstone is False:
                    new_table.put(current_data.key, current_data.value)
            self.__init__(new_table.capacity, self.hash_function)
            self.size = new_table.size
            self.buckets = new_table.buckets

    def get_keys(self) -> DynamicArray:
        """
        This method returns all the keys stored in a hash map in a dynamic array
        """
        new_array = DynamicArray()
        for index in range(self.capacity):
            current_data = self.buckets.get_at_index(index)
            if current_data is not None and current_data.is_tombstone is False:
                new_array.append(current_data.key)

        return new_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
