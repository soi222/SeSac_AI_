from node import Node 

class LinkedNode(Node):
    def __init__(self, node_id, datum, next = None):
        super().__init__(node_id, datum) 
        self.next = next 

class LinkedList:
    def __init__(self, elements):
        if elements == []:
            self.head = None 
            self.tail = None 
            self.end = None
            self.size = 0
        else:
            size = 0
            for idx, e in enumerate(elements):
                assert isinstance(e, LinkedNode)
                if idx < len(elements) - 1:
                    e.next = elements[idx+1]
                size += 1
            
            head = elements[0]
            tail = LinkedList(elements[1:])
            end = elements[-1]

            assert isinstance(tail, LinkedList) or tail is None 
            assert end.next is None
            self.head = head 
            self.tail = tail 
            self.end = end 
            self.size = size 

    def __iter__(self):
        cur = self.head

        while cur is not None:
            yield cur 
            cur = cur.next 

    def __str__(self):
        cur = self.head 
        res = '[HEAD]'

        while cur is not None:
            if cur == self.head:
                res += f'[head]->[{cur}]'
            else:
                res += f'->[{cur}]'
            cur = cur.next 
        
        res += f'->[None]'

        return res 
    
    # print(lst)
    # = print(str(lst))
    # - print(LinkedList.__str__(lst))

    def append_to_head(self,elem):
        #맨 앞에 인수를 삽입
        if not isinstance(elem, LinkedNode):
            elem = LinkedNode(self.size + 1, elem)
        elem.next = self.head
        self.head = elem
        self.size += 1


    def append_to_end(self,elem):
        #맨 뒤에 인수삽입
        #원래 마지막인수의 next를 elem으로 설정, elem의 next는 none.
        if not isinstance(elem, LinkedNode):
            elem = LinkedNode(self.size + 1, elem)
        self.end.next = elem
        self.end = elem
        self.size += 1

    
    

    def insert(self,idx,elem):
        if not isinstance(elem, LinkedNode):
            elem = LinkedNode(self.size + 1, elem)
        
        if idx == 0:
            self.append_to_head(elem)
        
        else:
            cur = self.head
        cur_idx = 0
        while cur_idx < idx-1:
            cur_idx += 1
            if cur is None:
                raise IndexError
            cur = cur.next

        elem.next = cur.next
        cur.next = elem
        self.size += 1
    
    def pop(self,idx):
        pass

    def pop_from_end(self):
        pass
        
    def pop_from_head(self):
        #원래 헤드를 다음의 위치로 변경
        #사이즈 -1 
        pass
    
class DoublyLinkedNode(Node):
    def __init__(self, node_id, datum, prev = None, next = None):
        super().__init__(node_id, datum) 
        self.next = next 

class DoublyLinkedList:
    def __init__(self, elements):
        if elements == []:
            self.head = None 
            self.tail = None 
            self.end = None
            self.size = 0
        else:
            size = 0
            for idx, e in enumerate(elements):
                assert isinstance(e, DoublyLinkedNode)
                if idx < len(elements) - 1:
                    e.next = elements[idx+1]
                if 0 < idx:
                    e.prev = elements[idx-1]
                size += 1
            
            head = elements[0]
            tail = DoublyLinkedList(elements[1:])
            end = elements[-1]

            assert isinstance(tail, DoublyLinkedList) or tail is None 
            assert end.next is None

            self.head = head 
            self.tail = tail 
            self.end = end 
            self.size = size

    def __iter__(self):
        cur = self.head

        while cur is not None:
            yield cur 
            cur = cur.next 

    def __str__(self):
        cur = self.head 
        res = ''

        while cur is not None:
            if cur == self.head:
                res += f'[head]->[{cur}]'
            else:
                res += f'->[{cur}]'
            cur = cur.next 
        
        res += f'->[None]'

        return res 


