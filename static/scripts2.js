
const provinceCityData  = {
    "An Giang": ["Long Xuyên", "Châu Đốc"],
    "Bà Rịa - Vũng Tàu": ["Vũng Tàu", "Bà Rịa"],
    "Bắc Giang": ["Bắc Giang"],
    "Bắc Kạn": ["Bắc Kạn"],
    "Bạc Liêu": ["Bạc Liêu"],
    "Bắc Ninh": ["Bắc Ninh"],
    "Bến Tre": ["Bến Tre"],
    "Bình Dương": ["Thủ Dầu Một", "Dĩ An", "Thuận An"],
    "Bình Định": ["Quy Nhơn"],
    "Bình Phước": ["Đồng Xoài"],
    "Bình Thuận": ["Phan Thiết"],
    "Cà Mau": ["Cà Mau"],
    "Cần Thơ": ["Ninh Kiều", "Cái Răng"],
    "Cao Bằng": ["Cao Bằng"],
    "Đà Nẵng": ["Hải Châu", "Thanh Khê"],
    "Đắk Lắk": ["Buôn Ma Thuột"],
    "Đắk Nông": ["Gia Nghĩa"],
    "Điện Biên": ["Điện Biên Phủ"],
    "Đồng Nai": ["Biên Hòa", "Long Khánh"],
    "Đồng Tháp": ["Cao Lãnh", "Sa Đéc"],
    "Gia Lai": ["Pleiku"],
    "Hà Giang": ["Hà Giang"],
    "Hà Nam": ["Phủ Lý"],
    "Hà Nội": ["Ba Đình", "Hoàn Kiếm", "Tây Hồ", "Cầu Giấy"],
    "Hà Tĩnh": ["Hà Tĩnh"],
    "Hải Dương": ["Hải Dương"],
    "Hải Phòng": ["Hồng Bàng", "Lê Chân"],
    "Hậu Giang": ["Vị Thanh"],
    "Hòa Bình": ["Hòa Bình"],
    "Hưng Yên": ["Hưng Yên"],
    "Khánh Hòa": ["Nha Trang", "Cam Ranh"],
    "Kiên Giang": ["Rạch Giá", "Hà Tiên"],
    "Kon Tum": ["Kon Tum"],
    "Lai Châu": ["Lai Châu"],
    "Lâm Đồng": ["Đà Lạt", "Bảo Lộc"],
    "Lạng Sơn": ["Lạng Sơn"],
    "Lào Cai": ["Lào Cai"],
    "Long An": ["Tân An"],
    "Nam Định": ["Nam Định"],
    "Nghệ An": ["Vinh"],
    "Ninh Bình": ["Ninh Bình"],
    "Ninh Thuận": ["Phan Rang-Tháp Chàm"],
    "Phú Thọ": ["Việt Trì"],
    "Phú Yên": ["Tuy Hòa"],
    "Quảng Bình": ["Đồng Hới"],
    "Quảng Nam": ["Tam Kỳ", "Hội An"],
    "Quảng Ngãi": ["Quảng Ngãi"],
    "Quảng Ninh": ["Hạ Long", "Cẩm Phả"],
    "Quảng Trị": ["Đông Hà"],
    "Sóc Trăng": ["Sóc Trăng"],
    "Sơn La": ["Sơn La"],
    "Tây Ninh": ["Tây Ninh"],
    "Thái Bình": ["Thái Bình"],
    "Thái Nguyên": ["Thái Nguyên"],
    "Thanh Hóa": ["Thanh Hóa"],
    "Thừa Thiên Huế": ["Huế"],
    "Tiền Giang": ["Mỹ Tho"],
    "TP Hồ Chí Minh": ["Quận 1", "Quận 3", "Bình Thạnh", "Gò Vấp"],
    "Trà Vinh": ["Trà Vinh"],
    "Tuyên Quang": ["Tuyên Quang"],
    "Vĩnh Long": ["Vĩnh Long"],
    "Vĩnh Phúc": ["Vĩnh Yên"],
    "Yên Bái": ["Yên Bái"]
};

document.addEventListener("DOMContentLoaded", function () {
    const provinceSelect = document.getElementById("province");
    const citySelect = document.getElementById("city");

    // Thêm danh sách tỉnh vào dropdown
    Object.keys(provinceCityData).forEach(province => {
        let option = document.createElement("option");
        option.value = province;
        option.textContent = province;
        provinceSelect.appendChild(option);
    });

    // Cập nhật danh sách thành phố khi chọn tỉnh
    window.updateCities = function () {
        citySelect.innerHTML = '<option value="">Chọn thành phố</option>'; // Reset danh sách
        let selectedProvince = provinceSelect.value;
        if (selectedProvince && provinceCityData[selectedProvince]) {
            provinceCityData[selectedProvince].forEach(city => {
                let option = document.createElement("option");
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        }
    };
});
