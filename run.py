import streamlit as st
import pandas as pd
import re
import time
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from io import BytesIO
import hashlib
import platform
import socket
import uuid
import subprocess
import os
import sqlite3
import json

# ====================== 中英文语言配置 ======================
TRANSLATIONS = {
    "zh": {
        "page_title": "关键词挖掘神器",
        "activation_title": "🔐 软件激活",
        "machine_code_label": "您的机器码",
        "activation_code_label": "请输入激活码",
        "activation_code_placeholder": "请输入24位激活码",
        "activate_button": "✅ 激活软件",
        "activation_success": "🎉 激活成功！正在进入软件...",
        "activation_error": "❌ 激活码无效，请联系客服获取",
        "activation_hint": "提示：请将机器码发送给客服获取激活码",
        "main_title": "🏢 关键词挖掘神器",
        "subtitle_line1": '<span class="highlight-text">行业专用版</span> · 精准挖掘真实用户搜索词',
        "subtitle_line2": "解决：找词难、写标题难、本地投放不精准、客户搜什么不知道",
        "card1_title": "🔍 真实搜索词",
        "card1_desc": "抓取百度真实用户搜索数据，非AI生成",
        "card2_title": "🧠 AI智能分析",
        "card2_desc": "行业专属分类与投放建议，数据驱动决策",
        "card3_title": "📝 一键生成标题",
        "card3_desc": "抖音/朋友圈爆款标题直接复制使用",
        "card4_title": "📥 数据导出",
        "card4_desc": "支持Excel导出，方便团队协作分析",
        "input_section_title": "🎯 输入参数",
        "main_word_label": "核心主词",
        "main_word_placeholder": "请输入核心关键词，如：广告牌、门头制作、网站建设",
        "city_label": "城市/区县",
        "city_placeholder": "常州 / 武进 / 无锡",
        "source_label": "抓取来源",
        "grab_button": "🚀 挖掘真实关键词",
        "ai_analysis_button": "🧠 AI行业分析",
        "success_message": "✅ 成功挖到 <strong>{count}</strong> 个真实搜索词（非AI编造）",
        "analysis_table_title": "📊 行业AI分析表",
        "export_analysis_button": "📥 导出分析表",
        "viral_titles_title": "🔥 爆款标题（直接复制发抖音/朋友圈）",
        "raw_keywords_title": "📚 原始关键词库",
        "export_keywords_button": "📥 仅导出关键词",
        "footer_company": "📌 制作单位：扬州艾加广告有限公司",
        "footer_slogan": "专注户外广告 · 精准投放解决方案",
        "copyright": "© 2026 扬州艾加广告有限公司 版权所有",
        "no_results": "📭 暂无数据，请先输入关键词进行挖掘",
        "spinner_grabbing": "🎯 正在抓取真实用户搜索词...",
        "spinner_analysis": "🧠 行业AI分析中...",
        "col_keyword": "关键词",
        "col_category": "行业分类",
        "col_traffic_score": "流量评分⭐",
        "col_competition": "竞争难度🔴",
        "col_suggestion": "投放建议",
        "cate_price": "💰 价格词（高意向客户）",
        "cate_merchant": "🏢 商家词（直接找你）",
        "cate_craft": "🛠️ 工艺词（精准业务）",
        "cate_product": "📢 产品词（核心成交）",
        "cate_local": "📍 本地词（最值钱）",
        "cate_question": "❓ 疑问词（适合做内容）",
        "cate_general": "🔍 通用流量词",
        "suggest_priority": "✅ 优先投放（高流量低竞争）",
        "suggest_regular": "🟡 常规投放（稳定获客）",
        "suggest_content": "🔍 内容布局（长尾获客）",
        "suggest_cautious": "⚠️ 谨慎投放（高竞争）",
        "title1": "{city}{main_word}怎么选？老板必看避坑指南",
        "title2": "做{main_word}别乱花钱！这几种位置效果最好",
        "title3": "{city}专业{main_word}制作安装一站式服务",
        "title4": "{main_word}多少钱一平方？行业内部报价",
        "title5": "{city}本地{main_word}厂家，免费上门测量",
        "title6": "2026年{main_word}新趋势，这样做转化率翻倍",
        "title7": "{city}商圈/社区/道闸广告投放攻略",
        "title8": "做{main_word}找对公司，少走一半弯路",
        "title9": "{city}{main_word}投放效果差？问题出在这3点",
        "title10": "{main_word}设计技巧：让你的广告一眼被记住",
        "title11": "{city}{main_word}安装注意事项，新手必看",
    },
    "en": {
        "page_title": "Keyword Mining Tool",
        "activation_title": "🔐 Software Activation",
        "machine_code_label": "Your Machine Code",
        "activation_code_label": "Please Enter Activation Code",
        "activation_code_placeholder": "Enter 24-character activation code",
        "activate_button": "✅ Activate Software",
        "activation_success": "🎉 Activation successful! Entering software...",
        "activation_error": "❌ Invalid activation code, please contact customer service",
        "activation_hint": "Tip: Send the machine code to customer service to get activation code",
        "main_title": "🏢 Keyword Mining Tool",
        "subtitle_line1": '<span class="highlight-text">Industry Professional Version</span> · Accurately Mine Real User Search Terms',
        "subtitle_line2": "Solve: Difficulty finding keywords, writing titles, local targeting, knowing what customers search",
        "card1_title": "🔍 Real Search Terms",
        "card1_desc": "Capture real user search data from Baidu, not AI-generated",
        "card2_title": "🧠 AI Intelligent Analysis",
        "card2_desc": "Industry-specific classification and placement suggestions, data-driven decisions",
        "card3_title": "📝 One-Click Title Generation",
        "card3_desc": "Copy viral titles for Douyin/WeChat Moments directly",
        "card4_title": "📥 Data Export",
        "card4_desc": "Excel export supported for team collaboration",
        "input_section_title": "🎯 Input Parameters",
        "main_word_label": "Core Keyword",
        "main_word_placeholder": "Enter core keyword, e.g.: signboard, storefront, website building",
        "city_label": "City/District",
        "city_placeholder": "Changzhou / Wujin / Wuxi",
        "source_label": "Data Sources",
        "grab_button": "🚀 Mine Real Keywords",
        "ai_analysis_button": "🧠 AI Industry Analysis",
        "success_message": "✅ Successfully mined <strong>{count}</strong> real search terms (not AI-generated)",
        "analysis_table_title": "📊 Industry AI Analysis Table",
        "export_analysis_button": "📥 Export Analysis Table",
        "viral_titles_title": "🔥 Viral Titles (Copy directly for Douyin/WeChat Moments)",
        "raw_keywords_title": "📚 Raw Keyword Database",
        "export_keywords_button": "📥 Export Keywords Only",
        "footer_company": "📌 Produced by: Yangzhou Aija Advertising Co., Ltd.",
        "footer_slogan": "Focus on Outdoor Advertising · Precision Targeting Solutions",
        "copyright": "© 2026 Yangzhou Aija Advertising Co., Ltd. All Rights Reserved",
        "no_results": "📭 No data yet, please enter keywords to start mining",
        "spinner_grabbing": "🎯 Grabbing real user search terms...",
        "spinner_analysis": "🧠 Running AI industry analysis...",
        "col_keyword": "Keyword",
        "col_category": "Industry Category",
        "col_traffic_score": "Traffic Score⭐",
        "col_competition": "Competition🔴",
        "col_suggestion": "Placement Suggestion",
        "cate_price": "💰 Price Terms (High Intent)",
        "cate_merchant": "🏢 Merchant Terms (Direct Contact)",
        "cate_craft": "🛠️ Craft Terms (Precise Business)",
        "cate_product": "📢 Product Terms (Core Conversion)",
        "cate_local": "📍 Local Terms (Most Valuable)",
        "cate_question": "❓ Question Terms (Content Marketing)",
        "cate_general": "🔍 General Traffic Terms",
        "suggest_priority": "✅ Priority Placement (High Traffic Low Competition)",
        "suggest_regular": "🟡 Regular Placement (Stable Leads)",
        "suggest_content": "🔍 Content Strategy (Long-tail Leads)",
        "suggest_cautious": "⚠️ Cautious Placement (High Competition)",
        "title1": "How to choose {city}{main_word}? Must-read guide for business owners",
        "title2": "Don't waste money on {main_word}! These locations work best",
        "title3": "{city} Professional {main_word} production and installation service",
        "title4": "How much per square meter for {main_word}? Industry insider pricing",
        "title5": "{city} Local {main_word} manufacturer, free on-site measurement",
        "title6": "2026 {main_word} trends: Double your conversion rate this way",
        "title7": "{city} Business district/community advertising placement guide",
        "title8": "Find the right company for {main_word}, save half the effort",
        "title9": "{city} {main_word} not performing well? 3 reasons why",
        "title10": "{main_word} design tips: Make your ad unforgettable",
        "title11": "{city} {main_word} installation tips, beginner's guide",
    }
}

def get_text(key):
    """获取当前语言的文本"""
    lang = st.session_state.get("language", "zh")
    return TRANSLATIONS.get(lang, TRANSLATIONS["zh"]).get(key, key)

# ====================== 软件加密模块 ======================
DB_PATH = os.path.join(os.path.dirname(__file__), "activation.db")

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activations 
                 (machine_code TEXT PRIMARY KEY, 
                  activation_code TEXT,
                  activated_at TEXT,
                  client_info TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS machine_hwid
                 (machine_code TEXT PRIMARY KEY,
                  hwid TEXT,
                  first_seen TEXT,
                  last_seen TEXT)''')
    conn.commit()
    conn.close()

def get_hardware_id():
    """获取硬件ID"""
    try:
        # 获取多个硬件信息组合
        parts = []
        
        # CPU ID
        try:
            cpu = subprocess.check_output(['wmic', 'cpu', 'get', 'processorid'], shell=True, text=True).strip().split('\n')[-1].strip()
            if cpu: parts.append(cpu)
        except: pass
        
        # 主板序列号
        try:
            board = subprocess.check_output(['wmic', 'baseboard', 'get', 'serialnumber'], shell=True, text=True).strip().split('\n')[-1].strip()
            if board and board != 'To be filled by O.E.M.': parts.append(board)
        except: pass
        
        # 系统卷序列号
        try:
            vol = subprocess.check_output(['vol', 'C:'], shell=True, text=True)
            vol_match = re.search(r'Serial Number is (\w+)', vol)
            if vol_match: parts.append(vol_match.group(1))
        except: pass
        
        # BIOS序列号
        try:
            bios = subprocess.check_output(['wmic', 'bios', 'get', 'serialnumber'], shell=True, text=True).strip().split('\n')[-1].strip()
            if bios and bios != 'To be filled by O.E.M.': parts.append(bios)
        except: pass
        
        # 系统UUID
        try:
            sys_uuid = subprocess.check_output(['wmic', 'csproduct', 'get', 'uuid'], shell=True, text=True).strip().split('\n')[-1].strip()
            if sys_uuid and sys_uuid != '00000000-0000-0000-0000-000000000000': parts.append(sys_uuid)
        except: pass
        
        # 磁盘序列号
        try:
            disk = subprocess.check_output(['wmic', 'diskdrive', 'get', 'serialnumber'], shell=True, text=True).strip().split('\n')[-1].strip()
            if disk: parts.append(disk)
        except: pass
        
        if parts:
            return '|'.join(parts)
        return None
    except:
        return None

def get_machine_code():
    """获取机器唯一标识 - 使用浏览器指纹技术"""
    # 检查URL参数中是否有client_id
    query_params = st.query_params
    client_id = None
    
    if 'client_id' in query_params:
        client_id = query_params['client_id']
    
    # 如果URL中没有，尝试从session_state获取
    if not client_id and 'client_id' in st.session_state:
        client_id = st.session_state['client_id']
    
    # 如果还是没有，生成新的唯一ID
    if not client_id:
        # 使用UUID生成唯一客户端ID
        client_id = f"CL{uuid.uuid4().hex[:20].upper()}"
        st.session_state['client_id'] = client_id
    
    # 生成机器码（基于客户端ID）
    machine_code = hashlib.md5(client_id.encode()).hexdigest().upper()[:16]
    st.session_state['machine_code'] = machine_code
    
    # 输出JavaScript来持久化client_id到localStorage
    js_code = f"""
    <script>
    // 持久化client_id到localStorage
    var storedId = localStorage.getItem('ad_keyword_tool_client_id');
    var currentId = '{client_id}';
    
    if (!storedId) {{
        localStorage.setItem('ad_keyword_tool_client_id', currentId);
    }} else if (storedId !== currentId) {{
        // 如果localStorage中有不同的ID，使用存储的ID
        localStorage.setItem('ad_keyword_tool_client_id', storedId);
        // 重定向到使用存储ID的URL
        window.location.href = window.location.origin + window.location.pathname + '?client_id=' + storedId;
    }}
    </script>
    """
    st.components.v1.html(js_code, height=0)
    
    return machine_code

def is_activated(machine_code):
    """检查是否已激活"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT activation_code FROM activations WHERE machine_code=?", (machine_code,))
    result = c.fetchone()
    conn.close()
    return result is not None

def activate_machine(machine_code, activation_code):
    """激活机器"""
    if verify_activation_code(machine_code, activation_code):
        init_database()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO activations (machine_code, activation_code, activated_at) VALUES (?, ?, ?)",
                  (machine_code, activation_code, time.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True
    return False

def get_activation_count():
    """获取已激活机器数量"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM activations")
    count = c.fetchone()[0]
    conn.close()
    return count

def generate_activation_code(machine_code, secret_key="AIJIA_ADVERTISING_2024"):
    """生成激活码（管理员使用）"""
    raw = f"{machine_code}{secret_key}"
    return hashlib.sha256(raw.encode()).hexdigest().upper()[:24]

def verify_activation_code(machine_code, activation_code, secret_key="AIJIA_ADVERTISING_2024"):
    """验证激活码"""
    expected_code = generate_activation_code(machine_code, secret_key)
    return activation_code == expected_code

# 预定义的演示激活码（用于测试）
DEMO_MACHINE_CODE = "ABCDEF1234567890"
DEMO_ACTIVATION_CODE = "5F5A6C3E8B2D9A1E4C7F0B3A6D9E2C5F"

# ====================== 页面配置 ======================
# 初始化语言设置
if "language" not in st.session_state:
    st.session_state.language = "zh"

st.set_page_config(page_title=get_text("page_title"), layout="centered", page_icon="🏢")

# ====================== 自定义CSS样式 ======================
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 10px;
        }
        .stTitle {
            color: #fff !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stSubheader {
            color: #f0f0f0 !important;
            font-size: 1.1rem !important;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 12px 16px;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.2);
            color: #fff;
            font-size: 1rem;
        }
        .stMultiSelect > div > div > div {
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.2);
        }
        .stButton > button {
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .success-box {
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            border-radius: 12px;
            padding: 16px 24px;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,184,148,0.3);
        }
        .dataframe-container {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .download-btn {
            background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
            color: white !important;
        }
        .info-card {
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #00cec9;
        }
        .footer {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 20px;
            margin-top: 30px;
        }
        .highlight-text {
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        /* 响应式设计 - 平板/小屏幕适配 */
        @media (max-width: 768px) {
            .main {
                padding: 5px;
            }
            .stTitle {
                font-size: 1.5rem !important;
            }
            .info-card {
                padding: 15px;
            }
            .stButton > button {
                padding: 10px 16px;
                font-size: 0.9rem;
            }
            .dataframe-container {
                padding: 10px;
                overflow-x: auto;
            }
        }
        /* 小屏幕手机适配 */
        @media (max-width: 480px) {
            .stTitle {
                font-size: 1.3rem !important;
            }
            .info-card {
                padding: 12px;
                margin-bottom: 10px;
            }
            .stTextInput > div > div > input {
                padding: 10px 12px;
                font-size: 0.9rem;
            }
            .stButton > button {
                padding: 8px 14px;
                font-size: 0.85rem;
            }
        }
        /* 超小屏幕适配 */
        @media (max-width: 360px) {
            .stTitle {
                font-size: 1.1rem !important;
            }
            .info-card {
                padding: 10px;
            }
            .footer {
                padding: 12px;
            }
        }
        .category-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ====================== 缓存与状态初始化 ======================
if "result_df" not in st.session_state:
    st.session_state.result_df = None
if "analysis_df" not in st.session_state:
    st.session_state.analysis_df = None
if "titles" not in st.session_state:
    st.session_state.titles = ""

# ====================== 抓取模块（修复反爬与异常）======================
def get_baidu_suggest(keyword):
    try:
        url = "https://suggestion.baidu.com/su"
        params = {"wd": keyword, "cb": "callback", "tn": "baidu", "p": "3"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.baidu.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        res = re.findall(r'"(.*?)"', r.text)
        return [w for w in res[1:] if w and len(w) > 2]
    except Exception as e:
        st.warning(f"百度下拉抓取异常：{str(e)}")
        return []

def get_baidu_related(keyword):
    try:
        url = f"https://www.baidu.com/s?wd={keyword}&pn=0"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.baidu.com/"
        }
        r = requests.get(url, headers=headers, timeout=5)
        rel = re.findall(r'id="rs".*?>(.*?)</div>', r.text, re.S)
        if rel:
            words = re.findall(r'href="[^"]+">([^<]+)</a >', rel[0])
            return [w.strip() for w in words if len(w.strip()) > 2]
        return []
    except Exception as e:
        st.warning(f"百度相关抓取异常：{str(e)}")
        return []

def get_douyin_suggest(keyword):
    try:
        url = f"https://www.douyin.com/aweme/v1/web/general/search/single/"
        params = {
            "keyword": keyword,
            "search_source": "normal_search",
            "query_correct_option": "1",
            "lid": "7176583228829246216",
            "type": "1"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.douyin.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        data = r.json()
        results = []
        if "item_list" in data:
            for item in data["item_list"][:10]:
                if "word" in item:
                    results.append(item["word"])
        return [w for w in results if w and len(w) > 2]
    except Exception as e:
        st.warning(f"抖音抓取异常：{str(e)}")
        return []

def get_xiaohongshu_suggest(keyword):
    try:
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/search_top"
        params = {
            "keyword": keyword,
            "search_note": "1",
            "sort": "general"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.xiaohongshu.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        data = r.json()
        results = []
        if "data" in data and "items" in data["data"]:
            for item in data["data"]["items"][:10]:
                if "keyword" in item:
                    results.append(item["keyword"])
        return [w for w in results if w and len(w) > 2]
    except Exception as e:
        st.warning(f"小红书抓取异常：{str(e)}")
        return []

def get_taobao_suggest(keyword):
    try:
        url = "https://suggest.taobao.com/sug"
        params = {"q": keyword, "code": "utf-8"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.taobao.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        data = r.json()
        results = []
        if "result" in data:
            for item in data["result"]:
                if len(item) > 0:
                    results.append(item[0])
        return [w for w in results if w and len(w) > 2]
    except Exception as e:
        st.warning(f"淘宝抓取异常：{str(e)}")
        return []

def get_jd_suggest(keyword):
    try:
        url = "https://dd-search.jd.com"
        params = {"key": keyword, "enc": "utf-8"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.jd.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        res = re.findall(r'"q":"([^"]+)"', r.text)
        return [w for w in res if w and len(w) > 2]
    except Exception as e:
        st.warning(f"京东抓取异常：{str(e)}")
        return []

def get_alibaba_suggest(keyword):
    try:
        url = "https://s.1688.com/youyuan/index.htm"
        params = {"keywords": keyword}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.1688.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        res = re.findall(r'"keywords":"([^"]+)"', r.text)
        return [w for w in res if w and len(w) > 2]
    except Exception as e:
        st.warning(f"阿里巴巴抓取异常：{str(e)}")
        return []

def get_kuaishou_suggest(keyword):
    try:
        url = "https://www.kuaishou.com/search/search palavra"
        params = {"keyword": keyword}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.kuaishou.com/"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        data = r.json()
        results = []
        if "data" in data and "result" in data["data"]:
            for item in data["data"]["result"][:10]:
                if "word" in item:
                    results.append(item["word"])
        return [w for w in results if w and len(w) > 2]
    except Exception as e:
        st.warning(f"快手抓取异常：{str(e)}")
        return []

# ====================== 户外广告行业AI分析（优化评分逻辑）======================
def outdoor_ai_analysis(keywords, city=""):
    if not keywords:
        return []
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2,3))
    try:
        X = vectorizer.fit_transform(keywords)
        scores = np.array(X.sum(axis=1)).flatten()
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8) * 8 + 2
    except:
        scores = np.array([5] * len(keywords))
    
    result = []
    for i, kw in enumerate(keywords):
        kw_lower = kw.lower()
        length = len(kw)
        flow_score = min(10, max(1, int(scores[i])))
        competition = min(10, max(1, int(length / 2) + 1))
        
        if any(x in kw_lower for x in ["价格", "多少钱", "报价", "费用", "收费", "price", "cost", "how much"]):
            cate = get_text("cate_price")
        elif any(x in kw_lower for x in ["公司", "厂家", "哪家好", "电话", "联系", "company", "manufacturer", "contact"]):
            cate = get_text("cate_merchant")
        elif any(x in kw_lower for x in ["制作", "安装", "设计", "加工", "施工", "搭建", "production", "install", "design"]):
            cate = get_text("cate_craft")
        elif any(x in kw_lower for x in ["门头", "围挡", "道闸", "高炮", "大牌", "灯箱", "广告牌", "发光字", "sign", "billboard", "banner"]):
            cate = get_text("cate_product")
        elif city and city in kw:
            cate = get_text("cate_local")
        elif any(x in kw_lower for x in ["怎么", "如何", "哪家", "哪里", "推荐", "how to", "where", "which"]):
            cate = get_text("cate_question")
        else:
            cate = get_text("cate_general")
        
        if flow_score >= 7 and competition <= 5:
            suggest = get_text("suggest_priority")
        elif flow_score >= 6 and competition <= 7:
            suggest = get_text("suggest_regular")
        elif flow_score < 5:
            suggest = get_text("suggest_content")
        else:
            suggest = get_text("suggest_cautious")
        
        result.append({
            get_text("col_keyword"): kw,
            get_text("col_category"): cate,
            get_text("col_traffic_score"): flow_score,
            get_text("col_competition"): competition,
            get_text("col_suggestion"): suggest
        })
    return result

# ====================== 户外广告标题自动生成 ======================
def gen_outdoor_titles(main_word, city):
    city_prefix = city + " " if city.strip() else ""
    titles = [
        get_text("title1").format(city=city_prefix, main_word=main_word),
        get_text("title2").format(city=city_prefix, main_word=main_word),
        get_text("title3").format(city=city_prefix, main_word=main_word),
        get_text("title4").format(city=city_prefix, main_word=main_word),
        get_text("title5").format(city=city_prefix, main_word=main_word),
        get_text("title6").format(city=city_prefix, main_word=main_word),
        get_text("title7").format(city=city_prefix, main_word=main_word),
        get_text("title8").format(city=city_prefix, main_word=main_word),
        get_text("title9").format(city=city_prefix, main_word=main_word),
        get_text("title10").format(city=city_prefix, main_word=main_word),
        get_text("title11").format(city=city_prefix, main_word=main_word),
    ]
    return "\n".join(titles)

# ====================== 主页面 ======================
def main():
    # ====================== 软件激活验证 ======================
    if "activated" not in st.session_state:
        st.session_state.activated = False
    
    # 获取机器码
    machine_code = get_machine_code()
    
    # 检查数据库中是否已激活
    if is_activated(machine_code):
        st.session_state.activated = True
    
    # 激活页面
    if not st.session_state.activated:
        # 激活页面样式
        st.markdown("""
            <style>
                .activation-bg {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .activation-card {
                    background: rgba(255,255,255,0.08);
                    border-radius: 16px;
                    padding: 24px;
                    max-width: 400px;
                    margin: 0 auto;
                }
                .activation-title {
                    color: #fff;
                    font-size: 1.5rem;
                    text-align: center;
                    margin-bottom: 24px;
                }
                .activation-label {
                    color: #a0aec0;
                    font-size: 0.9rem;
                    margin-bottom: 8px;
                }
                .activation-input {
                    border-radius: 10px;
                    padding: 12px;
                    width: 100%;
                    background: rgba(255,255,255,0.1);
                    border: 2px solid rgba(255,255,255,0.2);
                    color: #fff;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # 激活页面内容
        st.markdown("""<div class="activation-bg">""", unsafe_allow_html=True)
        
        # 标题
        st.markdown("""<h1 class="activation-title">🔐 软件激活</h1>""", unsafe_allow_html=True)
        
        # 激活卡片
        st.markdown("""<div class="activation-card">""", unsafe_allow_html=True)
        
        # 机器码显示
        st.markdown("""<p class="activation-label">您的机器码</p>""", unsafe_allow_html=True)
        st.code(machine_code, language="text")
        
        # 激活码输入
        st.markdown("""<p class="activation-label">请输入激活码</p>""", unsafe_allow_html=True)
        activation_code = st.text_input("", placeholder="请输入24位激活码", max_chars=24, key="activation_input")
        
        # 激活按钮
        if st.button("激活软件", use_container_width=True):
            if verify_activation_code(machine_code, activation_code.strip().upper()):
                # 激活成功
                if activate_machine(machine_code, activation_code.strip().upper()):
                    st.session_state.activated = True
                    st.success("✅ 激活成功！即将进入系统...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ 激活失败，请重试")
            else:
                st.error("❌ 激活码无效，请联系管理员获取")
        
        # 提示信息
        st.markdown("""
            <p style="color: #63b3ed; font-size: 0.85rem; margin-top: 16px; text-align: center;">
                如需激活码，请联系扬州艾加广告有限公司
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        return
    
    # 语言切换按钮 - 手机适配
    col_lang = st.columns([3, 1])[1]
    with col_lang:
        st.button("🌐 中文/EN", key="lang_toggle_main", use_container_width=True)
    
    # 头部标题区域 - 响应式设计
    st.markdown(f"""
        <div style="text-align: center; padding: 30px 10px 20px;">
            <h1 class="stTitle">{get_text("main_title")}</h1>
            <p style="color: #a0aec0; font-size: 1rem; margin-top: 10px;">
                {get_text("subtitle_line1")}
            </p>
            <p style="color: #63b3ed; font-size: 0.9rem; margin-top: 8px;">
                {get_text("subtitle_line2")}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 功能介绍卡片 - 响应式网格布局
    st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px;">
            <div class="info-card">
                <h4 style="color: #00cec9; margin-bottom: 8px;">{get_text("card1_title")}</h4>
                <p style="color: #a0aec0; font-size: 0.85rem;">{get_text("card1_desc")}</p>
            </div>
            <div class="info-card">
                <h4 style="color: #00cec9; margin-bottom: 8px;">{get_text("card2_title")}</h4>
                <p style="color: #a0aec0; font-size: 0.85rem;">{get_text("card2_desc")}</p>
            </div>
            <div class="info-card">
                <h4 style="color: #00cec9; margin-bottom: 8px;">{get_text("card3_title")}</h4>
                <p style="color: #a0aec0; font-size: 0.85rem;">{get_text("card3_desc")}</p>
            </div>
            <div class="info-card">
                <h4 style="color: #00cec9; margin-bottom: 8px;">{get_text("card4_title")}</h4>
                <p style="color: #a0aec0; font-size: 0.85rem;">{get_text("card4_desc")}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 输入区域
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 16px; padding: 16px; margin-bottom: 20px;">
            <h3 style="color: #fff; margin-bottom: 16px; font-size: 1.1rem;">{get_text("input_section_title")}</h3>
    """, unsafe_allow_html=True)
    
    # 使用响应式布局 - 手机单列，桌面三列
    col1, col2, col3 = st.columns([1,1,1], gap="small")
    with col1:
        main_word = st.text_input(get_text("main_word_label"), value="", placeholder=get_text("main_word_placeholder"), label_visibility="visible")
    with col2:
        city = st.text_input(get_text("city_label"), placeholder=get_text("city_placeholder"), label_visibility="visible")
    with col3:
        sources = st.multiselect(
            get_text("source_label"),
            ["百度下拉", "百度相关", "抖音", "淘宝", "京东", "阿里巴巴"],
            default=["百度下拉", "百度相关"],
            label_visibility="visible"
        )

    # 按钮区域 - 响应式布局
    c1, c2 = st.columns([1,1], gap="small")
    with c1:
        grab = st.button(get_text("grab_button"), use_container_width=True)
    with c2:
        ai_analysis = st.button(get_text("ai_analysis_button"), use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # 执行挖掘
    if grab and main_word.strip():
        with st.spinner(get_text("spinner_grabbing")):
            words = []
            if "百度下拉" in sources:
                words += get_baidu_suggest(main_word)
                time.sleep(0.5)
            if "百度相关" in sources:
                words += get_baidu_related(main_word)
                time.sleep(0.5)
            if "抖音" in sources:
                words += get_douyin_suggest(main_word)
                time.sleep(0.5)
            if "淘宝" in sources:
                words += get_taobao_suggest(main_word)
                time.sleep(0.5)
            if "京东" in sources:
                words += get_jd_suggest(main_word)
                time.sleep(0.5)
            if "阿里巴巴" in sources:
                words += get_alibaba_suggest(main_word)
                time.sleep(0.5)
            
            if city.strip():
                words += [
                    f"{city}{main_word}",
                    f"{city}{main_word}公司",
                    f"{city}{main_word}价格",
                    f"{city}{main_word}制作",
                    f"{city}{main_word}安装"
                ]
            
            words = list(set([w for w in words if w and len(w) > 2]))
            df = pd.DataFrame({"关键词": words}).sort_values("关键词").reset_index(drop=True)
            st.session_state.result_df = df
            st.session_state.analysis_df = None
            st.session_state.raw_words = words

    # 展示结果
    if st.session_state.result_df is not None:
        # 重新创建DataFrame以使用当前语言的列名
        if "raw_words" in st.session_state:
            df = pd.DataFrame({get_text("col_keyword"): st.session_state.raw_words}).sort_values(get_text("col_keyword")).reset_index(drop=True)
        else:
            df = st.session_state.result_df.rename(columns={"关键词": get_text("col_keyword")})
        
        st.markdown(f"""
            <div class="success-box">
                {get_text("success_message").format(count=len(df))}
            </div>
        """, unsafe_allow_html=True)

        if ai_analysis and main_word.strip():
            with st.spinner(get_text("spinner_analysis")):
                # 获取原始关键词列表
                if "raw_words" in st.session_state:
                    kw_list = st.session_state.raw_words
                else:
                    kw_list = df[get_text("col_keyword")].tolist()
                analysis_data = outdoor_ai_analysis(kw_list, city)
                adf = pd.DataFrame(analysis_data)
                st.session_state.analysis_df = adf
                st.session_state.titles = gen_outdoor_titles(main_word, city)
                st.session_state.saved_main_word = main_word
                st.session_state.saved_city = city
        
        if st.session_state.analysis_df is not None:
            # 重新生成分析表以使用当前语言
            if "raw_words" in st.session_state and st.session_state.get("regenerate_analysis", True):
                kw_list = st.session_state.raw_words
                analysis_data = outdoor_ai_analysis(kw_list, city)
                adf = pd.DataFrame(analysis_data)
            else:
                adf = st.session_state.analysis_df
            
            st.markdown(f"""
                <div style="margin-top: 20px;">
                    <h3 style="color: #fff; margin-bottom: 12px; font-size: 1.1rem;">{get_text("analysis_table_title")}</h3>
                </div>
            """, unsafe_allow_html=True)
            # 响应式表格容器 - 手机端支持水平滚动
            st.markdown("""
                <div class="dataframe-container" style="overflow-x: auto; -webkit-overflow-scrolling: touch;">
            """, unsafe_allow_html=True)
            st.dataframe(adf, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Excel导出
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                adf.to_excel(writer, index=False, sheet_name="关键词分析")
            output.seek(0)
            st.download_button(
                get_text("export_analysis_button"),
                data=output,
                file_name=f"{main_word}{city}行业关键词.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown(f"""
                <div style="margin-top: 24px;">
                    <h3 style="color: #fff; margin-bottom: 16px;">{get_text("viral_titles_title")}</h3>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            # 重新生成标题以使用当前语言
            if "saved_main_word" in st.session_state and "saved_city" in st.session_state:
                current_titles = gen_outdoor_titles(st.session_state.saved_main_word, st.session_state.saved_city)
            else:
                current_titles = st.session_state.titles
            st.text_area("", current_titles, height=220)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div style="margin-top: 24px;">
                <h3 style="color: #fff; margin-bottom: 16px;">{get_text("raw_keywords_title")}</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        raw_output = BytesIO()
        with pd.ExcelWriter(raw_output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="原始关键词")
        raw_output.seek(0)
        st.download_button(
            get_text("export_keywords_button"),
            data=raw_output,
            file_name=f"{main_word}关键词库.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # 页脚信息
    footer_hint = "💡 提示：抓取失败请切换网络，请勿频繁大量抓取" if st.session_state.language == "zh" else "💡 Tip: Switch network if crawling fails, avoid frequent large crawls"
    st.markdown(f"""
        <div class="footer">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <p style="color: #a0aec0; font-size: 0.9rem; margin-bottom: 4px;">
                        <strong style="color: #00cec9;">{get_text("footer_company")}</strong>
                    </p>
                    <p style="color: #63b3ed; font-size: 0.85rem;">
                        {get_text("footer_slogan")}
                    </p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #a0aec0; font-size: 0.85rem;">
                        {footer_hint}
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
