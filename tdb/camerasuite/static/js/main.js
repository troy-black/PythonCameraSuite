// Set 404.png image on error
document.addEventListener('DOMContentLoaded', function (event) {
    document.querySelectorAll('img').forEach(function (img) {
        img.onerror = function () {
            this.src = '../static/img/404.png';
        }
    })
})

function request(method, url, formId, refresh=false) {
    const xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open(method, url);
    xmlHttpRequest.onload = requestOnLoadFunction(xmlHttpRequest, refresh);
    if (!!formId) {
        let json = convertFormToJson(formId);
        console.log(json);
        xmlHttpRequest.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xmlHttpRequest.send(JSON.stringify(json));
    } else {
        xmlHttpRequest.send();
    }
}

function requestOnLoadFunction(xmlHttpRequest, refresh) {
    return function () {
        if (xmlHttpRequest.status === 200) {
            updateElementsFromJson(JSON.parse(this.responseText));
            if (refresh) {
                debugger;
                location.reload();
            }
        } else {
            debugger;
        }
    };
}

function updateElementsFromJson(json) {
    for (let key in json) {
        const element = document.getElementById(key);
        if (element) {
            element.value = json[key];
        }
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
