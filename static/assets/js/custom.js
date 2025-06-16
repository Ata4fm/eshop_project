function filterProducts() {
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}

function addProductToOrder(productId) {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        })
    });
}

function removeOrderDetail(detailId) {
    $.get('/profile/dashboard/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/profile/dashboard/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


$('#contact-form-sw').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function (res) {
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                confirmButtonText: res.confirm_button_text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/';
                }
            });
            form[0].reset();
        },
    });
});

$('#register-form-sw').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function (res) {
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                confirmButtonText: res.confirm_button_text,
                draggable: true
            }).then((result) => {
                if (result.isConfirmed && res.status === 'success') {
                    window.location.href = '/login'
                }
            });
            form[0].reset();
        },
        error: function (xhr) {
            const res = xhr.responseJSON;
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                confirmButtonText: res.confirm_button_text
            });
        }
    });
});


$('#login-form-sw').on('submit', function (e) {
    e.preventDefault();
    const form = $(this);
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function (res) {
            let timerInterval;
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                timer: 3000,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                },
                didClose: (result) => {
                    window.location.href = '/profile/dashboard/';
                }
            })
            form[0].reset();
        },
        error: function (xhr) {
            const res = xhr.responseJSON;
            Swal.fire({
                title: res.title,
                text: res.text,
                icon: res.icon,
                confirmButtonText: res.confirm_button_text,
                confirmButtonColor: '#46a9ae',
                focusConfirm: false,
            });
        }
    });
});