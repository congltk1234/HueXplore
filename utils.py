import base64
import streamlit as st
from pathlib import Path

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# function to render the logo image at the side bar
def add_logo(logo_url: str, height: int = 300):
    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                max-width: 120%;
                height: 120;
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 20}px;
                background-position: 30px 50px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

import os
from json import loads
import json
import google.generativeai as genai
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 30,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Bạn là một hướng dẫn viên du lịch chuyên nghiệp, nắm rõ các thông tin về địa danh văn hóa truyền thống và con người ở Huế. Sau đây là kế hoạch du lịch kèm thông tin về các địa điểm. Hãy giới thiệu đề xuất và đưa ra các tips hữu ích, hành xử và lưu ý cho chuyến đi.",
)
def gen_planer_details(data_plan)->dict:
    data_plan = json.dumps(data_plan)
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "[\n{\n    \"name\": \"Chùa Thiên Mụ\",\n    \"interests\": [\"Di tích\", \"Lịch sử\", \"Văn hóa\"],\n    \"describe\": \"Chùa Thiên Mụ, còn gọi là Chùa Linh Mụ, là một ngôi chùa cổ nằm bên bờ sông Hương, nổi tiếng với kiến trúc độc đáo và phong cảnh hữu tình.\",\n    \"Review\": \"Chùa Thiên Mụ là một điểm đến tuyệt vời để khám phá kiến trúc cổ và thưởng thức cảnh đẹp bên sông Hương.\"\n},\n{\n    \"name\": \"Cầu Tràng Tiền\",\n    \"interests\": [\"Di tích\", \"Lịch sử\", \"Văn hóa\"],\n    \"describe\": \"Cầu Tràng Tiền, còn gọi là Cầu Trường Tiền, là cây cầu nổi tiếng bắc qua sông Hương, biểu tượng của thành phố Huế.\",\n    \"Review\": \"Cầu Tràng Tiền là một địa điểm lý tưởng để ngắm cảnh và chụp ảnh, đặc biệt là vào buổi tối khi cầu được thắp sáng.\"\n},\n{\n    \"name\": \"Đại Nội Huế\",\n    \"interests\": [\"Di tích\", \"Lịch sử\", \"Văn hóa\"],\n    \"describe\": \"Đại Nội Huế là quần thể cung điện và đền đài của triều đại nhà Nguyễn, nơi vua chúa và hoàng tộc sinh sống và làm việc.\",\n    \"Review\": \"Đại Nội Huế là một trong những di sản văn hóa quan trọng nhất của Việt Nam, với kiến trúc tráng lệ và lịch sử phong phú.\"\n},\n{\n    \"name\": \"Chợ Đông Ba\",\n    \"interests\": [\"Văn hóa\", \"Ẩm thực\", \"Mua sắm\"],\n    \"describe\": \"Chợ Đông Ba là khu chợ lớn nhất và nổi tiếng nhất ở Huế, nơi du khách có thể tìm thấy đủ loại đặc sản và hàng hóa địa phương.\",\n    \"Review\": \"Chợ Đông Ba là nơi tuyệt vời để trải nghiệm văn hóa địa phương và thưởng thức ẩm thực Huế.\"\n}\n]\n\nHãy đưa ra thông tin về văn hoá địa phương khi du lịch đến 1 địa điểm ở Huế (nếu có). Ví dụ: tới 1 địa điểm du lịch ở Huế thì không nên làm gì (mặc quần đùi khi đi chùa, quay lưng vào di tích,...), cần chú ý những phong tục tập quán nào,...\n\nKết quả trả về dưới dạng JSON.\n{\n\"Lời dẫn cho từng chặng\": [[chặng_1], [chặng_2], [chặng_3]],\n\"Tips hữu ích\": [ [3 tips tại địa điểm 1], [3 tips tại địa điểm 2], [3 tips tại địa điểm 3], ..., [3 tips tại địa điểm n]],\n\"Lưu ý\": [[3 caution tại địa điểm 1],[ 3 caution tại địa điểm 2],[3 caution tại địa điểm 3],... ,[3 caution tại địa điểm n]]\n}\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"Lời dẫn cho từng chặng\": [[\"Chào mừng bạn đến với Huế - vùng đất cố đô với những di tích lịch sử và văn hóa đặc sắc. Hành trình của chúng ta sẽ bắt đầu từ Chùa Thiên Mụ - một ngôi chùa cổ kính với kiến trúc độc đáo bên bờ sông Hương thơ mộng.\"], [\"Rời Chùa Thiên Mụ, chúng ta sẽ đến với Cầu Tràng Tiền - biểu tượng của Huế. Cây cầu bắc qua sông Hương này không chỉ là điểm kết nối giao thông mà còn là nơi lưu giữ nhiều dấu ấn lịch sử.\"], [\"Tiếp theo, chúng ta sẽ cùng nhau khám phá Đại Nội Huế -  quần thể cung điện và đền đài đồ sộ của triều đại nhà Nguyễn. Nơi đây hứa hẹn sẽ mang đến cho bạn những trải nghiệm thú vị về kiến trúc và lịch sử.\"], [\"Kết thúc hành trình khám phá di sản, chúng ta sẽ đến với Chợ Đông Ba - khu chợ sầm uất và lâu đời nhất ở Huế. Tại đây, bạn có thể tìm thấy đủ loại đặc sản và hàng hóa địa phương, cũng như cảm nhận nhịp sống sôi động của người dân Cố đô.\"]], \"Tips hữu ích\": [[\"Nên mặc trang phục lịch sự, kín đáo khi vào tham quan chùa.\", \"Nên thắp hương và dâng lễ theo hướng dẫn của người địa phương.\", \"Nên dành thời gian đi dạo quanh khuôn viên chùa và ngắm cảnh sông Hương.\"], [\"Nên đi bộ hoặc đạp xe dọc cầu để ngắm cảnh sông Hương.\", \"Nên ghé thăm cầu vào buổi tối để chiêm ngưỡng vẻ đẹp lung linh của cầu khi được thắp sáng.\", \"Nên tìm hiểu về lịch sử và kiến trúc độc đáo của cầu.\"], [\"Nên mua vé tham quan để có thể vào tham quan tất cả các công trình kiến trúc bên trong Đại Nội.\", \"Nên thuê hướng dẫn viên du lịch để hiểu rõ hơn về lịch sử và văn hóa của triều đại nhà Nguyễn.\", \"Nên dành ít nhất nửa ngày để tham quan hết Đại Nội.\"], [\"Nên trả giá khi mua hàng hóa tại chợ.\", \"Nên thử các món ăn đặc sản Huế tại các quầy hàng trong chợ.\", \"Nên chú ý bảo quản tư trang cẩn thận khi đi chợ.\"]], \"Lưu ý\": [[\"Không nên mặc quần áo ngắn, hở hang khi vào chùa.\", \"Không nên nói chuyện ồn ào, cười đùa thiếu nghiêm túc trong khuôn viên chùa.\", \"Không nên xả rác bừa bãi, gây ô nhiễm môi trường.\"], [\"Không nên leo trèo hoặc ngồi lên lan can cầu.\", \"Không nên chen lấn, xô đẩy khi di chuyển trên cầu.\", \"Không nên tự ý dừng đỗ xe trên cầu.\"], [\"Không nên sờ mó, chạm khắc lên các hiện vật lịch sử.\", \"Không nên hút thuốc lá trong khuôn viên Đại Nội.\", \"Không nên mang theo vật dụng cấm vào Đại Nội.\"], [\"Không nên mua hàng hóa không rõ nguồn gốc, xuất xứ.\", \"Không nên ăn uống tại các quán vỉa hè không đảm bảo vệ sinh.\", \"Không nên để lộ tiền bạc hoặc tài sản giá trị khi đi chợ.\"]]}\n\n```",
        ],
        },
    ]
    )

    response = chat_session.send_message(data_plan)
    with open('res.txt', 'w',  encoding='utf-8') as file:
        file.write(response.text)
    data = loads(response.text)
    return data