bl_info = {
    "name": "come back cursor",
    "author": "1C0D",
    "version": (1, 1, 1),
    "blender": (2, 90, 0),
    "location": "Text Editor > only > Text editor",
    "description": "stay home cursor",
    "wiki_url": "",
    "category": "Text Editor",
}

"""
Use shortcut shift+Right Mouse to toggle the operator. the icon in the header is more like an indicator. don't activate more than 2 limits by default down and right are True (see in addon preferences). if you need other corners uncomment lines

"""

import bpy

class COME_back_cursor(bpy.types.Operator):
    """Get back cursor in the right place"""
    bl_idname = "text.come_back"
    bl_label = "come back cursor"

    def modal(self, context, event):

        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        region=context.region

        if context.area.type=='TEXT_EDITOR':
            if addon_prefs.y_min and event.mouse_region_y <= 10:    #bottom
                context.window.cursor_warp(event.mouse_x,region.y+event.mouse_region_y+1)

            if addon_prefs.y_max and event.mouse_region_y >= (region.height-10):   #top 
                context.window.cursor_warp(event.mouse_x,region.y+event.mouse_region_y-1)

            if addon_prefs.x_min and event.mouse_region_x <= 30:  
                context.window.cursor_warp(region.x+event.mouse_x+1,event.mouse_y)

            if addon_prefs.x_max and event.mouse_region_x >= context.area.width-1:  #if side panel 
                context.window.cursor_warp(region.x+event.mouse_x-1,event.mouse_y) 

        if event.type == 'ESC' or not context.scene.toggle_cbc:
            context.scene.toggle_cbc = False
            return {'FINISHED'}

        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    @classmethod
    def _setup(cls):
        cls._keymaps = []
        kc = bpy.context.window_manager.keyconfigs.addon.keymaps
        get, new = kc.get, kc.new
        km = get('Text', new(name='Text', space_type='TEXT_EDITOR'))

        new = km.keymap_items.new
        wm = bpy.context.window_manager
        kmi = new("wm.context_toggle", 'RIGHTMOUSE', 'PRESS', shift=1)
        kmi.properties.data_path = "scene.toggle_cbc"
        cls._keymaps.append((km, kmi))

    @classmethod
    def _remove(cls):
        for km, kmi in cls._keymaps:
            km.keymap_items.remove(kmi)
        cls._keymaps.clear()
    
class COME_PT_back_cursor(bpy.types.AddonPreferences):
    bl_idname = __name__

    y_min: bpy.props.BoolProperty(
            name="enable y min",
            default=True,
            )
    y_max: bpy.props.BoolProperty(
            name="enable y max",
            default=False,
            )            
    x_min: bpy.props.BoolProperty(
            name="enable x min",
            default=False,
            )
    x_max: bpy.props.BoolProperty(
            name="enable x max",
            default=True,
            )
            
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "y_min")
        layout.prop(self, "y_max")
        layout.prop(self, "x_min")
        layout.prop(self, "x_max")   
        

def update_toggle_cbc(self, context):
    
    print("state0", context.scene.toggle_cbc)
    if context.scene.toggle_cbc: 
        bpy.ops.text.come_back('INVOKE_DEFAULT')        
        print("state1", context.scene.toggle_cbc)

def draw(self, context):
    
    layout = self.layout    
    layout.prop(context.scene, "toggle_cbc",text='', icon="VIS_SEL_11", toggle=False)

def register():
    bpy.utils.register_class(COME_back_cursor)
    COME_back_cursor._setup()   
    bpy.utils.register_class(COME_PT_back_cursor)
    bpy.types.TEXT_HT_header.prepend(draw)
    bpy.types.Scene.toggle_cbc = bpy.props.BoolProperty(update=update_toggle_cbc,default=False)

def unregister():
    bpy.types.TEXT_HT_header.remove(draw)
    bpy.utils.unregister_class(COME_PT_back_cursor)
    bpy.utils.unregister_class(COME_back_cursor)
    COME_back_cursor._remove()
    del bpy.types.Scene.toggle_cbc

if __name__ == "__main__":
    register()
