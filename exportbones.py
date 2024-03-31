bl_info = {
    "name": "Export Armature Animation",
    "author": "YuSa64",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > YuSa64",
    "description": "Import and export FBX files with armature animation.",
    "category": "Import-Export",
}

import bpy
import os

class YuSa64Panel(bpy.types.Panel):
    bl_label = "Export Amrature Animation"
    bl_idname = "PT_YuSa64Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'YuSa64'

    def draw(self, context):
        layout = self.layout
        layout.operator("yusa64.importexport", text="Import/Export FBX")

class YuSa64ImportExportOperator(bpy.types.Operator):
    bl_idname = "yusa64.importexport"
    bl_label = "Choose Directory"

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        base_dir = self.directory
        converted_base_dir = os.path.join(base_dir, "converted")
        os.makedirs(converted_base_dir, exist_ok=True)
        for root, dirs, files in os.walk(base_dir):
            if root.startswith(converted_base_dir):
                continue  # don't visit "converted" directories
            for file in files:
                if file.endswith(".fbx"):
                    filepath = os.path.join(root, file)
                    bpy.ops.import_scene.fbx(filepath=filepath)
                    for obj in bpy.context.selected_objects:
                        if obj.type == 'ARMATURE':
                            bpy.ops.object.mode_set(mode='POSE')
                            bpy.ops.pose.select_all(action='SELECT')
                            # Unlink the meshes
                            for child in obj.children:
                                if child.type == 'MESH':
                                    bpy.context.collection.objects.unlink(child)
                            # Create the same subfolder structure in the "converted" directory
                            relative_dir = os.path.relpath(root, base_dir)
                            converted_dir = os.path.join(converted_base_dir, relative_dir)
                            os.makedirs(converted_dir, exist_ok=True)
                            bpy.ops.export_scene.fbx(filepath=os.path.join(converted_dir, file), use_selection=True)
                            bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.delete()
                    bpy.ops.outliner.orphans_purge()  # clean up unused data
        return {'FINISHED'}




    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(YuSa64Panel)
    bpy.utils.register_class(YuSa64ImportExportOperator)

def unregister():
    bpy.utils.unregister_class(YuSa64Panel)
    bpy.utils.unregister_class(YuSa64ImportExportOperator)

if __name__ == "__main__":
    register()
