const EXP_DAYS = 365;
const EXP_TIME = EXP_DAYS * 24 * 60 * 60 * 1000;

/**
 * @param {String} name
 * @param {String} value
 * @returns {void}
 */
function setRawCookie(value) {
    const d = new Date();
    d.setTime(d.getTime() + EXP_TIME);

    let expires = "expires="+ d.toUTCString();
    let path = "path=/";
    let samesite = "SameSite=None";
    let secure = "Secure";

    document.cookie = "data=" + encodeURIComponent(value) + ";" + expires + ";" + path + ";" + samesite + ";" + secure;
}

/**
 * @param {String} name
 * @returns {?JSON.Value}
 */
function getRawCookie() {
    let name_eq = "data=";
    let dec_cookie = decodeURIComponent(document.cookie);
    let a = dec_cookie.split(';');
    for (let i = 0; i < a.length; i++) {
        let c = a[i];

        while (c.charAt(0) === ' ') c = c.substring(1);
        if (c.indexOf(name_eq) === 0) return c.substring(name_eq.length, c.length);
    }
    return null;
}

/**
 * @param {String} name
 * @param {String} value
 * @returns {void}
 */
function setCookieField(name, value) {
    var data = getRawCookie(); 
    if (data === null) {
        data = '{}';
    }
    let data_json = JSON.parse(data);
    data_json[name] = value;
    setRawCookie(JSON.stringify(data_json));
}


/**
 * @param {String} name
 * @returns {any}
 */
function getCookieField(name) {
    var data = getRawCookie(); 
    if (data === null) {
        return null;
    }
    let data_json = JSON.parse(data);
    return name in data_json ? data_json[name] : null;
}

/**
 * @param {String} name
 */
function deleteCookieField(name) {
    var data = getRawCookie(); 
    if (data === null) return;
    let data_json = JSON.parse(data);
    delete data_json[name];
    setRawCookie(JSON.stringify(data_json));
}
