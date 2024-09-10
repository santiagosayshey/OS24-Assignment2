from mmu import MMU
import random

class RandMMU(MMU):
    def replace_page(self):
        # randomly select a page to replace
        return random.choice(self.memory)

    def update_access(self, page_number):
        # random replacement doesn't need to track access
        pass