try:
    from node import Node 
except ModuleNotFoundError:
    from data_structure.node import Node

#linked_list : 다음노드에 대한 정보를 담고 있는 데이터구조
class LinkedNode:
    def __init__(self, node_id, datum, next = None):
        self.node_id = node_id 
        self.datum = datum 
        self.next = next 

class LinkedList:
    def __init__(self, elements):
        if elements == []:
            self.head = None
            self.tail = None
            self.end = None
            self.size = 0 

        else:
            elements = list(elements)
            for idx, elem in enumerate(elements):
                if not isinstance(elem, LinkedNode):
                    elements[idx] = LinkedNode(idx, elem) 

            self.head = elements[0] 
            self.end = elements[-1]
            
            for idx, elem in enumerate(elements):
                if idx == len(elements)-1:
                    elem.next = None
                    break
                elem.next = elements[idx+1]
            
            self.tail = LinkedList(elements[1:])  
            self.size = len(elements)    


        


    def __iter__(self):
        cur = self.head 

        while cur is not None:
            yield cur.datum 
            cur = cur.next 

    def __str__(self):
        if self.head is None:
            return "LinkedList is empty"
        
        res = ''
        for elem in self:
            res += f'[{elem}] -->'
        res += 'None'
        return res 

    # def append(self,elem):
    #     if not isinstance(elem, LinkedNode):
    #         elem = LinkedNode(self.size, elem, next = None)

    #     self.end.next = elem
    #     self.end = elem
    #     self.size += 1
    #     self.tail = self.size - 1
    
    # def append_head(self,elem):
    #     if not isinstance(elem,LinkedNode):     
    #         elem = LinkedNode(self.size, elem, next = None)
        
    #     cur_head = self.head
    #     elem.next = cur_head
    #     self.tail.append_head(self.head)
    #     self.head = elem
    #     self.size += 1
        # append_head(self,elem) 원래 링크드리스트 self의 헤드 앞에 elem을 추가하는 함수
        # 지금 self.tail 의 헤드 앞에 self.head를 추가해야함 
        # 그러니까 append_head(self.tail, self.head) 하면 됨 
        # 그게 self.tail.append_head(self.head) 임 

    def append_head(self, elem):
        if LinkedList(elements = []):
            pass

        if not isinstance(elem, LinkedNode):
            elem = LinkedNode(self.size, elem)
        
        cur_head = self.head
        elem.next = cur_head
        self.head = elem
        self.size += 1
        
    def __len__(self):
        return self.size

    def pop_end(self):
        if self.size == 0:
            raise Exception("linkedlist is empty")
        
        #리스트 내 노드가 하나만 있는 경우
        elif self.size == 1:
            pop_node = self.head
            self.head = None
            self.end = None

        #마지막 요소 제거
        else:
            cur = self.head
            while cur.next != self.end:
                cur = cur.next
                
            pop_node = self.end
            self.end = cur
            self.end.next = None

        self.size -= 1
        return pop_node.datum   
        
    def last_number(self):
        if self.size == 0:
            raise Exception("linkedlist is empty")
        
        front = self.end.datum

        return front
        #return self.end.datum
    
class DoublyLinkedNode(Node):
    def __init__(self, node_id, datum, prev = None, next = None):
        self.node_id = node_id 
        self.datum = datum
        self.next = next 
        self.prev = prev 

class DoublyLinkedList:
    def __init__(self, elements):
        if elements == []:
            self.head = None 
            self.tail = None 
            self.end = None
            self.size = 0
        else:
            self.head = None 
            self.tail = None 
            self.end = None
            self.size = 0

    def __iter__(self):
        yield None 

    def __str__(self):
        res = ''

        return res 

if __name__ == "__main__":
    lst = LinkedList([1,2,3,4])

    # lst[0] == 1
    # # => LinkedList.__getitem__(lst,0)

    # for i in lst:
    #     pass
    # lst[1:3]


    # str(lst)
    # #=> LinkedList.__str__(lst)


    assert lst.head.datum == 1
    assert lst.head.next.datum == 2
    assert lst.head.next.next.datum == 3
    assert lst.head.next.next.next.datum == 4
    assert lst.head.next.next.next.next is None

    assert lst.head.next.next.next == lst.end
    print(True)