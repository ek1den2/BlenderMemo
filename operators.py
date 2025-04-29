import bpy
import os
from datetime import datetime

class MemoOperator(bpy.types.Operator):
    bl_idname = "wm.save_log"
    bl_label = "作業メモ"
    bl_description = "作業内容をログに記録して保存する"
    bl_options = {'REGISTER'} 

    user_text: bpy.props.StringProperty(name="Memo") # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "user_text")

    def execute(self, context):
        filepath = bpy.data.filepath
        filename = os.path.basename(filepath)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        log_lines = [
            f"[{now}]",
            f"ファイル名: {filename}",
            f"{self.user_text}",
        ]
        log_text = "\n".join(log_lines)
        print(os.path.dirname(filepath))

        log_path = os.path.dirname(filepath) + "/log.txt"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("\n" + log_text + "\n")
            self.report({'INFO'}, "ログを保存しました")
        except Exception as e:
            self.report({'ERROR'}, f"ログが保存できませんでした: {e}")
        
        return {'FINISHED'}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=350)
