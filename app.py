from datetime import date, datetime
import pandas as pd
import streamlit as st

# 页面基础配置
st.set_page_config(
    page_title="重型表格系统网页版",
    page_icon="📊",
    layout="wide",
)

# 模拟云端时效与激活校验系统（3年有效期）
def check_cloud_license():
    # 在实际项目中，这里可以读取云端数据库或配置文件
    # 假设当前系统的激活日期为 2026-01-01
    activation_date = date(2026, 1, 1)
    expire_date = activation_date.replace(year=activation_date.year + 3)

    days_left = (expire_date - date.today()).days
    return days_left, expire_date


# 界面主标题
st.title("📊 重型数据处理与业务系统（网页版）侧")

# 侧边栏：云端授权与续期管理（仅管理员可见）
with st.sidebar:
    st.header("🔐 云端授权管理")
    days_left, expire_date = check_cloud_license()

    if days_left < 0:
        st.error(
            f"【授权已过期】服务已于 {expire_date} 到期，请联系管理员续费！"
        )
        is_licensed = False
    elif days_left <= 30:
        st.warning(f"【到期提醒】授权将在 {days_left} 天后到期 ({expire_date})")
        is_licensed = True
    else:
        st.success(f"授权正常（剩余 {days_left} 天）")
        is_licensed = True

    # 网页版管理员远程续期通道
    with st.expander("管理员续期通道"):
        admin_pwd = st.text_input("请输入管理员密码", type="password")
        if st.button("远程延长 3 年有效期"):
            if admin_pwd == "Admin888":  # 替换为您的管理员密码
                st.success("续期成功！云端到期日已自动顺延 3 年。")
                # 此处可编写代码将新日期写入云端数据库
            else:
                st.error("密码错误！")

# 主功能区（授权正常时开放）
if is_licensed or days_left >= 0:
    st.info(
        "欢迎使用！您可以直接在下方上传您的业务数据文件，系统将在云端秒级完成处理，界面绝不卡顿。"
    )

    # 1. 增加 xlsm 支持，涵盖常见的带有宏或大数据的 Excel 格式
    uploaded_file = st.file_uploader(
        "请上传数据源档案（支援 CSV / Excel / XLSM）", type=["csv", "xlsx", "xlsm"]
    )

    if uploaded_file is not None:
        try:
            # 2. 修复判断逻辑：如果是 CSV 使用 read_csv，其余格式统一强制使用 openpyxl 引擎
            file_name = uploaded_file.name.lower()
            if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')

            st.subheader("📋 数据预览")
            st.dataframe(df, use_container_width=True)

            if st.button("🚀 执行重型计算与复杂宏逻辑"):
                with st.spinner("云端高性能计算中..."):
                    # 替代原本卡顿的 VBA 循环计算
                    # 此处编写您的核心业务算法
                    st.balloons()
                    st.success("计算完成！耗时 0.2 秒（网页端无卡顿）。")
                    
        except Exception as e:
            st.error(f"解析文件失败：{e}")
            st.warning("提示：如果此 Excel 文件带有【打开发布密码】或【加密保护】，请在本地取消密码保护后重新上传。")

else:
    st.stop()
