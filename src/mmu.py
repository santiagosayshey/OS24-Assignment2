class MMU:
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}  # Maps page numbers to frame numbers
        self.memory = []  # List of page numbers in memory
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        self.handle_page_fault(page_number) if page_number not in self.page_table else self.update_access(page_number)
            

    def write_memory(self, page_number):
        self.handle_page_fault(page_number) if page_number not in self.page_table else None
        self.page_table[page_number] = True  # mark as dirty
        self.update_access(page_number)

    def handle_page_fault(self, page_number):
        self.page_faults += 1
        if len(self.memory) >= self.frames:
            victim_page = self.replace_page()
            self.remove_page(victim_page)
        
        self.memory.append(page_number)
        self.page_table[page_number] = False  # Not dirty initially
        self.disk_reads += 1            

    def remove_page(self, page_number):
        if self.page_table[page_number]:  # If dirty
            self.disk_writes += 1
        
        self.memory.remove(page_number)
        del self.page_table[page_number]

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults

    def replace_page(self):
        pass

    def update_access(self, page_number):
        pass