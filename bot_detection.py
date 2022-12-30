import streamlit as st
import crawl_info

st.markdown('# <center> 🤖️ 微博机器人识别 </center>', unsafe_allow_html=True)

st.text_input("输入用户ID (例如:6374435213)", key="uid")

if st.button('识别'): 
    if (st.session_state.uid).strip() == "":
        st.error('用户ID不能为空！', icon="🚨")
    user_data = crawl_info.crawl_info((st.session_state.uid).strip())
    user_data = user_data.fillna(-1)

    # 预测结果
    import pickle
    #import xgboost
    # load model from file 模型加载
    #random_forest = pickle.load(open("random_forest.pickle.dat", "rb"))
    xgb_cls = pickle.load(open("./model/xgb1222.pickle.dat", "rb"))
    scaler = pickle.load(open("./model/scale1222.pickle.dat", "rb"))

    user_input  = user_data[['verified','urank','mbrank','statuses_count','follow_count','followers_count','sunshine_credit_level','school','location','gender', 'created_year', 'description','birthday_date','followers_follow','origin_rate','like_num','forward_num','comment_num','post_freq', 'post_location','statuses_follow', 'content_length','content_std', 'name_digit','name_length','richness']]
    user_input = scaler.transform(user_input)
    user_data['bot'] = xgb_cls.predict(user_input)
    user_data['bot_prob'] = xgb_cls.predict(user_input,output_margin=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("用户昵称", user_data['screen_name'].values[0])
    col2.metric("是否是机器人", ['否','是'][user_data['bot'].values[0]])
    col3.metric("Bot Score", user_data['bot_prob'].values[0], help="模型输出的机器人分数，该分数分布在-10～10之间，大于0时模型将账号分类为机器人，小于0时模型将账号分类为人类。",)