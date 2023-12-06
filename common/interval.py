from sortedcontainers import SortedList
from str_util import *

# TODO: Add support for unbounded intervals using None e.g. (None, 10) is all negative numbers and positive up to 10

# Should be immutable
class Interval:
    
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __hash__(self):
        return 11 * hash(self.lower) + 17 * hash(self.upper)

    def __eq__(self, other):
        return self.lower == other.lower and self.upper == other.upper

    def __str__(self):
        return "[" + str(self.lower) + "," + str(self.upper) + "]"

    def __lt__(self, other):
        if self.lower == other.lower:
            return self.upper < other.upper
        else:
            return self.lower < other.lower

    def includes(self, value):
        return True if value >= self.lower and value <= self.upper else False
    
    def get_shifted_interval(self, shift):
        return Interval(self.lower + shift, self.upper + shift)

    def is_empty(self):
        return True if self.upper < self.lower else False


    def intersection(self, other):
        if self.includes(other.lower) or other.includes(self.lower):
            return Interval(max(self.lower, other.lower), min(self.upper, other.upper))
        else:
            return Interval(0, -1)

class IntegerIntervalSet:
    
    def __init__(self):
        self.intervals = SortedList()

    #def get_intersecting_indices(self, interval):
        

    def add_interval(self, interval):

        if interval.is_empty() or interval in self.intervals:
            return
        
        # We want to know all the intervals this one intersects or can merge with
        
        # Empty interval markers
        lower_marker = Interval(interval.lower + 1, interval.lower) #Guaranteed to be right of intervals starting with lower and left of starting with lower+1
        upper_marker = Interval(interval.upper + 2, interval.upper + 1) #Guaranteed to be right of intervals starting with upper+1 and left of starting with upper+2
        
        lower_index = self.intervals.bisect_left(lower_marker)
        upper_index = self.intervals.bisect_left(upper_marker)

        new_interval_lower = interval.lower
        new_interval_upper = interval.upper

        retain_up_to_index = lower_index
        retain_from_index = upper_index - 1 if upper_index > 0 else 0
        
        if lower_index >= 1:
            lower_interval = self.intervals[lower_index - 1]
            if lower_interval.upper >= interval.lower - 1:
                new_interval_lower = lower_interval.lower
                retain_up_to_index = lower_index - 1
                
        if upper_index >= 1:
            upper_interval = self.intervals[upper_index - 1]
            if upper_interval.upper >= interval.lower - 1:
                new_interval_upper = max(upper_interval.upper, interval.upper)
                retain_from_index = upper_index
        del self.intervals[retain_up_to_index:retain_from_index]
        self.intervals.add(Interval(new_interval_lower, new_interval_upper))



    def remove_interval(self, interval):

        if interval.is_empty():
            return
        if interval in self.intervals:
            self.intervals.remove(interval)
                
        # Empty interval markers
        lower_marker = Interval(interval.lower, interval.lower - 1) #Guaranteed to be right of intervals starting with lower-1 and left of starting with lower
        upper_marker = Interval(interval.upper + 1, interval.upper) #Guaranteed to be right of intervals starting with upper and left of starting with upper+1
        
        lower_index = self.intervals.bisect_left(lower_marker)
        upper_index = self.intervals.bisect_left(upper_marker)

        new_interval_lower = interval.lower
        new_interval_upper = interval.upper

        retain_up_to_index = lower_index
        retain_from_index = upper_index - 1 if upper_index > 0 else 0
        
        intervals_to_add = []
        
        if lower_index >= 1:
            lower_interval = self.intervals[lower_index - 1]
            if lower_interval.upper >= interval.lower:
                intervals_to_add.append(Interval(lower_interval.lower, interval.lower - 1))
                retain_up_to_index = lower_index - 1
                
        if upper_index >= 1:
            upper_interval = self.intervals[upper_index - 1]
            if upper_interval.upper >= interval.lower:
                retain_from_index = upper_index
                if upper_interval.upper > interval.upper:
                    intervals_to_add.append(Interval(interval.upper + 1, upper_interval.upper))

        del self.intervals[retain_up_to_index:retain_from_index]
        [self.intervals.add(interval_to_add) for interval_to_add in intervals_to_add]


    def contains_value(self, value):
        print("TODO")

    def intersect(self, other):
        print("TODO")

    def union(self, other):
        print("TODO")

    def __str__(self):
        return list_as_string_repr(self.intervals)

    def deep_copy(self):
        interval_set_copy = IntegerIntervalSet()
        interval_set_copy.intervals = self.intervals.copy() # Intervals should be immutable
        return interval_set_copy

""" Tests """
iis = IntegerIntervalSet()

iis.add_interval(Interval(1,5))
iis.remove_interval(Interval(2,4))
iis.add_interval(Interval(7,10))
iis.add_interval(Interval(11, 14))
iis.add_interval(Interval(7, 12))
iis.remove_interval(Interval(4,5))
iis.remove_interval(Interval(12,12))
iis.add_interval(Interval(5, 20))
iis.add_interval(Interval(4, 15))
iis.add_interval(Interval(24, 30))
iis.add_interval(Interval(100, 104))
iis.add_interval(Interval(60, 70))
iis.add_interval(Interval(65, 85))
iis.add_interval(Interval(90, 90))
iis.remove_interval(Interval(20, 95))
iis.add_interval(Interval(-50, -1))
iis.remove_interval(Interval(-59, -49))
iis.add_interval(Interval(-1, 0))
