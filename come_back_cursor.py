bl_info = {
    "name": "come back cursor",
    "author": "1C0D",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "Text Editor > only > Text editor",
    "description": "stay home cursor",
    "wiki_url": "",
    "category": "Text Editor",
}

"""
Assign a shortcut from the search menu. stop with alt (or esc). if you need other corners uncomment lines

this is not hyper sensitive but if you let the mouse not far from the border it will automatically get back in. 
"""

#to improve: if in stop calculation

import bpy

try:
    import pyautogui
except ImportError:
    pybin = bpy.app.binary_path_python
    subprocess.check_call([pybin, '-m', 'pip', 'install', 'pyautogui']) #win
    import pycodestyle

class COME_back_cursor(bpy.types.Operator):
    """Get back cursor in the right place"""
    bl_idname = "text.come_back"
    bl_label = "come back cursor"

    def modal(self, context, event):

        def get_3d_area_region():
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'TEXT_EDITOR':
                        return area

        area = get_3d_area_region()       
        if event.mouse_region_y <= 5:    #bottom
            pyautogui.moveRel(0, -8)  # 8 pixels up
#        if event.mouse_region_y >= area.height+15:   #top 
#            pyautogui.moveRel(0, 8)  # 8 pixels down            
#        if event.mouse_region_x <= 5:  
#            pyautogui.moveRel(8, 0)  # 8 pix right
        if event.mouse_region_x >= area.width-5:   
            pyautogui.moveRel(-8, 0)  # 8 pix left
        
        if event.type == 'ESC' or event.alt:
            return {'FINISHED'}
        
        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def draw(self, context):
    layout = self.layout
    
    layout.operator("text.come_back",text='', icon="VIS_SEL_11")


def register():
    bpy.utils.register_class(COME_back_cursor)
    bpy.types.TEXT_HT_header.prepend(draw)


def unregister():
    bpy.utils.unregister_class(COME_back_cursor)
    bpy.types.TEXT_HT_header.remove(draw)


if __name__ == "__main__":
    register()

#    # test call
#    bpy.ops.object.modal_operator('INVOKE_DEFAULT')