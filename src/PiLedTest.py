import time
from hal import hal_led as led
from hal import hal_input_switch as switch

LEFT = 1    # value the switch returns in the left position (swap if wrong)
RIGHT = 0

def main():
    led.init()
    switch.init()

    led_state = 0
    last_toggle = time.time()
    last_pos = None
    right_start = None

    while True:
        pos = switch.read_slide_switch()
        now = time.time()

        # Detect a change in switch position
        if pos != last_pos:
            last_pos = pos
            last_toggle = now
            right_start = now if pos == RIGHT else None

        if pos == LEFT:
            half_period = 0.1        # (b) 5 Hz
            blinking = True
        else:
            half_period = 0.05       # (c) 10 Hz
            # (d) only blink for 5 s after moving to the right
            blinking = (now - right_start) < 5
            # For (b)/(c) only, use: blinking = True  (for (b) alone: blinking = False)

        if blinking:
            if now - last_toggle >= half_period:
                led_state = 1 - led_state
                led.set_output(0, led_state)   # check argument order in hal_led.py
                last_toggle = now
        else:
            led_state = 0
            led.set_output(0, 0)

        time.sleep(0.005)   # tiny delay so the loop doesn't hog the CPU

if __name__ == "__main__":
    main()