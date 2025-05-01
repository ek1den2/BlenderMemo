import bpy
import os
import json
from datetime import datetime

class SaveOperator(bpy.types.Operator):
    bl_idname = "wm.save_log"
    bl_label = "作業メモの保存"
    bl_description = "作業内容をログに記録して保存する"
    bl_options = {'REGISTER'} 

    user_text: bpy.props.StringProperty(name="Memo") # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=350)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "user_text")

    def execute(self, context):
        filepath = bpy.data.filepath
        filename = os.path.basename(filepath)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        log = {
            "data": now,
            "memo": self.user_text
        }

        log_path = os.path.dirname(filepath) + "/log.json"

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        
        if filename not in data:
            data[filename] = []

        data[filename].append(log)

        try:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.report({'INFO'}, "ログを保存しました")
        except Exception as e:
            self.report({'ERROR'}, f"ログが保存できませんでした: {e}")
        
        return {'FINISHED'}
    

class LoadOperator(bpy.types.Operator):
    bl_idname = "wm.load_log"
    bl_label = "作業メモを表示"
    bl_description = "保存した作業内容を表示する"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty() # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        log_path = os.path.dirname(self.filepath) + "/log.json"
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                for text in f:
                    print(text.strip())
            self.report({'INFO'}, "ログを読み込みました")
        except Exception as e:
            self.report({'ERROR'}, f"ログが読み込めませんでした: {e}")

        layout = self.layout
        layout.label(text = text)
    
    def execute(self, context):
        return {'FINISHED'}
    