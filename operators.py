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
            "date": now,
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
    bl_label = "前回の作業"
    bl_description = "保存した作業内容を表示する"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty() # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=350)

    def draw(self, context):
        filename = os.path.basename(self.filepath)
        print("ファイル名", filename)
        log_path = os.path.dirname(self.filepath) + "/log.json"
        print("ログパス", log_path)
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)[filename]
            self.report({'INFO'}, "ログを読み込みました")
        except Exception as e:
            self.report({'ERROR'}, f"ログが読み込めませんでした: {e}")
        
        latest_memo = max(
            (memo for memo in json_data),
            key=lambda m: datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
        )

        dt = datetime.strptime(latest_memo['date'], "%Y-%m-%d %H:%M")
        timedate = get_relative_time(dt)
        print("時間:", latest_memo['date'])

        layout = self.layout
        layout.label(text = timedate)
        layout.label(text = latest_memo['memo'])
    
    def execute(self, context):
        return {'FINISHED'}


def get_relative_time(post_time: datetime):
    now = datetime.now()
    delta = now - post_time

    seconds = delta.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = delta.days

    if seconds < 60:
        return "たった今"
    elif minutes < 60:
        return f"{int(minutes)}分前"
    elif hours < 24:
        return f"{int(hours)}時間前"
    elif days < 7:
        return f"{int(days)}日前"
    elif days < 30:
        weeks = days // 7
        return f"{int(weeks)}週間前"
    elif days < 365:
        month = days // 30.5
        return f"{int(month)}ヶ月前"
    else:
        return post_time.strftime("%Y年%m月")