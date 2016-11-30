#include <unistd.h>
#include <mraa/gpio.h>
#include <stdlib.h>
#include <time.h>

// Handler for GPIO interrupt.
void do_on_button_press()
{
	system("/home/root/EE180DA-B/detect.sh");
}

int main()
{
	mraa_gpio_context button;
	button = mraa_gpio_init(4);
	mraa_gpio_dir(button, MRAA_GPIO_IN);

	// Set an interrupt on the pin for button.
	mraa_gpio_isr(button, MRAA_GPIO_EDGE_RISING, &do_on_button_press, NULL);

	while(1) {
		sleep(1);
	}	
}
