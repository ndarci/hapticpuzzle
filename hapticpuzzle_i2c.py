import time
import busio

class Peripheral():
    '''parent class to peripheral i2c objects. children can implement hardware-specific functionality'''
    def __init__(self, bus, address):
        # bus is the i2c connection - must be the same object across all peripherals
        self.bus = bus
        # address is the i2c device address
        self.address = address

    def bignumber_to_bytelist(self, number):
        '''convert a hex number > 255 to a list of bytes'''
        hexstr = hex(number)[2:]
        if len(hexstr) % 2 != 0:
            hexstr = '0' + hexstr
        list_of_bytes = []
        for i in range(0, len(hexstr), 2):
            list_of_bytes.append(int(hexstr[i:(i+2)], 16))
        # print([hex(x) for x in list_of_bytes])
        return list_of_bytes

class Slider(Peripheral):
    '''made for adafruit neoslider'''
    def __init__(self, bus, address=0x30, register=[0x09, 0x07 + 18]):
        Peripheral.__init__(self, bus, address)
        # register is the base ADC address inside the neoslider chip
        self.register = register

    def read_potentiometer(self, num_bytes, register = None, delay = 0.008):
        '''read the potentiometer from the adafruit neoslider. outputs an int 0-1023'''
        if register is None:
            register = self.register
        buffer = bytearray(num_bytes)
        # lock the bus
        while self.bus.try_lock() == False:
            pass
        try:
            # tell device which register we're about to read from
            time.sleep(delay)
            self.bus.writeto(self.address, bytes(register))
        except Exception as e:
            print("write error:", e)
        try:
            # read from defined register and store in buffer
            time.sleep(delay)
            self.bus.readfrom_into(self.address, buffer)
        except Exception as e:
            print("read error:", e)
        
        # unlock the bus
        self.bus.unlock()
        # mask to 10 bits and convert to int
        output = int.from_bytes(buffer) & 1023
        return output

class LEDStick(Peripheral):
    '''made for sparkfun qwiic apa102c'''
    def __init__(self, bus, address=0x23):
        Peripheral.__init__(self, bus, address)
        self.current_led = -1 # eventually this should be a dictionary for all LEDs currently on ... {index: [r, g, b]}

    def __write_to_leds(self, register, byte_list, delay = 0.008):
        '''private fx. writes a message to the LED stick at the given register, depending on the desired command'''
        # lock the bus
        while self.bus.try_lock() == False:
            pass
        try:
            # tell device which register we're about to read from
            # append the message we want to send after the register information
            time.sleep(delay)
            self.bus.writeto(self.address, bytes(register + byte_list))
        except Exception as e:
            print("write error:", e)
        # unlock the bus
        self.bus.unlock()

    def __clean_color(self, color):
        # crop too high/too low color values
        for i in range(len(color)):
            if color[i] > 255:
                color[i] = 255
            elif color[i] < 0:
                color[i] = 0
        return color

    def set_all_leds(self, color):
        '''writes a single color to all 10 LEDs'''
        color = self.__clean_color(color)
        self.__write_to_leds([0x72], color)

    def __set_one_led(self, index, color):
        '''writes a single color to one specified LED'''
        color = self.__clean_color(color)
        self.__write_to_leds([0x71], [index] + color)

    def __clean_index(self, index):
        '''crops out of range LED indices'''
        if index > 9:
            index = 9
        elif index < 0:
            index = 0
        return index

    def change_led(self, newindex, newcolor):
        '''updates lit LED to the new index and color, if it differs from the old index'''
        newindex = self.__clean_index(9-newindex)
        newcolor = self.__clean_color(newcolor)
        if newindex != self.current_led:
            if self.current_led > -1:
                self.__set_one_led(self.current_led, [0x00, 0x00, 0x00])
            self.__set_one_led(newindex, newcolor)
            self.current_led = newindex
    
    def off(self):
        '''turns off all the LEDs'''
        self.set_all_leds([0x00, 0x00, 0x00])
        self.current_led = -1
