import streamlit as st
import pandas as pd
import folium
import json
from folium import IFrame, plugins
from streamlit_folium import st_folium
import requests
import networkx as nx
import osmnx as ox
from streamlit_extras.grid import grid
# from streamlit_star_rating import st_star_rating
from utils import *
import io
from PIL import Image
import consts

st.write("this is planner")

if "final_locations" in st.session_state:
    final_locations = st.session_state["final_locations"]

col1, col2 = st.columns(spec=[4,6])

describes=[
"""Lăng Gia Long, hay Thiên Thọ Lăng, là nơi an nghỉ của vua Gia Long, vị vua sáng lập triều Nguyễn, nằm tại xã Hương Thọ, thành phố Huế. Khởi công năm 1814 và hoàn tất vào năm 1820, lăng là một quần thể kiến trúc hòa quyện với thiên nhiên, bao gồm 42 đồi núi với ngọn Đại Thiên Thọ làm tiền án. Khu lăng được chia thành ba phần: khu lăng mộ chính của vua và Thừa Thiên Cao Hoàng hậu, khu vực tẩm điện Minh Thành, và Bi Đình với bia "Thánh đức thần công". Các lăng lân cận bao gồm lăng của Thái Tông Hiếu Triết Hoàng hậu, Anh Tông Hiếu Nghĩa Hoàng hậu, chúa Nguyễn Phúc Chú, và mẹ của vua Gia Long. Tuy không được bảo tồn tốt như các lăng khác như Tự Đức hay Khải Định, Lăng Gia Long vẫn là một bức tranh tuyệt tác về sự phối trí giữa thiên nhiên và kiến trúc, mang đến một không gian tĩnh lặng và thơ mộng để suy ngẫm về lịch sử và cuộc đời.""",
'Đại Nội Huế, tọa lạc bên bờ sông Hương, là quần thể kiến trúc cổ kính thuộc Cố đô Huế. Được UNESCO công nhận là di sản văn hóa thế giới, nơi đây từng là trung tâm hành chính và nơi ở của triều đình Nguyễn. Công trình bao gồm Hoàng Thành và Tử Cấm Thành với nhiều kiến trúc độc đáo như Ngọ Môn, Điện Thái Hòa, và Cung Diên Thọ. Đại Nội Huế là điểm du lịch nổi tiếng, hấp dẫn du khách bởi vẻ đẹp tráng lệ, kiến trúc tinh xảo, và giá trị lịch sử phong phú. Thời điểm tốt nhất để tham quan là từ tháng 1 đến tháng 3 hoặc trong mùa lễ hội Festival Huế.',
"Nhà hát ca kịch Huế là nơi diễn ra các buổi biểu diễn nghệ thuật truyền thống của Huế, bao gồm ca kịch cung đình và các loại hình nghệ thuật dân gian khác. Nhà hát mang đậm dấu ấn văn hóa Huế, với kiến trúc cổ kính và không gian biểu diễn trang trọng.",
"Làng nghề hoa giấy Thanh Tiên là một làng nghề truyền thống nổi tiếng ở Huế, nơi sản xuất ra những bông hoa giấy tinh xảo và đẹp mắt. Nghề làm hoa giấy ở đây đã tồn tại hàng trăm năm và gắn liền với đời sống văn hóa của người dân Huế.",
"Âu thuyền Phú Hải là một khu vực đỗ thuyền truyền thống của ngư dân ở Huế, nơi các thuyền đánh cá neo đậu và sửa chữa. Đây là một phần quan trọng trong đời sống và văn hóa của cộng đồng ngư dân địa phương."
]
reviews  =[
"""🌲Đây là lăng xa nhất trong hệ thống các lăng tẩm được đưa vào du lịch ở Huế hiện nay. Lăng nằm tách mình yên mình với lối vào là 1 con đường nhỏ trải dài với hàng thông 2 bên tạo cảm giác mát mẻ và thư thái. Nếu mn để ý thì sẽ thấy lăng Gia Long không có la thành như các lăng khác mà tận dụng chính địa hình núi, đồi, rừng thông để tạo nên la thành tự nhiên của riêng mình.
🌞Từ bên ngoài cổng đi vào bên trong khá xa, các kiến trúc trong lăng nằm rải rác, mn nên thuê xe điện hoặc xe đạp từ ngoài cổng đi vào để có thể khám phá hết vẻ đẹp của lăng mà không bị đuối sức nha.""",
'Đại nội so với 20 năm trước mình tới thăm thật sự đã khác biệt rất nhiều, được trùng tu khá nhiều chứ trước đây toàn tường gạch vỡ nham nhở, nay dọc hai bên lối đi được trùng tu thành dẫy để khách đi được mát, có treo tranh ảnh, tuy nhiên thì vẫn còn rất ít và du khách đi đoạn dài, nắng mà không hiểu rõ là cung gì, để làm gì, thời nào, ai dùng trước đây, được trùng tu khi nào luôn. Giá vé 200k/ người, thuyết minh thì 200k nữa. Tuy nhiên khi đông dồn xếp hàng để qua cổng thấy chưa được văn minh, khách đoàn khách lẻ lẫn lộn, nháo nhác và nóng bức, trong khi cổng bên canh thì khoá, sao không cho khách đoàn đi riêng. Nói chung cần làm dịch vụ hơn nữa, trùng tu hơn nữa.',
'Cơ quan nhà nước, hoạt động nghệ thuật truyền thống hơn 60 năm.',
'Thật tuyệt vời khi vẫn còn những nghệ nhân yêu nghề để gìn giữ một nghề truyền thống qua 400 năm qua. Thật quý trọng và biết ơn ❤️',
"Ngắm hoàng hôn ở đây rất đẹp.mọi người nên ghé nhé"
]
data_plan = []
for i in range(len(final_locations)):
    object_data = final_locations[i]
    data_plan.append({
        "name": object_data['name'],
        "interests": object_data['interests'],
        "moods": object_data['moods'],
        "describe": describes[i],
        "Review": reviews[i],
    })
# st.write(data_plan)
# gen_info = gen_planer_details(data_plan)
from json import loads
with open('res.txt', 'r', encoding='utf-8') as file:
    gen_info = loads(file.read())

st.write(final_locations)
with col2:
    with st.container():
        for i, location in enumerate(final_locations):
            index = i+1
            with st.expander(f'**{index}. {location["name"]}**', expanded=True):
                
                inside_col1, inside_col2 = st.columns(spec=[2,8])
                with inside_col1:
                    st.image(location["img"])
                with inside_col2:
                    long_text = gen_info['Lời dẫn cho từng chặng'][i][0]
                    st.write(long_text)
                    # https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream
                    st.write(f'{location["vote"]}⭐({location["review"]})')
                    st.write(f'Địa chỉ: [{location["address"]}]({location["gg_map"]})')
                    for _ in gen_info['Tips hữu ích'][i]:
                        st.markdown("- " + _)
                    for _ in gen_info["Lưu ý"][i]:
                        st.markdown("- " + _)    
start=[16.4683,107.5786]
with col1:
    url = "https://www.google.com/maps/dir"
    for location in final_locations:
        url += "/" + location["name"] +',' + location["address"]
    st.link_button("Đồng bộ hóa thành công, chuyển đến map", url)
    # stars = st_star_rating('Bạn đánh giá lộ trình này như thế nào?', 5, 0, size=60, emoticons=True, read_only=False, dark_theme=False)
    m = folium.Map(location=start, zoom_start=10)
    gg_res= st.session_state["final_locations"] 
    if len(gg_res)!=0:
        place_show = st.session_state["place_show"]
        for index,place in enumerate(gg_res):
            if index>0:
                res_obj = {
                "origin_node": gg_res[index-1]['node_id'],
                "destination_node": gg_res[index]['node_id'],
                }
                # response = requests.post(url + "/find-route", json = res_obj)
                response = requests.post(consts.domain + "/find-route", json = res_obj)
                points_list= response.json()
                folium.PolyLine(locations=points_list, color='blue', dash_array='5, 5',
                                tooltip=f"From a to b", smooth_factor=0.1,).add_to(m)
            # Define marker variables
            name = place['name']
            website = "#"
            directions = place['gg_map']
            pub_html = folium.Html(f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
            <p style="text-align: center;"><img src="{place['img']}" width="220" height="250">
            <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 14px;">{name} Website</span></a></p>
            <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 14px;">Directions to {name}</span></a></p>
            """, script=True)
            popup = folium.Popup(pub_html, max_width=220)
            icon = folium.Icon(color='red', prefix='fa',icon=f'{index+1}')
            folium.Marker(location=place['coordinate'], tooltip=name, icon=icon, popup = popup).add_to(m)

    folium.FitOverlays().add_to(m)
    folium.plugins.MiniMap(width=100, height=100).add_to(m)
    st_data = st_folium(m, width=600, height=400, returned_objects=[])

st.write(final_locations)