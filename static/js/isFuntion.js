function isUername(username){
    var reg=/^[a-zA-Z]\w{3,17}$/;
    return reg.test(username);
}
function isTel(tel){
        var reg=/^1[3-9]\d{9}$/;
        return reg.test(tel);
}
function isPassword(password){
    var reg=/^[a-zA-Z0-9_]{4,18}$/
    return reg.test(password);
}

