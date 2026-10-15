import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. TẠO DATAFRAME - DỮ LIỆU ĐÚNG THEO NOTEBOOK ĐÃ GỬI
# ============================================================
data = {
    "Ho_va_ten": [
        "Nguyễn Thị Lan",
        "Phan Bình",
        "Lê Thị Chi",
        "Nguyễn Văn Dũng",
        "Phan Thị Hà",
        "Bùi Lan",
        "Đinh Minh",
        "Lê Văn Nam",
        "Nguyễn Đức Phúc",
        "Nguyễn Thu Trang",
    ],
    "Chuyen_can": [8.0, 8.5, 6.5, 9.5, 7.8, 6.0, 8.9, 7.2, 8.2, 9.7],
    "Giua_ky":    [7.5, 8.0, 5.5, 9.0, 7.0, 6.5, 8.4, 7.5, 7.8, 9.2],
    "Cuoi_ky":    [8.2, 8.3, 6.0, 9.6, 7.5, 6.2, 9.1, 7.0, 8.0, 9.5],
}

df = pd.DataFrame(data)

# ============================================================
# 2. TÍNH ĐIỂM TỔNG KẾT
# Công thức trong notebook: 20% chuyên cần + 30% giữa kỳ + 50% cuối kỳ
# ============================================================
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# ============================================================
# 3. XẾP LOẠI SINH VIÊN THEO ĐIỂM TỔNG KẾT
# ============================================================
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# ============================================================
# 4. CẤU HÌNH VÀ GIAO DIỆN WEB APP
# ============================================================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide",
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý điểm, xếp loại và thống kê kết quả học tập.")

st.subheader("1. Bảng điểm của 10 sinh viên")
bang_diem = df.rename(columns={
    "Ho_va_ten": "Họ và tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại",
})
st.dataframe(bang_diem, use_container_width=True, hide_index=True)

# ============================================================
# 5. THỐNG KÊ ĐIỂM
# ============================================================
st.subheader("2. Thống kê kết quả học tập")

diem_tb = df["Tong_ket"].mean()
diem_max = df["Tong_ket"].max()
diem_min = df["Tong_ket"].min()
sv_max = df.loc[df["Tong_ket"] == diem_max]
sv_min = df.loc[df["Tong_ket"] == diem_min]
so_dat = int((df["Tong_ket"] >= 5).sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
col2.metric("Điểm cao nhất", f"{diem_max:.2f}")
col3.metric("Điểm thấp nhất", f"{diem_min:.2f}")
col4.metric("Số sinh viên đạt (≥ 5)", f"{so_dat}/10")

st.write("**Sinh viên có điểm tổng kết cao nhất:**")
st.dataframe(
    sv_max[["Ho_va_ten", "Tong_ket", "Xep_loai"]].rename(columns={
        "Ho_va_ten": "Họ và tên",
        "Tong_ket": "Tổng kết",
        "Xep_loai": "Xếp loại",
    }),
    use_container_width=True,
    hide_index=True,
)

st.write("**Sinh viên có điểm tổng kết thấp nhất:**")
st.dataframe(
    sv_min[["Ho_va_ten", "Tong_ket", "Xep_loai"]].rename(columns={
        "Ho_va_ten": "Họ và tên",
        "Tong_ket": "Tổng kết",
        "Xep_loai": "Xếp loại",
    }),
    use_container_width=True,
    hide_index=True,
)

# ============================================================
# 6. SELECTBOX TRA CỨU ĐIỂM TỪNG SINH VIÊN
# ============================================================
st.subheader("3. Tra cứu điểm theo sinh viên")
ten_chon = st.selectbox("Chọn sinh viên:", df["Ho_va_ten"].tolist())
sv = df.loc[df["Ho_va_ten"] == ten_chon].iloc[0]

a, b, c, d = st.columns(4)
a.metric("Chuyên cần", f'{sv["Chuyen_can"]:.1f}')
b.metric("Giữa kỳ", f'{sv["Giua_ky"]:.1f}')
c.metric("Cuối kỳ", f'{sv["Cuoi_ky"]:.1f}')
d.metric("Điểm tổng kết", f'{sv["Tong_ket"]:.2f}')
st.info(f'Xếp loại của **{ten_chon}**: **{sv["Xep_loai"]}**')

# ============================================================
# 7. BIỂU ĐỒ CỘT ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN
# ============================================================
st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Ho_va_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.35)
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ============================================================
# 8. THÔNG TIN NGƯỜI TẠO APP - THEO YÊU CẦU ĐỀ BÀI
# ============================================================
st.divider()
st.caption("Người tạo ứng dụng: Lê Văn Nam | MSSV: 067208003476")
