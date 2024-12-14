const EXP_DAYS = 365;
const EXP_TIME = EXP_DAYS * 24 * 60 * 60 * 1000;

/**
 * @param {String} name
 * @param {String} value
 * @returns {void}
 */
function setCookie(name, value) {
    const d = new Date();
    d.setTime(d.getTime() + EXP_TIME);

    let expires = "expires="+ d.toUTCString();
    let path = "path=/";
    let samesite = "SameSite=None";
    let secure = "Secure";

    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + ";" + expires + ";" + path + ";" + samesite + ";" + secure;
}

/**
 * @param {String} name
 * @returns {?String}
 */
function getCookie(name) {
    let name_eq = name + "=";
    let dec_cookie = decodeURIComponent(document.cookie);
    let a = dec_cookie.split(';');
    for (let i = 0; i < a.length; i++) {
        let c = a[i];

        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name_eq) == 0) return c.substring(name_eq.length, c.length);
    }
    return null;
}
