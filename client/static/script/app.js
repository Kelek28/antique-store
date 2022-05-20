const site = 'http://127.0.0.1:5001/'
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function fade(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1) {
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}
var alert = document.getElementById("notification")
if (alert) {

    sleep(1500).then(() => {
        fade(alert)
    })
}



function hideCookie() {
    const cookieContainer = document.getElementById("cookie-container")
    axios.request(site + 'acceptcookie').then(response => {
        const users = response.data;
    })
        .catch(error => console.error(error));
    cookieContainer.style.display = "none"
}


function addItemToCart(itemId) {
    axios.request(site + 'additem/' + itemId).then(response => {
        const res = response.data;
        console.log(res);
        document.location.reload(true)

    })
        .catch(error => console.error(error));
}

function showAddingForm() {
    if (document.getElementById('items')) {

        if (document.getElementById('items').style.display == 'none') {
            document.getElementById('items').style.display = '';
            document.getElementById('formAddItem').style.display = 'none';
        }
        else {
            document.getElementById('items').style.display = 'none';
            document.getElementById('formAddItem').style.display = 'block';
        }
    }

}

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        // Save it!
        axios.get(site + 'deletelisting/' + itemId).then(response => {
            const res = response.data;
            document.location.reload(true)

        })
            .catch(error => console.error(error));
    } else {
        // Do nothing!
        console.log('Thing was not saved to the database.');
    }
}

function checkUrl(e) {
    url = document.getElementById("img").value
    ifLinkValid = url.match(/\.(jpeg|jpg|gif|png)$/) != null
    sumbitButton = document.getElementById("submitNewItem")
    if (!ifLinkValid) {
        sumbitButton.disabled = true
        return
    }
    if (ifLinkValid || url.trim() == "") {
        sumbitButton.disabled = false
        return
    }
}
