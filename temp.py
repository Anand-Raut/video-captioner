# class Node:
#     def __init__(self, value, prev = None, next = None):
#         self.value = value
#         self.next = next
#         self.prev = prev

# class LinkedList:

#     def __init__(self):
#         self.head = None

#     def __repr__(self):
#         values = []
#         curr = self.head
#         while curr:
#             values.append(str(curr.value))
#             curr = curr.next
#         return f"[{",".join(values)}]"
    

#     def append(self, value):
        
#         if self.head == None:
#             self.head = Node(value)
#             return
#         curr = self.head
#         while curr.next != None:
#             curr = curr.next
#         curr.next = Node(value, prev=curr)

#     def prepend(self, value):

#         if self.head == None:
#             self.head = Node(value)
#             return
#         self.head = Node(value, next=self.head)

# #     def __contains__(self, value):
# #         curr = self.head
# #         while curr != None:
# #             if curr.value == value:
# #                 return True
# #             curr = curr.next
# #         return False

# #     def __len__(self):
# #         curr = self.head
# #         count = 0
# #         while curr != None:
# #             curr = curr.next
# #             count +=1
# #         return count


# #     def append(self, value):
# #         if self.head == None:
# #             self.head = Node(value)
# #         else:
# #             last = self.head
# #             while last.next:
# #                 last = last.next
# #             last.next = Node(value)

# #     def prepend(self, value):
# #         self.head = Node(value, self.head)

# #         # first = Node(value)
# #         # first.next = self.head
# #         # self.head = first

# #     def insert (self, value, index):
# #         if index == 0:
# #             self.prepend(value)
# #             return

# #         last = self.head
# #         for _ in range(index-1):
# #             if last == None:
# #                 raise ValueError("Index out of bounds")
# #             last = last.next

# #         last.next= Node(value, last.next)

# #     def delete(self, value):
# #         if self.head is None:
# #             raise ValueError("List is empty")
# #         curr1 = self.head
# #         curr2 = self.head.next
# #         if curr1.value == value:
# #             self.head = curr1.next
# #             return
# #         while (curr2): 
# #             if curr2.value == value:
# #                 curr1.next= curr2.next
# #                 return
# #             curr1 = curr1.next
# #             curr2 = curr2.next
# #         raise ValueError("Value not found")

# #     def pop(self, index) -> int: 
# #         if self.head is None:
# #             raise ValueError("List is empty")
# #         if index == 0:
# #             value = self.head.value
# #             self.head = self.head.next
# #             return value

# #         curr = self.head
# #         for _ in range(index-1):
# #             if curr.next == None:
# #                 raise ValueError("Index out of bounds")
# #             curr = curr.next
# #         value = curr.next.value
# #         curr.next = curr.next.next
# #         return value


# #     def get(self, index):
# #         if self.head is None:
# #             raise ValueError("List is empty")
# #         if index == 0:
# #             value = self.head.value
# #             return value

# #         curr = self.head
# #         for _ in range(index-1):
# #             if curr.next == None:
# #                 raise ValueError("Index out of bounds")
# #             curr = curr.next

# #         value = curr.next.value
# #         return value

# # if __name__ == "__main__":
# #     pass
import multiprocessing

def cpu_burn():
    while True:
        pass

if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=cpu_burn)
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
