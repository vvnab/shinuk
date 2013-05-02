function inarray(arr, obj){
    for (var i = 0; i < arr.length; i++){
        if (arr[i] == obj) return true;
    }
    return false;
}

function addbookmark(){
    var bm = $.cookie('bookmarks');
    if (bm){
        bm = eval('['+bm.replace(/-/g, ',')+']');
        if (! inarray(bm, ad_id)) bm.push(ad_id);
    } else {
        bm = new Array();
        bm.push(ad_id);
    }
    $.cookie('bookmarks', bm.join('-'), {expires: 30, path: '/'});
    $('.toolbar #like').html('из закладок');
    $('.toolbar #like').removeClass('like like_on');
    $('.toolbar #like').addClass('like_off');
    $('.toolbar #like').attr('href','javascript:delbookmark()');
}

function delbookmark(){
    var bm = $.cookie('bookmarks');
    if (bm){
        bm = eval('['+bm.replace(/-/g, ',')+']');
        for (var i = 0; i < bm.length; i++){
            if (bm[i] == ad_id) bm.splice(i,1);
        }
    } 
    $.cookie('bookmarks', bm.join('-'), {expires: 30, path: '/'});
    $('.toolbar #like').html('в закладки');
    $('.toolbar #like').removeClass('like_off like');
    $('.toolbar #like').addClass('like_on');
    $('.toolbar #like').attr('href','javascript:addbookmark()');
}

$(document).ready(function(){
    var bm = $.cookie('bookmarks');
    if (bm) {
        bm = eval('['+bm.replace(/-/g, ',')+']');
        if (inarray(bm, ad_id)) {
            $('.toolbar #like').html('из закладок');
            $('.toolbar #like').removeClass('like');
            $('.toolbar #like').addClass('like_off');
            $('.toolbar #like').attr('href','javascript:delbookmark()');
        } else {
            $('.toolbar #like').html('в закладки');
            $('.toolbar #like').removeClass('like');
            $('.toolbar #like').addClass('like_on');
            $('.toolbar #like').attr('href','javascript:addbookmark()');
        } 
    } else {
        $('.toolbar #like').html('в закладки');
        $('.toolbar #like').removeClass('like');
        $('.toolbar #like').addClass('like_on');
        $('.toolbar #like').attr('href','javascript:addbookmark()');
    }
})
