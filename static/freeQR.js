document.getElementById("check").addEventListener("click", (event) => checkQR())
document.getElementById("submit").addEventListener("click", (event) => submit())
document.getElementById("down_png").addEventListener("click", (event) => down_png())
function checkQR() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var img = new Image()
    img.src = document.getElementById('image').src;
    canvas.width = img.width;
    canvas.height = img.height;
    context.drawImage(img, 0, 0);
    var myData = context.getImageData(0, 0, img.width, img.height);
    const code = jsQR(myData.data, img.width, img.height)
    if (code) {
        if (code.data == document.getElementById("url").value) {
            document.getElementById("result").innerHTML = `<i class="fa-regular fa-circle-check"></i> Your QR Code is working perfectly fine! URL: ${code.data}`
        } else {
            document.getElementById("result").innerHTML = `<i class="far fa-question-circle"></i> Your QR Code's functionality is in question! URL: ${code.data}`
        }
    } else {
        document.getElementById("result").innerHTML = `<i class="fa-regular fa-circle-xmark"></i> Your QR Code does not work!`
    }
}
function submit() {
    if (document.getElementById("file_check").checked) {
        var file = document.getElementById("logo_file").files[0]
        var reader = new FileReader();
        reader.onloadend = function () {
            var body = {
                url: document.getElementById("url").value,
                logo: reader.result.replace("data:image/png;base64,", ""),
                version: document.getElementById("version").value,
                error: document.getElementById("error").value,
                box_size: document.getElementById("box_size").value,
                border: document.getElementById("border").value
            }
            sendData(body)
        }
        reader.readAsDataURL(file);
    } else {
        var body = {
            url: document.getElementById("url").value,
            version: document.getElementById("version").value,
            error: document.getElementById("error").value,
            box_size: document.getElementById("box_size").value,
            border: document.getElementById("border").value
        }
        sendData(body)
    }
}
function sendData(body) {
    var myheaders = new Headers()
    myheaders.append("Accept", "*/*")
    myheaders.append("Content-Type", "application/json")

    var options = {
        method: "POST",
        body: JSON.stringify(body),
        headers: myheaders
    }
    var req = new Request("/get_qr", options)
    fetch(req).then(response => response.text()).then(text => {
        document.getElementById("image").src = "data:image/png;base64," + text
    })
}
function down_png() {
    const downloadLink = document.createElement("a");
    downloadLink.href = document.getElementById("image").src;
    downloadLink.download = "your_qr_code.png";
    downloadLink.click();
}