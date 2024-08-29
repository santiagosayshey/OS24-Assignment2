import random
from mmu import MMU

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}
        self.debug_mode = False
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")
        else:
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if len(self.page_table) < self.frames:
                self.page_table[page_number] = False  # dirty_bit
                if self.debug_mode:
                    print(f"Page {page_number} loaded into memory")
            else:
                self._replace_page(page_number)

    def write_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")
            self.page_table[page_number] = True  # Set dirty bit
        else:
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if len(self.page_table) < self.frames:
                self.page_table[page_number] = True  # dirty_bit
                if self.debug_mode:
                    print(f"Page {page_number} loaded into memory")
            else:
                self._replace_page(page_number)
                self.page_table[page_number] = True  # Set dirty bit

    def _replace_page(self, page_number):
        victim_page = random.choice(list(self.page_table.keys()))
        if self.page_table[victim_page]:
            self.total_disk_writes += 1
            if self.debug_mode:
                print(f"Page {victim_page} written back to disk")
        del self.page_table[victim_page]
        self.page_table[page_number] = False  # dirty_bit
        if self.debug_mode:
            print(f"Page {page_number} loaded into memory (replacing page {victim_page})")

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults