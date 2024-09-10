from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)
        self.clock_hand = 0 # initialise clock hand to 0 as a pointer to the current page
        self.use_bits = {}  # initialise use bits dictionary to store page number and use bit

    def replace_page(self):
        while True: # loop until a page is chosen
            current_page = self.memory[self.clock_hand]
            if self.use_bits[current_page]: 
                # page has been used, give it a second chance
                self.use_bits[current_page] = False
                self.clock_hand = (self.clock_hand + 1) % len(self.memory) # move the clock hand to the next page
            else:
                # page hasn't been used, choose it for replacement
                self.clock_hand = (self.clock_hand + 1) % len(self.memory) 
                return current_page

    def update_access(self, page_number):
        self.use_bits[page_number] = True # set use bit to true

    def handle_page_fault(self, page_number):
        if len(self.memory) < self.frames:
            # add page to memory
            self.memory.append(page_number)
            self.page_table[page_number] = False  # set use bit to false
            self.use_bits[page_number] = True  # set use bit
        else:
            # memory is full, replace a page
            victim_page = self.replace_page()
            self.remove_page(victim_page) # remove page from memory
            self.memory[self.clock_hand - 1] = page_number
            self.page_table[page_number] = False  # set use bit to false
            self.use_bits[page_number] = True  # set use bit

        self.disk_reads += 1
        self.page_faults += 1

    def remove_page(self, page_number):
        if self.page_table[page_number]:  # If dirty
            self.disk_writes += 1                
        del self.page_table[page_number]
        del self.use_bits[page_number]

    def read_memory(self, page_number):
        self.handle_page_fault(page_number) if page_number not in self.page_table else self.update_access(page_number)

    def write_memory(self, page_number):
        self.handle_page_fault(page_number) if page_number not in self.page_table else None
        self.page_table[page_number] = True  # mark as dirty
        self.update_access(page_number)
            