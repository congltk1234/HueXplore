import streamlit as st
from utils import *
from streamlit_extras.stylable_container import stylable_container
import requests
import consts
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state='collapsed')

set_background('assests/bg.png')
from streamlit_navigation_bar import st_navbar
styles = {
    "nav": {
        "background-color": "rgb(255 255 255 / 62%)",
        "justify-content": "center",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "rgb(255 255 255 / 62%)",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": False,
    "show_sidebar": False,
}
page = st_navbar(
    [ " ", "   "],
    styles=styles,
    options=options,
)

init_request = requests.get(consts.domain + "/check-place-dict")

if init_request:
    home_col1, home_col2, home_col3 = st.columns([2.4,6,1.6])
    with home_col2:
        st.image("assests/logo.png")

st.sidebar.header("App")

interests = [
    "🏛️ Kiến Trúc", 
    "🎨 Nghệ Thuật", 
    "⛩️ Văn Hóa", 
    "🛕 Di Sản", 
    "⏳ Lịch Sử",
    "🛒 Mua Sắm",
    "🏺 Bảo Tàng",
    "🏞️ Thiên Nhiên",
    "🧘‍♀️ Chữa lành",
    "🗿 Phế Tích",
    "🍯 Workshop"
]

interests_dict = {
    "🏛️ Kiến Trúc":"architecture", 
    "🎨 Nghệ Thuật":"art", 
    "⛩️ Văn Hóa":"culture", 
    "🛕 Di Sản":'heritage', 
    "⏳ Lịch Sử":'history',
    "🛒 Mua Sắm":'market',
    "🏺 Bảo Tàng":'museum',
    "🏞️ Thiên Nhiên":'nature',
    "🧘‍♀️ Chữa lành":'wellness',
    "🗿 Phế Tích":'ruin',
    "🍯 Workshop":'workshop'
}

moods = [
    "🛣️ Phượt", 
    "📻 Cổ kính", 
    "💓 Lãng mạn", 
    "🙏 Tâm linh", 
    "🏙️ Đường phố",
    "🛍️ Mua sắm",
    "📸 Chụp ảnh",
    "🌊 Biển",
    "🌅 Ngắm cảnh",
    "🥖 Ẩm thực",
    "💆🏻‍♀️ Thư giãn",
    "🎡 Giải trí",
    "🪦 Tưởng niệm"
]
moods_dict = {
    "🛣️ Phượt":'roadtrip', 
    "📻 Cổ kính":'vintage', 
    "💓 Lãng mạn":'romantic', 
    "🙏 Tâm linh":'spiritual', 
    "🏙️ Đường phố":'city explorer',
    "🛍️ Mua sắm":'shopping',
    "📸 Chụp ảnh":'photography',
    "🌊 Biển":'beach-loving',
    "🌅 Ngắm cảnh":'sightseeing',
    "🥖 Ẩm thực":'cuisine',
    "💆🏻‍♀️ Thư giãn":'relax',
    "🎡 Giải trí":'entertain',
    "🪦 Tưởng niệm":'memorial'
}


_, select_col1, select_col2,_ = st.columns([1,4,4,1])

with select_col1:
        with stylable_container(
        key="interest",
        css_styles="""

            .st-bu {
                background-color: rgb(170 98 103);
            }
            .st-emotion-cache-1whx7iy p {
                font-weight: bold;
                font-size: 20px;
            }

            .st-emotion-cache-ue6h4q {
                justify-content: center;
 
            }
            """,    ):
            interests_select = st.multiselect("Sở thích của bạn", interests, key="interests")
            interests_select = [interests_dict[i] for i in interests_select]
    
with select_col2:
        with stylable_container(
        key="moods",
        css_styles="""

         .st-bu {
                background-color: rgb(170 98 103);
            }
            .st-emotion-cache-1whx7iy p {
                font-weight: bold;
                font-size: 20px;
                justify-content: center;
            }
            """,    ):
            moods_select = st.multiselect("Cảm hứng của bạn", moods, key="moods")
            moods_select = [moods_dict[i] for i in moods_select]
_, select_col1,_ = st.columns([5,3,3])
with select_col1:
    with stylable_container(
        key="green_button",
        css_styles="""
            button {
                background-color: #FAC576;
                color: #db1e1e;
                border-radius: 20px;
                border-color: rgb(236 224 83);
                width: 150px;
                height: 50px;
            }
            row-widget stButton {
                text-align:center;
        
            }
            p {
                font-weight: bold;
                font-size: 20px
            }
            """,
    ):
        cfirm_btn = st.button("🗺️ Khám phá")
if cfirm_btn:
    st.session_state["interests_select"] = interests_select
    st.session_state["moods_select"] = moods_select
    st.session_state["is_interests"] = True if len(interests_select) > 0 else False
    st.session_state["is_moods"] = True if len(moods_select) > 0 else False
    st.experimental_set_query_params(page="locations")
    st.switch_page("pages/locations.py")