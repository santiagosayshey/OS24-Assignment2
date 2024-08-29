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

    def _access_memory(self, page_number, is_write):
        if page_number not in self.page_table:
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if len(self.page_table) < self.frames:
                self.page_table[page_number] = [True, is_write]
                self.clock_hand = (self.clock_hand + 1) % self.frames
                if self.debug_mode:
                    print(f"Page {page_number} loaded into memory")
            else:
                self._replace_page(page_number, is_write)
        else:
            if is_write:
                self.page_table[page_number][1] = True
            self.page_table[page_number][0] = True
            if self.debug_mode:
                print(f"Page {page_number} is already in memory")

    def read_memory(self, page_number):
        self._access_memory(page_number, False)

    def write_memory(self, page_number):
        self._access_memory(page_number, True)

    def _replace_page(self, page_number, is_write):
        while True:
            self.clock_hand = (self.clock_hand + 1) % self.frames
            current_page = list(self.page_table.keys())[self.clock_hand]
            if not self.page_table[current_page][0]:
                if self.page_table[current_page][1]:
                    self.total_disk_writes += 1
                    if self.debug_mode:
                        print(f"Page {current_page} written back to disk")
                del self.page_table[current_page]
                self.page_table[page_number] = [True, is_write]
                if self.debug_mode:
                    print(f"Page {page_number} loaded into memory (replacing page {current_page})")
                break
            else:
                self.page_table[current_page][0] = False

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults