var position = 0;
var page = 16;
var listStop = 0;

$(document).ready(function(){
  listStop = Math.random();
  getList(0, listStop);
});

function getList(param, id){
//    hideLoader('#list');
    $('#loader').remove();
    $.ajax({
      url: '/shop/get_goods/',
      type: 'GET',                                      
      dataType: 'json',
      data: {
        'position': param, 
        'page': page, 
        'group': sData.group, 
        'category': sData.category,
        'subcategory': sData.subcategory, 
        'fSort': sData.fSort,
        'fBrand': sData.fBrand,
        'fPrice': sData.fPrice,
        'fSize': sData.fSize,
        'fColor': sData.fColor,
        'fSubcategory': sData.fSubcategory
        },
      beforeSend: function(){
        if (position == 0) showLoader('#list');
      },
      success: function(resp){
        if (listStop != id) {
          return;
        }
        if (position == 0) $('#list').empty();
        var count = resp.count;
        resp = resp.items;
        position += resp.length;
        $('.nav small').html('({0} из {1})'.format(position, count));
        for (var i=0; i<resp.length;i++){
          var cl = '';
          var clear = '';
          if((i % 4) == 0){
            cl = 'alpha';
          }            
          if((i % 4) == 3){
            cl = 'omega';
            clear = '<div class="clear"></div>';
          }            
          var color = '';
          if (resp[i].colors.length > 1){
            for(var c = 0; c < resp[i].colors.length; c++){
            color += '<div img="{2}" class="colorBlock" style="background:#{0}" title="{1}"></div>'.format(resp[i].colors[c][1], resp[i].colors[c][0], resp[i].imgs[c]);
            }
          }
          var oldprice = resp[i].oldprice;
          if (oldprice > 0) {
            oldprice = '<div class="oldprice">{0} р.</div>'.format(intcomma(oldprice));
          } else {
            oldprice = '';
          }
          if (edit){
            $('#list').append('<div class="grid_5 {3}"><div class="list_item"><a class="thing_href" href="/shop/model/{7}/"><img src="{0}"/></a><a class="edit" target="_blank" href="/ladmin/goods_add/?art={7}">редактировать</a><a class="name" href="/shop/model/{7}/">{1}</a>{6}<div class="price">{2} р.</div>{5}</div></div>{4}'.format(resp[i].imgs[0], resp[i].name, intcomma(resp[i].price), cl, clear, color, oldprice, resp[i].art));
          } else {
            $('#list').append('<div class="grid_5 {3}"><div class="list_item"><a class="thing_href" href="/shop/model/{7}/"><img src="{0}"/></a><a class="name" href="/shop/model/{7}/">{1}</a>{6}<div class="price">{2} р.</div>{5}</div></div>{4}'.format(resp[i].imgs[0], resp[i].name, intcomma(resp[i].price), cl, clear, color, oldprice, resp[i].art));
          }
        }
        $('.colorBlock').bind('click', function(){
          var img = $(this).attr('img');
          $(this).parent().find('img').attr('src', img);
        });
        if (resp.length == page){
          getList(position, id);
        }
      },
      error: function(){
//        alert('Произошла ошибка!');
      },
      complete: function(){
        hideLoader('#list');
      }
  });
}