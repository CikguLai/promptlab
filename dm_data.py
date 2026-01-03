# dm_data.py
# 核心数据加载器 (Data Loader)
# 负责整合所有语言包，避免单个文件过大

import dm_data_part1 as p1  # 英、中、马 (核心)
import dm_data_part2 as p2  # 亚洲语言
import dm_data_part3 as p3  # 欧美语言

# 汇总所有语言的 FAQ 数据库
FAQ_DATABASE = {}
FAQ_DATABASE.update(p1.FAQ_DATA)
FAQ_DATABASE.update(p2.FAQ_DATA)
FAQ_DATABASE.update(p3.FAQ_DATA)

# 汇总所有语言的表格数据
TABLE_DB = {}
TABLE_DB.update(p1.TABLE_DATA)
TABLE_DB.update(p2.TABLE_DATA)
TABLE_DB.update(p3.TABLE_DATA)

# 汇总所有语言的工单类型
TICKET_OPTIONS = {}
TICKET_OPTIONS.update(p1.TICKET_DATA)
TICKET_OPTIONS.update(p2.TICKET_DATA)
TICKET_OPTIONS.update(p3.TICKET_DATA)

# 获取语言列表
ALL_LANGUAGES = list(FAQ_DATABASE.keys())

# 辅助函数
def get_ticket_types(lang): 
    return TICKET_OPTIONS.get(lang, TICKET_OPTIONS["English"])

def get_table_data(lang, ui_module):
    ui = ui_module.get_safe_ui(lang)
    data = TABLE_DB.get(lang, TABLE_DB.get("English"))
    rows = [{"k": data["keys"][i], "v1": data["guest"][i], "v2": data["pro"][i]} for i in range(len(data["keys"]))]
    return ui["tbl_head"], rows
