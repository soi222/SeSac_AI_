#선입선출
import sys 
sys.path.append('../data_structure')

try:
    from linked_list import LinkedList, LinkedNode, DoublyLinkedNode, DoublyLinkedList
    
except ModuleNotFoundError:
    from data_structure.linked_list import LinkedList, LinkedNode, DoublyLinkedNode, DoublyLinkedList

class Queue:
    def __init__(self, *elements, backend = list):
        assert isinstance(elements, (list, tuple))
        
        self.backend = backend
        if self.backend == list:
            self.list = list(elements)

        elif self.backend == LinkedList:
             self.linked_list = LinkedList(list(elements))


    def elements(self):
        if self.backend == list:
            return self.list 
        
        elif self.backend == LinkedList:
            res = []
            
            cur = self.linked_list.head

            while cur is not None:
                res.append(cur.datum)
                cur = cur.next

            return res

    def enqueue(self, elem):
        if self.backend == list:
            self.list = [elem] + list(self.list)
            
        elif self.backend == LinkedList:
            return self.linked_list.append_head(elem)

    def dequeue(self):
        if self.backend == list:
            return self.list.pop()
        
        elif self.backend == LinkedList:
            return self.linked_list.pop_end()
            
                
    def front(self):
        if self.backend == list:
            return self.list[-1]
        
        elif self.backend == LinkedList:
            return self.linked_list.last_number()

    def size(self):
        if self.backend == list:
            return len(self.list)
        
        elif self.backend == LinkedList: 
            return len(self.linked_list)
    
    def is_empty(self):
        if self.backend == list:
            return len(self.list) == 0
        
        elif self.backend == LinkedList:
            if self.size == 0:
                return len(self.linked_list) == 0
            return len(self.linked_list) == 0
            

    def __str__(self):
        return str(self.elements())

    def __eq__(self, other):
        if isinstance(other, Queue):
            return self.elements == other.elements 
        return False 

class PriorityQueue:
    def __init__(self, *elements_with_priority, backend = list):
        """Get list of 2-tuple containing (obj, number), which denotes object and its priority. Higher the number, the element have hight priority. 
        """
        self.backend = backend

        if self.backend == list:
            self.list = list(elements_with_priority)
            self.list.sort(key = lambda x : x[1])

        elif self.backend == LinkedList:
            a = list(elements_with_priority)
            a.sort(key= lambda x : x[1])
            self.linked_list = LinkedList(a)


    def elements(self):
        if self.backend == list:
            return self.list 
        
        elif self.backend == LinkedList:
            res = []
            cur = self.linked_list.head

            while cur is not None:
                res.append(cur.datum)
                cur = cur.next

            return res
    

    def enqueue(self, elem):
        if self.backend == list:
            self.list.append(elem)
            self.list.sort(key=lambda x: x[1])
            return self.list

        elif self.backend == LinkedList:
            cur = self.linked_list.head
            new_node = LinkedNode(node_id = None, datum=elem)
        
            if cur is None or cur.datum[1] < elem[1]:
                self.linked_list.append_head(elem)

            else:
                while cur.next.datum[1] >= elem[1]:
                    cur = cur.next
                new_node.next = cur.next
                cur.next = new_node

            return list(self.elements())
             


    def dequeue(self):
        if self.backend == list:
            return self.list.pop()

        elif self.backend == LinkedList:
            return self.linked_list.pop_end()
                
    def front(self):
        if self.backend == list:
            return self.list[-1]
        
        elif self.backend == LinkedList:
            return self.linked_list.last_number()
            #return self.linked_list.end.datum
            

    def size(self):
        if self.backend == list:
            return len(self.list)
        
        elif self.backend == LinkedList:
            return len(self.linked_list)
    
    def is_empty(self):
        if self.backend == list:
            return len(self.list) == 0
        
        elif self.backend == LinkedList:
            return len(self.linked_list) == 0

    def __str__(self):
        return str(self.elements())

    def __eq__(self, other):
        if isinstance(other, Queue):
            return self.elements() == other.elements 
        return False 

if __name__ == '__main__':
    available_backends = [list, LinkedList]#DoublyLinkedList


    for backend in available_backends:
        q1 = Queue(1,2,3,4, backend = backend)

        assert q1.elements() == [1,2,3,4]
        assert q1.size() == 4
        
        q1.enqueue(5)
        assert q1.elements() == [5,1,2,3,4]
        assert q1.size() == 5
        assert q1.dequeue() == 4

        assert q1.size() == 4
        assert q1.elements() == [5,1,2,3]
        assert q1.front() == 3 


        q2 = Queue(backend = backend)

        assert q2.elements() == []
        assert q2.size() == 0
        assert q2.is_empty()
        
        q2.enqueue(1)

        assert q2.elements() == [1]
        assert q2.size() == 1
        assert not q2.is_empty()

        if backend == LinkedList:
            print(q1.linked_list, q2.linked_list)
    
        q2 = PriorityQueue(('c',1), ('d',4), ('e',2), ('b',3), backend = backend)
        print("q2 is ",q2)
        assert q2.elements() == [('c',1), ('e',2), ('b',3), ('d',4)]
        assert q2.size() == 4 
        assert q2.front() == ('d', 4) 
        assert not q2.is_empty()
        q2.dequeue()

        assert q2.elements() == [('c',1), ('e',2), ('b',3)]
        assert q2.size() == 3 
        assert q2.front() == ('b', 3) 
        assert not q2.is_empty()
        
        print(q2)
        q2.dequeue()
        print(q2)
        q2.dequeue()
        print(q2)
        q2.dequeue()
        print(q2)
        

        assert q2.is_empty()
        print("list ls empty")

#시간
#append >> lst1 + lst2