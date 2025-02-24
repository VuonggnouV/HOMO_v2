// Hiển thị nút khi người dùng cuộn xuống
window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    const backToTopButton = document.getElementById("backToTop");
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = "block"; // Hiển thị nút khi lăn quá 300px
    } else {
        backToTopButton.style.display = "none"; // Ẩn nút khi ở trên cùng
    }
}

// Lăn lên đầu trang khi nhấp vào nút
document.getElementById("backToTop").addEventListener("click", function(event) {
    event.preventDefault();
    window.scrollTo({top: 0, behavior: 'smooth'}); // Lăn lên đầu trang với hiệu ứng mượt
});

// Lấy các trường "Từ", "Đến", và "Loại xe"
var fromInput = document.getElementById('from');
var toInput = document.getElementById('to');
var vehicleSelect = document.getElementById('vehicle');

// Lấy phần tử hiển thị ảnh loading, khoảng cách và giá
var loadingElement = document.getElementById('loading');
var priceElement = document.getElementById('price');
var priceDisplay = document.getElementById('price-display');
var distanceDisplay = document.getElementById('distance-display');
var durationDisplay = document.getElementById('duration-display');

// Kiểm tra khi thay đổi các trường
function updatePrice() {
    var fromValue = fromInput.value.trim();
    var toValue = toInput.value.trim();
    var vehicleType = vehicleSelect.value;

    if (!fromValue || !toValue || !vehicleType) return;

    // Hiển thị loading
    loadingElement.style.display = 'block';
    priceDisplay.style.display = 'none';
    distanceDisplay.style.display = 'none';

    // Gọi API để lấy khoảng cách
    fetch(`/address_calculator?from=${encodeURIComponent(fromValue)}&to=${encodeURIComponent(toValue)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Lỗi khi gọi API');
            }
            return response.json();
        })
        .then(data => {
            loadingElement.style.display = 'none';
            var distance = data.distance / 1000; // Chuyển đổi từ mét sang km
            var duration = data.duration / 60; // Chuyển đổi từ giây sang phút

            // Tính giá tiền
            var price = 0;
            if (vehicleType === 'ba_gac') {
                price = distance * 100000;
            } else if (vehicleType === 'xe_tai_nho') {
                price = distance * 200000;
            } else if (vehicleType === 'xe_tai_trung') {
                price = distance * 300000;
            }

            // Hiển thị khoảng cách
            document.getElementById('distance').innerText = `Khoảng cách: ${distance.toFixed(2)} km`;
            distanceDisplay.style.display = 'block';

            // Hiển thị giá tiền
            document.getElementById('price').innerText = `Giá tiền: ${price.toLocaleString()} VND`;
            priceDisplay.style.display = 'block';
        })
        .catch(error => {
            loadingElement.style.display = 'none';
            document.getElementById('distance').innerText = 'Không thể lấy thông tin khoảng cách';
            document.getElementById('price').innerText = '';
            distanceDisplay.style.display = 'block';
            priceDisplay.style.display = 'block';
            console.error('Lỗi:', error);
        });
}

// Gán sự kiện onchange để tự động cập nhật giá
fromInput.addEventListener('change', updatePrice);
toInput.addEventListener('change', updatePrice);
vehicleSelect.addEventListener('change', updatePrice);