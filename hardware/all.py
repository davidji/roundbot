
import arduino, swdconnector, usb_battery_replacer_box, chassis

if __name__ == '__main__':
    arduino.export_scad()
    swdconnector.export_scad()
    usb_battery_replacer_box.export_scad()
    chassis.export_scad()
