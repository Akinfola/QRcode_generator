//  Function declearation 
let imgBoxEL = document.getElementById('imgBox');

let qrImgEL = document.getElementById('qrImg');

let qrTextEL = document.getElementById('qrText');
function generateQRcode() {

    if(qrText.value.length > 0) {
        qrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + qrText.value;

        imgBoxEL.classList.add("show-img")

    } else {
        qrText.classList.add('error');
        setTimeout(() => {
        qrText.classList.remove('error');
    }, 1000)
    }
}