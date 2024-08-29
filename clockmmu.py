from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}
        self.clock_hand = 0
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
            self.page_table[page_number][0] = True  # Set reference bit
        else:
            self._handle_page_fault(page_number)

    def write_memory(self, page_number):
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")
            self.page_table[page_number] = [True, True]  # Set reference and dirty bits
        else:
            self._handle_page_fault(page_number)
            self.page_table[page_number][1] = True  # Set dirty bit

    def _handle_page_fault(self, page_number):
        self.total_page_faults += 1
        self.total_disk_reads += 1
        if len(self.page_table) < self.frames:
            self.page_table[page_number] = [True, False]  # [reference_bit, dirty_bit]
            if self.debug_mode:
                print(f"Page {page_number} loaded into memory")
        else:
            self._replace_page(page_number)

    def _replace_page(self, page_number):
        while True:
            current_page = list(self.page_table.keys())[self.clock_hand]
            if not self.page_table[current_page][0]:
                if self.page_table[current_page][1]:
                    self.total_disk_writes += 1
                    if self.debug_mode:
                        print(f"Page {current_page} written back to disk")
                del self.page_table[current_page]
                self.page_table[page_number] = [True, False]  # [reference_bit, dirty_bit]
                if self.debug_mode:
                    print(f"Page {page_number} loaded into memory (replacing page {current_page})")
                self.clock_hand = (self.clock_hand + 1) % self.frames
                break
            else:
                self.page_table[current_page][0] = False  # Reset reference bit
            self.clock_hand = (self.clock_hand + 1) % self.frames

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults