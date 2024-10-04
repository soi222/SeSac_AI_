try:
    from node import Node 
except ModuleNotFoundError:
    from data_structure.node import Node

class TreeNode:
    def __init__(self, node_id, datum):
        self.node_id = node_id
        self.datum = datum 

class Tree:
    def __init__(self, root, children = []):
        if not isinstance(root, TreeNode):
            root = TreeNode(0,root)

        self.root = root
        self.children = list(children)
        
        for i, e in enumerate(self.children):
            if not isinstance(e, Tree):
                children[i] = Tree(TreeNode(i, e))
        
            
    def iter_nodes(self):
        yield self.root.datum

        for child in self.children:
            yield from child.iter_nodes()
        

    #노드와 노드의 주소를 함께 반환
    def iter_nodes_with_address(self):
        yield [], self.root

        for idx, child in enumerate(self.children):
            for x in child.iter_nodes_with_address():
                #iter_nodes_with_address는 튜플리턴
                #daar는 주소, n은 노드값
                addr, n = x 
                yield [idx] + addr, n  

        """
        address = []
        
        if len(self.children) == 0:
            yield tuple(address, self.root.datum)

        else:
            for i in range(len(self.children)-1):
                address.append(i)

            print(address)
            for idx, child in enumerate(self.children):
                for x in child.iter_nodes_with_address(address + [idx]):
                    yield [idx] + address, x
        """

       

    # def iter_nodes_with_address(self, address = []):

    #     yield address, self.root 

    #     for idx, child in enumerate(self.children):
    #         for x in child.iter_nodes_with_address([idx]):
    #             yield x 

    # def __iter__(self):
    #     for node in self.iter_nodes():
    #         yield node

    def insert(self, address, elem):
        address_lst = []
        for addr, node in self.iter_nodes_with_address():
            
            ad1 = addr[0]
            ad2 = addr[1]
            
            for x in address:
                x1, x2 = x
                if x1 == ad1:
                    if x2 == ad2:
                        address_lst.insert(x1,elem)
                    elif x2 < ad2:
                        address_lst.insert((x1 + 1),elem)
                    else:
                        address_lst.insert((x1-1),elem)

                elif x1 > ad1:
                    address_lst.append((x1-1),elem)
                else:
                    address_lst.append((x1+1),elem)
            
                
                
                

    def delete(self, address):
        pass
        
    def search(self, elem):
        if elem == self.root.datum:
            return []

        else:
            for idx, child in enumerate(self.children):
                for x in child.iter_nodes_with_address():
                    addr, n = x
                    if elem == n.datum:
                        return [idx] + addr
                    

        # for addr, node in self.iter_nodes_with_address():
        #     if node.datum == elem:
        #         return addr 

    #yield와 동일
    def return_search(self, elem):
        res = []
        if elem == self.root.datum:
            # yield []
            res.append([])

        else:
            for idx, child in enumerate(self.children):
                for x in child.iter_nodes_with_address():
                    addr, n = x
                    if  elem == n.datum:
                        # yield [idx] + addr
                        res.append([idx] + addr)
                    else:
                        print("Search Error")
        return res 
    
    def root_datum(self):
        root_value = self.root.datum   
        return root_value

    def height(self): #tab의 갯수로는 구하기 어려울까?
        if len(self.children) == 0:
            return 0
        
        else:
            address_lst = []
            for idx, child in enumerate(self.children):
                for x in child.iter_nodes_with_address():
                    addr, n = x
                    y = [idx] + addr
                    address_lst.append(y) 

            select = max(address_lst, key= len)
            length = len(select) + 1
            return length
                
            """address_lst = []
            address = []

            for i in range(len(self.children)-1):
                address.append(i)

            for idx, child in enumerate(self.children):
                for x in child.iter_nodes_with_address(address + [idx]):
                    y = [idx] + address 
                    yield y
                    address_lst.append(y)
    
            length = max(address_lst, key = len)
            length = len(length)
            return length"""

        
    def __str__(self):
        # only tab version 
        res = [str(self.root.datum)]
        t = '   '
        n = '\n'
        nt = n + t
        al =  '└──'
        bl = '├──'     
        nt_bar = n + "│   "

        l = len(self.children)
        
        for idx, child in enumerate(self.children):
            if idx == l - 1:
                res.append(al + str(child).replace(n, nt))
            else:
                res.append(bl + str(child).replace(n, nt_bar))

        return n.join(res)
        
        '''
        #tab으로 출력하는 방법
        res = [str(self.root.datum)]

        for idx, child in enumerate(self.children):
            res.append(t + str(child).replace(n, nt))

        return n.join(res)'''
    
    """
    #tab모형으로 출력하기

    def s(t):
        res = [str(t.root)]
        for child in children:
            part = child.s()

        for line in part:
            res.append(tab + line)

        return res
    """
    

if __name__ == '__main__':
    t1 = Tree(1, [
                Tree(11, [Tree(111), Tree(112)],), 
                Tree(12, [Tree(121), Tree(122), Tree(123),])
             ]
         )
    print(t1)
    for addr, n in t1.iter_nodes_with_address():
        print(addr, n.datum)

    assert t1.root_datum() == 1 
    assert t1.height() == 3
    
    for res in t1.search(111):
        print('search ~ ', res)

    for addr, n in t1.iter_nodes_with_address():
        assert [int(e)-1 for e in list(str(n.datum))[1:]] == addr 
        search_result = t1.search(n.datum)

        assert search_result == addr, search_result

    t1.insert([2], Tree(13, [Tree(131), Tree(132), Tree(133)]))
    t1.insert([1, 1], Tree(122, [Tree(1221), Tree(1222)]))

    # print(t1)
    
    # assert 122 == t1.delete([1,2])
    # assert 123 == t1.delete([1,2])

    # for addr, n in t1.iter_nodes_with_address():
    #     assert [int(e)-1 for e in list(str(n.datum))[1:]] == addr 
    #     assert t1.search(n.datum) == addr 

    # print(t1)
