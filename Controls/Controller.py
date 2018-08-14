from direct.task import Task

class X360():
    def __init__(self, ControlManager,Controller):
        self.CM = ControlManager
        self.Controller = Controller
        self.Controller._last_state = self.Controller.get_state()
        self.KeyBindings()
            
        def CheckController(task):
            state = self.Controller.get_state()
            if not state:
                # Start searching again for the controller!
                self.CM.SearchForControllers()
                return task.done
            if state.packet_number != self.Controller._last_state.packet_number:
                self.Controller.handle_changed_state(state)
            self.Controller._last_state = state
            return task.cont

        taskMgr.add(CheckController)

    def KeyBindings(self):
        # Bind the X360 controller buttons to game scripts
        @self.Controller.event
        def on_axis(axis, value):
            if axis=="l_thumb_x": # Left stick, horizontal direction
                self.CM.Steer(min(1.,value*-2)) # Axis values range from [-0.5, 0.5]

        @self.Controller.event
        def on_button(button, pressed):
            if button == 13: # A button
                self.CM.Throttle(pressed)
            elif button ==14: # B button
                self.CM.Brake(pressed)

class SteamController(X360):
    def KeyBindings(self):
        # TODO: Find the key bindings for the Steam Controller
        pass