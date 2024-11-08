import obsws_python as obs_ws
import obspython as obs
#Shutil is used so files can be moved across disks if required
import shutil
import os

# load conn info from config.toml
cl = obs_ws.EventClient()

# Description displayed in the Scripts dialog window
def script_description():
    return """Output file mover
            This is a simple OBS script that utilizes websockets to move a file when a recording has ended."""


# Settings
output_path = None

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "output_path", "Output Path", obs.OBS_PATH_DIRECTORY, '', None)
    return props

def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "output_path", "")

def script_update(settings):
    global output_path
    output_path = obs.obs_data_get_string(settings, "output_path")

# Events
def on_record_state_changed(data):
    # Recording finished event and output path is defined
    if data.output_state == 'OBS_WEBSOCKET_OUTPUT_STOPPED' and output_path:
        # File name for the saved recording, if record stopped. null otherwise
        file = data.output_path
        if file:
            file_name = os.path.basename(file)
            shutil.move(file, output_path + "/" + file_name)

cl.callback.register(on_record_state_changed)