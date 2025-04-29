import bpy

bl_info = {
    "name": "Blender Memo",
    "author": "Ek1den2",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "保存時、初回起動時にポップ",
    "description": "作業内容を記録するアドオン。ログは保存したblendファイルと同じ場所にwork_log.txtとして保存",
    "warning": "開発中",
    "support": "COMMUNITY",
    "category": "Interface"
}

from .operators import MemoOperator

def save_handler(dummy):
    bpy.ops.wm.save_log('INVOKE_DEFAULT')

def register():
    bpy.utils.register_class(MemoOperator)
    if save_handler not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(save_handler)
    print("アドオンを開始")

def unregister():
    bpy.utils.unregister_class(MemoOperator)
    if save_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_handler)
    print("アドオンを終了")
