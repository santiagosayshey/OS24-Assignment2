from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)
        self.access_order = [] # initial access order list to store page access order

    def replace_page(self):
        return self.access_order.pop(0) # remove the least recently used page from the access order

    def update_access(self, page_number):
        # update the access order list
        self.access_order.remove(page_number) if page_number in self.access_order else None
        self.access_order.append(page_number)

    def handle_page_fault(self, page_number):
        super().handle_page_fault(page_number) 
        self.update_access(page_number) # update access order