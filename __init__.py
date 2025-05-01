import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Blender Memo",
    "author": "Ek1den2",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "保存時、初回起動時にポップ",
    "description": "作業内容を記録するアドオン。ログは保存したblendファイルと同じ場所にlog.jsonとして保存",
    "warning": "開発中",
    "support": "COMMUNIT"
    "Y",
    "category": "Interface"
}

from .operators import LoadOperator, SaveOperator

# 起動時の空読み込みを飛ばすため
@persistent
def load_handler(filepath):
    if filepath:
        bpy.ops.wm.load_log('INVOKE_DEFAULT', filepath=filepath)

def save_handler(dummy):
    bpy.ops.wm.save_log('INVOKE_DEFAULT')
    

def register():
    bpy.utils.register_class(LoadOperator)
    bpy.utils.register_class(SaveOperator)
    if load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_handler)
    if save_handler not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(save_handler)
    print("アドオンを開始")

def unregister():
    bpy.utils.unregister_class(SaveOperator)
    bpy.utils.unregister_class(LoadOperator)
    if save_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_handler)
    if load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    print("アドオンを終了")
