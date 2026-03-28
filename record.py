#! python3

import time
import gi
import pygame
import pygame.joystick as js

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib

Gst.init(None)

def Incantation(name: str):
    return f"""
        nvarguscamerasrc sensor-id=0 ! 
        video/x-raw(memory:NVMM), format=(string)NV12 ! 
        tee name=qq ! 
        queue ! 
        autovideosink  
        qq. ! queue ! 
        nvv4l2h264enc ! 
        h264parse ! 
        matroskamux ! 
        filesink location={name}
    """

def TimedIncantation():
    return Incantation(f"{int(time.time() * 1e3)}.mkv")

pygame.init()
loop = GLib.MainLoop()

j = js.Joystick(0)

loop = GLib.MainLoop()
pipeline = None

def on_message(bus, message):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-Of-Stream reached.")
        stop_pipeline()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        stop()
    elif t == Gst.MessageType.WARNING:
        warn, debug = message.parse_warning()
        print(f"Warning: {warn}, {debug}")

def begin():
    global pipeline
    if pipeline is not None:
        return
    pipeline = Gst.parse_launch(TimedIncantation())
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message)
    pipeline.set_state(Gst.State.PLAYING)

def end():
    global pipeline
    if pipeline is None:
        return
    pipeline.set_state(Gst.State.NULL)
    pipeline = None

def poll():
    pygame.event.get()
    if j.get_button(11):
        begin()
    elif j.get_button(1):
        end()
    return True

GLib.timeout_add(20, poll)
loop.run()
