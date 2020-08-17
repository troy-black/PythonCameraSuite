// Set 404.png image on error
document.addEventListener('DOMContentLoaded', function (event) {
    document.querySelectorAll('img').forEach(function (img) {
        img.onerror = function () {
            this.src = '../static/img/404.png';
        }
    })
})

function request(method, url, formId) {
    const xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open(method, url);
    xmlHttpRequest.onload = requestOnLoadFunction(xmlHttpRequest);
    if (!!formId) {
        xmlHttpRequest.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xmlHttpRequest.send(
            JSON.stringify(
                convertFormToJson(formId)));
    } else {
        xmlHttpRequest.send();
    }
}

function requestOnLoadFunction(xmlHttpRequest) {
    return function () {
        if (xmlHttpRequest.status === 200) {
            updateElementsFromJson(JSON.parse(this.responseText));
        }
    };
}

function updateElementsFromJson(json) {
    for (let key in json) {
        document.getElementById(key).value = json[key];
    }
}

function convertFormToJson(formId) {
    const inputs = document.getElementById(formId).querySelectorAll('.form-data');
    let json = {};

    for (const field of inputs) {
        if (field.id !== '') {
            json[field.id] = field.type === 'checkbox' ? field.checked : field.value;
        }
    }

    return json;
}
