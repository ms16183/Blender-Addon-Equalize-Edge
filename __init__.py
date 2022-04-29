import types
import math, mathutils
import bpy, bmesh

bl_info = {
    'name': 'Blender Addon Edge Equal Tool',
    'author': 'ms16183',
    'version': (1, 0),
    'blender': (3, 0, 0),
    'location': 'Mesh > Edge',
    'description': 'This tool equalizes all selected edges to the active edge length.',
    'warning': '',
    'support': 'TESTING',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Mesh'
}


class Equalize_OT_Edges(bpy.types.Operator):

    bl_idname = 'mesh.equalize_edges'
    bl_label = 'Equalize Edges'
    bl_description = 'Equalizes all selected edges to the active edge length.'
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        # get mesh as bmesh
        bm = bmesh.from_edit_mesh(context.object.data)

        # get active edge length
        active_edge = bm.select_history.active
        if not isinstance(active_edge, bmesh.types.BMEdge):
            return {'FINISHED'}
        active_edge_length = active_edge.calc_length()
        
        # resize selected edges
        # TODO: fix this process
        for edge in bm.edges:
            if edge.select:
                bmesh.ops.transform(
                    bm, 
                    matrix=mathutils.Matrix.Scale(active_edge_length / edge.calc_length(), 4),
                    space=mathutils.Matrix.Translation(-(edge.verts[0].co+edge.verts[1].co)/2),
                    verts=edge.verts)

        # update
        bmesh.update_edit_mesh(context.object.data)
        self.report({'INFO'}, f'Resized {active_edge_length:.3f}[m]')

        return {'FINISHED'}



def menu(self, context):
    self.layout.separator()
    self.layout.operator(Equalize_OT_Edges.bl_idname)


classes = [
    Equalize_OT_Edges,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(menu)
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
