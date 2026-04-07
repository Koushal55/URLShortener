import time
import threading

class SnowflakeGenerator:
    def __init__(self, machine_id, epoch=1704067200000): # Epoch: Jan 1, 2024
        self.machine_id = machine_id
        self.epoch = epoch
        
        # Bit lengths
        self.machine_id_bits = 10
        self.sequence_bits = 12
        
        # Max values
        self.max_machine_id = -1 ^ (-1 << self.machine_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)
        
        if machine_id > self.max_machine_id:
            raise ValueError(f"Machine ID exceeds {self.max_machine_id}")

        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_ms(self):
        return int(time.time() * 1000)

    def generate_id(self):
        with self.lock:
            timestamp = self._current_ms()

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards!")

            if timestamp == self.last_timestamp:
                # Same millisecond, increment sequence
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    # Sequence exhausted, wait for next millisecond
                    while timestamp <= self.last_timestamp:
                        timestamp = self._current_ms()
            else:
                # New millisecond, reset sequence
                self.sequence = 0

            self.last_timestamp = timestamp

            # Bit shifting to create the 64-bit ID
            new_id = ((timestamp - self.epoch) << (self.machine_id_bits + self.sequence_bits)) | \
                     (self.machine_id << self.sequence_bits) | \
                     self.sequence
            return new_id

# Local Test
if __name__ == "__main__":
    generator = SnowflakeGenerator(machine_id=1)
    for _ in range(5):
        print(f"Generated ID: {generator.generate_id()}")